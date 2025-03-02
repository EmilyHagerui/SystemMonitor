#!/usr/bin/env python3
"""
SystemMonitor - A lightweight system monitoring tool
"""

import time
import sys
import os
import argparse
from system_info import SystemMonitor
from config import Config
from alerts import AlertManager

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_info(info, alerts=None):
    """Display system information"""
    print(f"=== System Monitor - {info['timestamp']} ===\n")
    
    # Show alerts first if any
    if alerts:
        print("🚨 ALERTS:")
        for alert in alerts:
            print(f"   {alert}")
        print()
    
    # System Info
    print("💻 System Information:")
    print(f"   Platform: {info['system']['platform']} {info['system']['platform_release']}")
    print(f"   Hostname: {info['system']['hostname']}")
    
    # CPU Info
    print(f"\n🔧 CPU Information:")
    print(f"   Cores: {info['cpu']['physical_cores']} physical, {info['cpu']['total_cores']} logical")
    print(f"   Usage: {info['cpu']['cpu_usage']}%")
    if info['cpu']['current_frequency'] > 0:
        print(f"   Frequency: {info['cpu']['current_frequency']} MHz")
    
    # Memory Info
    print(f"\n💾 Memory Information:")
    print(f"   Total: {info['memory']['total']} GB")
    print(f"   Used: {info['memory']['used']} GB ({info['memory']['percentage']}%)")
    print(f"   Available: {info['memory']['available']} GB")
    
    # Disk Info
    print(f"\n💽 Disk Information:")
    print(f"   Total: {info['disk']['total']} GB")
    print(f"   Used: {info['disk']['used']} GB ({info['disk']['percentage']:.1f}%)")
    print(f"   Free: {info['disk']['free']} GB")
    
    print(f"\n{'='*50}")
    print("Press Ctrl+C to exit...")

def display_once(info):
    """Display system information once"""
    print(f"=== System Monitor - {info['timestamp']} ===\n")
    
    # System Info
    print("💻 System Information:")
    print(f"   Platform: {info['system']['platform']} {info['system']['platform_release']}")
    print(f"   Hostname: {info['system']['hostname']}")
    print(f"   Architecture: {info['system']['architecture']}")
    
    # CPU Info
    print(f"\n🔧 CPU Information:")
    print(f"   Physical Cores: {info['cpu']['physical_cores']}")
    print(f"   Total Cores: {info['cpu']['total_cores']}")
    print(f"   CPU Usage: {info['cpu']['cpu_usage']}%")
    if info['cpu']['current_frequency'] > 0:
        print(f"   Current Frequency: {info['cpu']['current_frequency']} MHz")
        print(f"   Max Frequency: {info['cpu']['max_frequency']} MHz")
    
    # Memory Info
    print(f"\n💾 Memory Information:")
    print(f"   Total: {info['memory']['total']} GB")
    print(f"   Used: {info['memory']['used']} GB ({info['memory']['percentage']}%)")
    print(f"   Available: {info['memory']['available']} GB")
    
    # Disk Info
    print(f"\n💽 Disk Information:")
    print(f"   Total: {info['disk']['total']} GB")
    print(f"   Used: {info['disk']['used']} GB ({info['disk']['percentage']:.1f}%)")
    print(f"   Free: {info['disk']['free']} GB")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='SystemMonitor - A lightweight system monitoring tool')
    parser.add_argument('-o', '--once', action='store_true', 
                        help='Show system info once and exit')
    parser.add_argument('-i', '--interval', type=int, default=3,
                        help='Update interval in seconds (default: 3)')
    parser.add_argument('-v', '--version', action='version', version='SystemMonitor v0.4.0')
    return parser.parse_args()

def main():
    """Main entry point"""
    args = parse_arguments()
    
    print("SystemMonitor v0.4.0")
    print("Initializing...")
    
    # Load configuration
    config = Config()
    monitor = SystemMonitor()
    alert_manager = AlertManager(config)
    
    # Use config values if args not provided
    interval = args.interval if args.interval != 3 else config.get('monitor.update_interval', 3)
    
    try:
        if args.once:
            # Show info once and exit
            info = monitor.get_all_info()
            alerts = alert_manager.check_alerts(info)
            formatted_alerts = [alert_manager.format_alert(alert) for alert in alerts]
            display_once(info)
            if alerts:
                print("\n🚨 Current Alerts:")
                for alert in formatted_alerts:
                    print(f"   {alert}")
        else:
            # Continuous monitoring
            alerts_enabled = config.get('alerts.enabled', False)
            print(f"Update interval: {interval} seconds")
            print(f"Alerts: {'Enabled' if alerts_enabled else 'Disabled'}")
            print()
            
            while True:
                clear_screen()
                info = monitor.get_all_info()
                
                # Check for alerts
                alerts = alert_manager.check_alerts(info)
                formatted_alerts = [alert_manager.format_alert(alert) for alert in alerts]
                
                display_info(info, formatted_alerts if alerts else None)
                time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()