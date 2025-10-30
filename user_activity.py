import json
import os
from typing import Dict, Set, Optional
from datetime import datetime
from collections import defaultdict

class UserActivity:
    def __init__(self, storage_file: str = 'user_activity.json'):
        self.storage_file = storage_file
        self.activity_data: Dict = {}
        self.blacklisted_users: Set[int] = set()
        self.blacklisted_hwids: Set[str] = set()
        self.load_data()
    
    def load_data(self) -> None:
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.activity_data = data.get('activity', {})
                    self.blacklisted_users = set(data.get('blacklisted_users', []))
                    self.blacklisted_hwids = set(data.get('blacklisted_hwids', []))
        except Exception as e:
            print(f"Error loading user activity data: {e}")
            self.activity_data = {}
            self.blacklisted_users = set()
            self.blacklisted_hwids = set()
    
    def save_data(self) -> None:
        try:
            data = {
                'activity': self.activity_data,
                'blacklisted_users': list(self.blacklisted_users),
                'blacklisted_hwids': list(self.blacklisted_hwids)
            }
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving user activity data: {e}")
    
    def log_activity(self, user_id: int, activity_type: str, details: Optional[str] = None) -> None:
        user_id_str = str(user_id)
        
        if user_id_str not in self.activity_data:
            self.activity_data[user_id_str] = {
                'total_activities': 0,
                'activities': []
            }
        
        activity_entry = {
            'type': activity_type,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details
        }
        
        self.activity_data[user_id_str]['activities'].append(activity_entry)
        self.activity_data[user_id_str]['total_activities'] += 1
        
        if len(self.activity_data[user_id_str]['activities']) > 100:
            self.activity_data[user_id_str]['activities'] = self.activity_data[user_id_str]['activities'][-100:]
        
        self.save_data()
    
    def get_user_activity(self, user_id: int) -> Dict:
        user_id_str = str(user_id)
        if user_id_str in self.activity_data:
            return self.activity_data[user_id_str]
        return {'total_activities': 0, 'activities': []}
    
    def is_blacklisted(self, user_id: int, hwid: Optional[str] = None) -> bool:
        if user_id in self.blacklisted_users:
            return True
        
        if hwid and hwid.upper() in self.blacklisted_hwids:
            return True
        
        return False
    
    def blacklist_user(self, user_id: int) -> bool:
        if user_id not in self.blacklisted_users:
            self.blacklisted_users.add(user_id)
            self.save_data()
            return True
        return False
    
    def unblacklist_user(self, user_id: int) -> bool:
        if user_id in self.blacklisted_users:
            self.blacklisted_users.remove(user_id)
            self.save_data()
            return True
        return False
    
    def blacklist_hwid(self, hwid: str) -> bool:
        hwid_upper = hwid.upper()
        if hwid_upper not in self.blacklisted_hwids:
            self.blacklisted_hwids.add(hwid_upper)
            self.save_data()
            return True
        return False
    
    def unblacklist_hwid(self, hwid: str) -> bool:
        hwid_upper = hwid.upper()
        if hwid_upper in self.blacklisted_hwids:
            self.blacklisted_hwids.remove(hwid_upper)
            self.save_data()
            return True
        return False
    
    def get_blacklist_data(self) -> Dict:
        return {
            'total_users': len(self.blacklisted_users),
            'total_hwids': len(self.blacklisted_hwids),
            'user_ids': list(self.blacklisted_users),
            'hwids': list(self.blacklisted_hwids)
        }
    
    def get_stats(self) -> Dict:
        total_users = len(self.activity_data)
        total_activities = sum(data['total_activities'] for data in self.activity_data.values())
        
        return {
            'total_users': total_users,
            'total_activities': total_activities,
            'blacklisted_users': len(self.blacklisted_users),
            'blacklisted_hwids': len(self.blacklisted_hwids)
        }
