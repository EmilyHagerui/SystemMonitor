# SystemMonitor

A lightweight system monitoring tool built with Python.

## Features

- Monitor CPU, Memory, Disk, and Network usage
- Real-time system statistics
- Configurable alert system with thresholds
- Simple command-line interface with multiple options
- JSON-based configuration management
- Color-coded alerts and notifications

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic monitoring (continuous):
```bash
python monitor.py
```

### Show system info once:
```bash
python monitor.py --once
```

### Custom update interval:
```bash
python monitor.py --interval 5
```

### Command line options:
```bash
python monitor.py --help
```

Available options:
- `-o, --once`: Show system information once and exit
- `-i, --interval`: Set update interval in seconds (default: 3)
- `-v, --version`: Show version information
- `-h, --help`: Show help message

## Requirements

- Python 3.7+
- psutil

## License

MIT License