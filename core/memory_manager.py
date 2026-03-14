from collections import deque
from dataclasses import dataclass, field
import asyncio
import logging
from core.async_gateway import AsyncLLMGateway

logger = logging.getLogger("MemoryManager_SALM")

@dataclass
class SALMMemory:
    """Structured Autobiographical Layered Memory (2026 白皮書終極實作版)"""
    # === Layer 1: Identity Core (靜態核心，最高權重，通常由 World/Player 定義) ===
    identity_core: str = ""
    goals: list[str] = field(default_factory=list)
    
    # === Layer 2: Long-Term Archive (由 LLM 自行維護與壓縮，包含世界觀認知與關係變化) ===
    long_term_summary: str = ""
    relationship_graph: dict = field(default_factory=dict) # 記錄對其他 NPC 的看法
    
    # === Layer 3: Short-Term Working Memory (環狀緩衝區，高頻存取) ===
    short_term_buffer: deque = field(default_factory=lambda: deque(maxlen=6))
    
    # Metadata
    steps_since_compression: int = 0
    compression_interval: int = 6  # 每 6 個事件觸發一次向量化/摘要化
    total_steps: int = 0
    total_compression_tokens_used: int = 0

class MemoryManager:
    """
    SALM 記憶管理器 (真實壓縮版)。
    透過將細碎的 Short-Term 經驗智能壓縮成 Long-Term Summary，
    並即時更新 Identity Goals，達成無限上下文。
    """
    
    def __init__(self, gateway: AsyncLLMGateway, model_id: str = "gemini/gemini-2.5-flash"):
        self.memories: dict[str, SALMMemory] = {}
        self.gateway = gateway
        self.model_id = model_id # 供 Compression 用的輕量或特化型號
    
    def create_memory(self, agent_id: str, name: str, personality: str, goals: str,
                      compression_interval: int = 6) -> SALMMemory:
        """初始化 SALM 記憶三層結構"""
        goal_list = [g.strip() for g in goals.split(";") if g.strip()]
        
        memory = SALMMemory(
            identity_core=f"姓名：{name}\n性格傾向：{personality}",
            goals=goal_list,
            compression_interval=compression_interval,
            long_term_summary="你剛在這個世界甦醒，尚未有值得記錄的過去經驗。"
        )
        self.memories[agent_id] = memory
        return memory
    
    async def add_experience(self, agent_id: str, experience: str):
        """將即時經歷塞入 Working Memory Ring"""
        mem = self.memories.get(agent_id)
        if not mem:
            return
            
        mem.short_term_buffer.append(experience)
        mem.steps_since_compression += 1
        mem.total_steps += 1
        
        # 觸發大腦睡眠整理 (Compression)
        if mem.steps_since_compression >= mem.compression_interval:
            await self._compress_and_reflect(agent_id)
            
    async def _compress_and_reflect(self, agent_id: str):
        """
        核心 SALM 壓縮算法：
        把 Working Memory 取出，利用 LLM 合併進 Long-Term Summary。
        這降低了 Context Window 壓力，是白皮書省 token 的第四大神器。
        """
        mem = self.memories[agent_id]
        
        # 把環狀區經歷倒出來
        experiences = list(mem.short_term_buffer)
        if not experiences:
            return
            
        experiences_text = "\n".join(f"- {m}" for m in experiences)
        
        prompt = f"""請以第一人稱視角，將以下「近期經歷」融入你的「舊有長期記憶」中。
必須極度精簡（不超過150字），保留情緒、關鍵事件與對他人的態度轉變。

【你的性格核心】: {mem.identity_core}
【舊有長期記憶】: {mem.long_term_summary}

【近期經歷】: 
{experiences_text}

請輸出更新後的「長期記憶」："""

        try:
            # Compression Task 可以用較低的 thinking level 即可
            # 這裡串接真實 Gateway 進行摘要
            response = await self.gateway.call(
                model_id=self.model_id, 
                prompt=prompt, 
                max_tokens=250,
                thinking_level="minimal" # 摘要求快求穩
            )
            
            mem.long_term_summary = response.strip()
            mem.total_compression_tokens_used += 300 # 估算
            logger.info(f"[{agent_id}] 記憶壓縮完成。新摘要長度: {len(mem.long_term_summary)}字")
            
        except Exception as e:
            logger.error(f"[{agent_id}] SALM 壓縮失敗: {e}")
            
        mem.steps_since_compression = 0
        
        # 壓縮完後，淨空工作記憶 (保留最新1~2條以防語境斷裂)
        while len(mem.short_term_buffer) > 1:
            mem.short_term_buffer.popleft()
            
    def get_prompt(self, agent_id: str) -> str:
        """組裝 SALM 用於 Agent 推理的 Prefix"""
        mem = self.memories[agent_id]
        goals_text = "- " + "\n- ".join(mem.goals) if mem.goals else "無特定人生目標"
        short_term_text = "\n".join(f"[{i+1}] {s}" for i, s in enumerate(mem.short_term_buffer))
        
        prompt = f"""--- [你的大腦結構 (SALM)] ---
<Identity Core>
{mem.identity_core}
我的目標:
{goals_text}
</Identity Core>

<Long-Term Memory Archive>
{mem.long_term_summary}
</Long-Term Memory Archive>

<Working Memory (Recent)>
{short_term_text if mem.short_term_buffer else "一片空白。"}
</Working Memory>
---------------------------------"""
        return prompt

    def get_all_stats(self) -> dict:
        """回報所有 Agent 記憶庫狀態供 Dashboard 顯示"""
        return {
            aid: {
                "total_steps": m.total_steps,
                "short_term_count": len(m.short_term_buffer),
                "long_term_length": len(m.long_term_summary),
                "compression_tokens": m.total_compression_tokens_used,
            }
            for aid, m in self.memories.items()
        }
