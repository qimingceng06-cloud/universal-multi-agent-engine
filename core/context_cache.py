import datetime
import json
import logging
import os
import google.generativeai as genai
from google.generativeai import caching

logger = logging.getLogger("ContextCacheManager")

class ContextCacheManager:
    """
    通用 Context Cache (2026白皮書相容版)。
    實作這項技術可省下 90% 的 Input Token 成本。
    如果字數不足 4096 tokens (Gemini Cache 最低門檻)，或者 API Key 無效，
    則會優雅降級回一般字串快取 (Graceful Degradation)。
    """
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        # 儲存 {cache_name: (CachedContent_instance, plain_text_content)}
        self.caches = {}
        
    def _pad_to_minimum(self, content: str, target_chars: int = 15000) -> str:
        """
        Gemini 限制 Context Caching 必須至少有 4096 tokens (約 12000-16000 字元)。
        若不夠，我們透過加入大量的規則說明作為 padding，強硬滿足快取門檻以節省後續 token。
        """
        if len(content) >= target_chars:
            return content
            
        padding = "\n=== 通用安全與動態規則填充 (Padding for Minimum Cache Size) ===\n" * 150
        return content + padding
        
    def create_cache(self, name: str, content: str, ttl_hours: float = 2.0) -> str:
        """
        將世界設定存入 Gemini Context Cache。
        所有 Agent 共用這一份 cache，不需要每次都傳。
        若不支援或失敗，則自動降級為普通 Memory Cache。
        """
        padded_content = self._pad_to_minimum(content)
        
        try:
            if not self.api_key:
                raise ValueError("Missing Gemini API Key")
                
            # 使用 Google SDK 建立實體 Explicit Cache
            cached_obj = caching.CachedContent.create(
                model="models/gemini-2.5-flash", # Fallback to 2.5 flash API if 3 is not fully rolled out in litellm
                display_name=f"sim_cache_{name}",
                contents=[padded_content],
                ttl=datetime.timedelta(hours=ttl_hours),
            )
            
            logger.info(f"Cache 建立成功！名稱: {cached_obj.name}, 過期時間: {cached_obj.expire_time}")
            self.caches[name] = {"obj": cached_obj, "text": content}
            
        except Exception as e:
            logger.warning(f"Explicit Context Cache 失敗 ({e})，降級為一般記憶體快取。")
            # 降級：只存文字
            self.caches[name] = {"obj": None, "text": content}
            
        return content

    def refresh(self, name: str, new_content: str, phase: str = "active"):
        """
        當世界狀態發生重大變化時重建快取。
        利用 phase 參數控制 TTL，避免浪費資源。
        """
        ttl_hours = 2.0 if phase == "active" else 0.5
        
        if name in self.caches and self.caches[name]["obj"]:
            try:
                self.caches[name]["obj"].delete()
                logger.info(f"舊 Cache '{name}' 已刪除。")
            except:
                pass
                
        self.create_cache(name, new_content, ttl_hours=ttl_hours)
        
    def get_cache_text(self, name: str) -> str:
        """取得快取的純文字內容 (給非 Gemini 模型或本地端降級使用)"""
        return self.caches.get(name, {}).get("text", "")
        
    def get_cache_obj(self, name: str):
        """取得 Google 原生的 CachedContent 物件，用於組裝進 LLM Call"""
        return self.caches.get(name, {}).get("obj", None)
