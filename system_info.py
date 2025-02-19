"""
System information collection module
"""

import psutil
import platform
from datetime import datetime

class SystemMonitor:
    """System monitoring class"""
    
    def __init__(self):
        self.system_info = self._get_system_info()
    
    def _get_system_info(self):
        """Get basic system information"""
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'hostname': platform.node(),
            'processor': platform.processor(),
        }
    
    def get_cpu_info(self):
        """Get CPU usage information"""
        cpu_freq = psutil.cpu_freq()
        return {
            'physical_cores': psutil.cpu_count(logical=False),
            'total_cores': psutil.cpu_count(logical=True),
            'max_frequency': round(cpu_freq.max, 2) if cpu_freq else 0,
            'current_frequency': round(cpu_freq.current, 2) if cpu_freq else 0,
            'cpu_usage': psutil.cpu_percent(interval=1)
        }
    
    def get_memory_info(self):
        """Get memory usage information"""
        memory = psutil.virtual_memory()
        return {
            'total': self._bytes_to_gb(memory.total),
            'available': self._bytes_to_gb(memory.available),
            'used': self._bytes_to_gb(memory.used),
            'percentage': memory.percent
        }
    
    def get_disk_info(self):
        """Get disk usage information"""
        disk = psutil.disk_usage('/')
        return {
            'total': self._bytes_to_gb(disk.total),
            'used': self._bytes_to_gb(disk.used),
            'free': self._bytes_to_gb(disk.free),
            'percentage': (disk.used / disk.total) * 100
        }
    
    def _bytes_to_gb(self, bytes_value):
        """Convert bytes to GB"""
        return round(bytes_value / (1024**3), 2)
    
    def get_all_info(self):
        """Get all system information"""
        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'system': self.system_info,
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info()
        }