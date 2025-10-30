import hashlib
import json
import os
from typing import Optional, Set

class HWIDService:
    def __init__(self, storage_file: str = 'hwid_data.json'):
        self.storage_file = storage_file
        self.registered_hwids: dict = {}
        self.load_data()
    
    def load_data(self) -> None:
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.registered_hwids = {int(k): v for k, v in data.items()}
        except Exception as e:
            print(f"Error loading HWID data: {e}")
            self.registered_hwids = {}
    
    def save_data(self) -> None:
        try:
            with open(self.storage_file, 'w') as f:
                json.dump({str(k): v for k, v in self.registered_hwids.items()}, f, indent=2)
        except Exception as e:
            print(f"Error saving HWID data: {e}")
    
    def generate_hwid(self, user_id: int, additional_data: str = "") -> str:
        data_string = f"{user_id}:{additional_data}:{os.urandom(16).hex()}"
        return hashlib.sha256(data_string.encode()).hexdigest()[:32].upper()
    
    def register_hwid(self, user_id: int, hwid: Optional[str] = None) -> str:
        if hwid is None:
            hwid = self.generate_hwid(user_id)
        
        self.registered_hwids[user_id] = {
            'hwid': hwid,
            'registered_at': str(os.times())
        }
        self.save_data()
        return hwid
    
    def get_hwid(self, user_id: int) -> Optional[str]:
        if user_id in self.registered_hwids:
            return self.registered_hwids[user_id]['hwid']
        return None
    
    def verify_hwid(self, user_id: int, hwid: str) -> bool:
        stored_hwid = self.get_hwid(user_id)
        if stored_hwid is None:
            return False
        return stored_hwid.upper() == hwid.upper()
    
    def remove_hwid(self, user_id: int) -> bool:
        if user_id in self.registered_hwids:
            del self.registered_hwids[user_id]
            self.save_data()
            return True
        return False
    
    def get_stats(self) -> dict:
        return {
            'total_registered': len(self.registered_hwids),
            'storage_file': self.storage_file
        }
