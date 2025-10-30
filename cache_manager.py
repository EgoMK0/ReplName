import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, ttl_minutes: int = 30):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_minutes * 60
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        if key not in self.cache:
            return None
        
        cache_entry = self.cache[key]
        
        if time.time() - cache_entry['timestamp'] > self.ttl_seconds:
            del self.cache[key]
            return None
        
        return cache_entry['data']
    
    def set(self, key: str, data: Dict[str, Any]) -> None:
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def delete(self, key: str) -> bool:
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self) -> int:
        count = len(self.cache)
        self.cache.clear()
        return count
    
    def cleanup_expired(self) -> int:
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.cache.items():
            if current_time - entry['timestamp'] > self.ttl_seconds:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        current_time = time.time()
        active_entries = 0
        expired_entries = 0
        
        for entry in self.cache.values():
            if current_time - entry['timestamp'] <= self.ttl_seconds:
                active_entries += 1
            else:
                expired_entries += 1
        
        return {
            'total_entries': len(self.cache),
            'active_entries': active_entries,
            'expired_entries': expired_entries,
            'ttl_seconds': self.ttl_seconds
        }
