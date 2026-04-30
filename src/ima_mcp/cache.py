import os
import json
import time
from typing import Any, Optional, Dict

class Cache:
    """缓存机制"""
    
    def __init__(self, cache_dir="~/.cache/ima_mcp", max_size=100, expiry=3600):
        """初始化缓存
        
        Args:
            cache_dir: 缓存目录
            max_size: 最大缓存条目数
            expiry: 缓存过期时间（秒）
        """
        self.cache_dir = os.path.expanduser(cache_dir)
        self.max_size = max_size
        self.expiry = expiry
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        
        # 创建缓存目录
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 加载文件缓存
        self._load_cache()
    
    def _load_cache(self):
        """加载文件缓存"""
        cache_file = os.path.join(self.cache_dir, "cache.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if not self._is_expired(value.get("timestamp", 0)):
                            self.memory_cache[key] = value
            except Exception:
                pass
    
    def _save_cache(self):
        """保存缓存到文件"""
        cache_file = os.path.join(self.cache_dir, "cache.json")
        # 只保存未过期的缓存
        valid_cache = {k: v for k, v in self.memory_cache.items() if not self._is_expired(v.get("timestamp", 0))}
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(valid_cache, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def _is_expired(self, timestamp: int) -> bool:
        """检查缓存是否过期"""
        return time.time() - timestamp > self.expiry
    
    def _clean_expired(self):
        """清理过期缓存"""
        expired_keys = [k for k, v in self.memory_cache.items() if self._is_expired(v.get("timestamp", 0))]
        for key in expired_keys:
            del self.memory_cache[key]
    
    def _ensure_cache_size(self):
        """确保缓存大小不超过限制"""
        if len(self.memory_cache) > self.max_size:
            # 按时间戳排序，删除最旧的缓存
            sorted_keys = sorted(self.memory_cache.keys(), key=lambda k: self.memory_cache[k].get("timestamp", 0))
            for key in sorted_keys[:len(self.memory_cache) - self.max_size]:
                del self.memory_cache[key]
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存
        
        Args:
            key: 缓存键
            
        Returns:
            缓存的值，如果不存在或已过期则返回 None
        """
        # 清理过期缓存
        self._clean_expired()
        
        if key in self.memory_cache:
            item = self.memory_cache[key]
            if not self._is_expired(item.get("timestamp", 0)):
                return item.get("value")
            else:
                del self.memory_cache[key]
                self._save_cache()
        return None
    
    def set(self, key: str, value: Any):
        """设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        # 清理过期缓存
        self._clean_expired()
        
        # 设置缓存
        self.memory_cache[key] = {
            "value": value,
            "timestamp": int(time.time())
        }
        
        # 确保缓存大小
        self._ensure_cache_size()
        
        # 保存到文件
        self._save_cache()
    
    def delete(self, key: str):
        """删除缓存
        
        Args:
            key: 缓存键
        """
        if key in self.memory_cache:
            del self.memory_cache[key]
            self._save_cache()
    
    def clear(self):
        """清空缓存"""
        self.memory_cache.clear()
        self._save_cache()
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在且未过期
        
        Args:
            key: 缓存键
            
        Returns:
            是否存在且未过期
        """
        if key in self.memory_cache:
            return not self._is_expired(self.memory_cache[key].get("timestamp", 0))
        return False

# 创建全局缓存实例
cache = Cache()
