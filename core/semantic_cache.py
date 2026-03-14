"""基於語意相似度的快取系統"""
import hashlib
from typing import Optional

class SemanticCache:
    """
    基於語意相似度的快取系統。
    使用 prompt 的 hash 做精確匹配，加上簡易語意匹配。
    """
    
    def __init__(self, max_size: int = 500, similarity_threshold: float = 0.92):
        self.cache: dict[str, dict] = {}  # hash -> {prompt, response, features}
        self.max_size = max_size
        self.threshold = similarity_threshold
    
    def _hash_prompt(self, prompt: str) -> str:
        """精確匹配用的 hash"""
        return hashlib.md5(prompt.encode()).hexdigest()
    
    def _extract_key_features(self, prompt: str) -> set[str]:
        """簡易語意特徵提取"""
        keywords = set()
        role_markers = ["農民", "商人", "士兵", "工匠", "漁夫", "牧師", "farmer", "merchant"]
        event_markers = ["漲價", "戰爭", "疾病", "慶典", "稅收", "盜匪"]
        mood_markers = ["害怕", "開心", "生氣", "焦慮", "平靜"]
        
        for marker_list in [role_markers, event_markers, mood_markers]:
            for marker in marker_list:
                if marker in prompt:
                    keywords.add(marker)
        
        return keywords
    
    def _similarity(self, features_a: set, features_b: set) -> float:
        """Jaccard 相似度"""
        if not features_a or not features_b:
            return 0.0
        intersection = features_a & features_b
        union = features_a | features_b
        return len(intersection) / len(union)
    
    def get(self, prompt: str) -> Optional[str]:
        """查找快取，先精確匹配，再語意匹配"""
        h = self._hash_prompt(prompt)
        if h in self.cache:
            return self.cache[h]["response"]
        
        query_features = self._extract_key_features(prompt)
        best_match = None
        best_similarity = 0
        
        for cached in self.cache.values():
            sim = self._similarity(query_features, cached["features"])
            if sim > best_similarity:
                best_similarity = sim
                best_match = cached
        
        if best_match and best_similarity >= self.threshold:
            return best_match["response"]
        
        return None  # Cache miss
    
    def put(self, prompt: str, response: str):
        """存入快取"""
        if len(self.cache) >= self.max_size:
            oldest = next(iter(self.cache))
            del self.cache[oldest]
        
        h = self._hash_prompt(prompt)
        self.cache[h] = {
            "prompt": prompt,
            "response": response,
            "features": self._extract_key_features(prompt),
        }
