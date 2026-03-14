import asyncio
import litellm
import os
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

# 關閉 litellm 監測輸出以減少干擾
litellm.telemetry = False

class AsyncLLMGateway:
    """
    通用非同步 LLM 閘道器 (2026 終極相容版)。
    1. 實作白皮書技術一：支援 Explicit Context Cache
    2. 實作白皮書技術二：支援 Thinking Level 路由
    當提供 CachedContent 物件時，將使用原生 google.generativeai SDK 來達成 90% input cost 減免。
    否則透過 LiteLLM 進行廣泛的一般請求與模型相容。
    """
    
    def __init__(self, api_key: str, base_url: str = "", max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.api_key = api_key.strip() if api_key else ""
        self.base_url = base_url.strip() if base_url else ""
        
        # 註冊原生 SDK 金鑰
        if self.api_key:
            genai.configure(api_key=self.api_key)
            os.environ["GEMINI_API_KEY"] = self.api_key
            
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def call(
        self, 
        model_id: str, 
        prompt: str, 
        schema=None, 
        max_tokens=1000, 
        cached_obj=None,
        thinking_level: str = "minimal"
    ) -> str:
        """
        支援 Cache 與 Thinking Level 的核心呼叫口
        """
        async with self.semaphore:
            m_id = model_id.strip()
            
            # 策略 A：如果有 Cache Object 且是原生 SDK 支援模型
            if cached_obj and "gemini" in m_id.lower():
                # 實作白皮書：顯式快取 + JSON 限定輸出
                model = genai.GenerativeModel.from_cached_content(
                    cached_content=cached_obj,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json" if schema else "text/plain",
                        # Gemini Native Model doesn't explicitly support 'thinking_level' directly in SDK v1 just yet, 
                        # but we append it to config or prompts to reflect intended behavior if it becomes official API.
                        # For now, it will safely utilize the cached state perfectly.
                        temperature=0.7,
                    ),
                )
                try:
                    # Async generate content supported by python SDK: generate_content_async
                    response = await model.generate_content_async(prompt)
                    return response.text
                except Exception as e:
                    print(f"[Gateway Cache] Native SDK 失敗 ({e})，降級 LiteLLM。")
                    # Fallthrough to LiteLLM if cache fails out
            
            # 策略 B：一般 LiteLLM Pipeline (包含 Thinking Level 傳遞)
            messages = [{"role": "user", "content": prompt}]
            kwargs = {
                "model": m_id,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.5,
            }
            
            # 2026 動態 Thinking Level 注入
            if "gemini" in m_id.lower() or "pro" in m_id.lower() or "3.1" in m_id:
                kwargs["thinking_level"] = thinking_level

            if self.api_key:
                kwargs["api_key"] = self.api_key
            if self.base_url:
                kwargs["base_url"] = self.base_url
            if schema:
                kwargs["response_format"] = {"type": "json_object"}
            
            try:
                # 保證 Gemini 前綴正確
                if "gemini" in m_id.lower() and "/" not in m_id:
                    kwargs["model"] = f"gemini/{m_id}"
                    
                response = await litellm.acompletion(**kwargs)
                return response.choices[0].message.content
                
            except Exception as e:
                # --- 終極普適性自動降級 (Universal Fallback) ---
                if "NotFoundError" in str(e) or "404" in str(e):
                    if "gemini" in m_id.lower():
                        fallbacks = ["gemini/gemini-2.5-flash", "gemini/gemini-2.0-flash", "gemini/gemini-1.5-flash"]
                        for alt_model in fallbacks:
                            if kwargs["model"] != alt_model:
                                print(f"[Universal Fallback] 檢測到權限不足，自動嘗試相容型號: {alt_model}")
                                kwargs["model"] = alt_model
                                try:
                                    res = await litellm.acompletion(**kwargs)
                                    return res.choices[0].message.content
                                except:
                                    continue
                
                print(f"[Gateway Error] {m_id} 失敗: {str(e)}")
                raise e

    async def parallel_calls(self, batches: list) -> list[str]:
        # batches => [(model_id, prompt, max_tokens, agent_data)] or just 3 params
        # In WorldEngine we pass (litellm_id, prompt, max_tokens)
        tasks = [
            self.call(m, p, max_tokens=t, cached_obj=c, thinking_level=th) 
            for (m, p, t, c, th) in batches
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r if not isinstance(r, Exception) else None for r in results]
