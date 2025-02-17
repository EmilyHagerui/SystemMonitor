#!/usr/bin/env python3
"""
SystemMonitor - A lightweight system monitoring tool
"""

import time
import sys

def main():
    """Main entry point"""
    print("SystemMonitor v0.1.0")
    print("Starting system monitoring...")
    
    try:
        while True:
            # TODO: Add monitoring logic here
            print("Monitoring... (Press Ctrl+C to exit)")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()