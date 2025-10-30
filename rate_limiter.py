import time
from collections import defaultdict, deque
from typing import Dict, Deque

class RateLimiter:
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.user_requests: Dict[int, Deque[float]] = defaultdict(deque)
    
    def is_rate_limited(self, user_id: int) -> bool:
        current_time = time.time()
        user_queue = self.user_requests[user_id]
        
        while user_queue and current_time - user_queue[0] > self.time_window:
            user_queue.popleft()
        
        if len(user_queue) >= self.max_requests:
            return True
        
        user_queue.append(current_time)
        return False
    
    def get_remaining_requests(self, user_id: int) -> int:
        current_time = time.time()
        user_queue = self.user_requests[user_id]
        
        while user_queue and current_time - user_queue[0] > self.time_window:
            user_queue.popleft()
        
        return max(0, self.max_requests - len(user_queue))
    
    def get_reset_time(self, user_id: int) -> float:
        user_queue = self.user_requests[user_id]
        
        if not user_queue:
            return 0
        
        oldest_request = user_queue[0]
        reset_time = oldest_request + self.time_window
        
        return max(0, reset_time - time.time())
    
    def reset_user(self, user_id: int) -> bool:
        if user_id in self.user_requests:
            del self.user_requests[user_id]
            return True
        return False
    
    def get_stats(self) -> dict:
        return {
            'max_requests': self.max_requests,
            'time_window': self.time_window,
            'tracked_users': len(self.user_requests)
        }
