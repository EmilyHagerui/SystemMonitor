"""
Configuration management module
"""

import json
import os
from typing import Dict, Any

class Config:
    """Configuration manager"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.default_config = {
            "monitor": {
                "update_interval": 3,
                "auto_clear_screen": True,
                "show_system_info": True,
                "show_cpu_info": True,
                "show_memory_info": True,
                "show_disk_info": True
            },
            "display": {
                "use_colors": True,
                "use_emojis": True,
                "precision": 2
            },
            "alerts": {
                "enabled": False,
                "cpu_threshold": 80,
                "memory_threshold": 85,
                "disk_threshold": 90
            }
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                # Merge with defaults to ensure all keys exist
                config = self.default_config.copy()
                self._deep_update(config, loaded_config)
                return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")
                print("Using default configuration")
                return self.default_config.copy()
        else:
            # Create default config file
            self.save_config(self.default_config)
            return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any] = None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save config file: {e}")
    
    def get(self, key_path: str, default=None):
        """Get configuration value using dot notation (e.g., 'monitor.update_interval')"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key_path.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
    
    def _deep_update(self, base_dict: Dict, update_dict: Dict):
        """Recursively update nested dictionary"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def reset_to_default(self):
        """Reset configuration to default values"""
        self.config = self.default_config.copy()
        self.save_config()
    
    def get_monitor_config(self):
        """Get monitor-specific configuration"""
        return self.config.get('monitor', {})
    
    def get_display_config(self):
        """Get display-specific configuration"""
        return self.config.get('display', {})
    
    def get_alerts_config(self):
        """Get alerts-specific configuration"""
        return self.config.get('alerts', {})