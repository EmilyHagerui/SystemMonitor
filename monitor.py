#!/usr/bin/env python3
"""
SystemMonitor - A lightweight system monitoring tool
"""

import time
import sys
import os
from system_info import SystemMonitor

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_info(info):
    """Display system information"""
    print(f"=== System Monitor - {info['timestamp']} ===\n")
    
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

def main():
    """Main entry point"""
    print("SystemMonitor v0.2.0")
    print("Initializing...")
    
    monitor = SystemMonitor()
    
    try:
        while True:
            clear_screen()
            info = monitor.get_all_info()
            display_info(info)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()