"""
System alerts and notifications module
"""

import time
from typing import Dict, List, Any
from datetime import datetime

class AlertManager:
    """Manage system alerts and notifications"""
    
    def __init__(self, config):
        self.config = config
        self.alert_history = []
        self.last_alert_time = {}
        self.cooldown_period = 60  # 60 seconds between same type alerts
        
    def check_alerts(self, system_info: Dict[str, Any]) -> List[Dict[str, str]]:
        """Check system metrics against thresholds and return alerts"""
        alerts = []
        alerts_config = self.config.get_alerts_config()
        
        if not alerts_config.get('enabled', False):
            return alerts
        
        current_time = time.time()
        
        # Check CPU usage
        cpu_usage = system_info['cpu']['cpu_usage']
        cpu_threshold = alerts_config.get('cpu_threshold', 80)
        if cpu_usage > cpu_threshold:
            alert_key = 'cpu_high'
            if self._should_send_alert(alert_key, current_time):
                alerts.append({
                    'type': 'warning',
                    'category': 'CPU',
                    'message': f'High CPU usage: {cpu_usage}% (threshold: {cpu_threshold}%)',
                    'value': cpu_usage,
                    'threshold': cpu_threshold,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                self.last_alert_time[alert_key] = current_time
        
        # Check memory usage
        memory_usage = system_info['memory']['percentage']
        memory_threshold = alerts_config.get('memory_threshold', 85)
        if memory_usage > memory_threshold:
            alert_key = 'memory_high'
            if self._should_send_alert(alert_key, current_time):
                alerts.append({
                    'type': 'warning',
                    'category': 'Memory',
                    'message': f'High memory usage: {memory_usage}% (threshold: {memory_threshold}%)',
                    'value': memory_usage,
                    'threshold': memory_threshold,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                self.last_alert_time[alert_key] = current_time
        
        # Check disk usage
        disk_usage = system_info['disk']['percentage']
        disk_threshold = alerts_config.get('disk_threshold', 90)
        if disk_usage > disk_threshold:
            alert_key = 'disk_high'
            if self._should_send_alert(alert_key, current_time):
                alerts.append({
                    'type': 'critical',
                    'category': 'Disk',
                    'message': f'High disk usage: {disk_usage:.1f}% (threshold: {disk_threshold}%)',
                    'value': disk_usage,
                    'threshold': disk_threshold,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                self.last_alert_time[alert_key] = current_time
        
        # Store alerts in history
        for alert in alerts:
            self.alert_history.append(alert)
            # Keep only last 50 alerts
            if len(self.alert_history) > 50:
                self.alert_history.pop(0)
        
        return alerts
    
    def _should_send_alert(self, alert_key: str, current_time: float) -> bool:
        """Check if enough time has passed since last alert of this type"""
        if alert_key not in self.last_alert_time:
            return True
        
        time_since_last = current_time - self.last_alert_time[alert_key]
        return time_since_last >= self.cooldown_period
    
    def get_alert_history(self) -> List[Dict[str, str]]:
        """Get alert history"""
        return self.alert_history.copy()
    
    def clear_alert_history(self):
        """Clear alert history"""
        self.alert_history.clear()
        self.last_alert_time.clear()
    
    def format_alert(self, alert: Dict[str, str]) -> str:
        """Format alert for display"""
        alert_type = alert['type']
        category = alert['category']
        message = alert['message']
        timestamp = alert['timestamp']
        
        # Color coding based on alert type
        if alert_type == 'critical':
            color_code = '\033[91m'  # Red
            emoji = '🚨'
        elif alert_type == 'warning':
            color_code = '\033[93m'  # Yellow
            emoji = '⚠️ '
        else:
            color_code = '\033[96m'  # Cyan
            emoji = 'ℹ️ '
        
        reset_code = '\033[0m'
        
        return f"{color_code}{emoji} [{timestamp}] {category}: {message}{reset_code}"