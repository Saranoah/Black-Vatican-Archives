#!/usr/bin/env python3
"""
🔥 SOUL MONITOR - Track the life force of your machine
Monitors CPU, Memory, Disk, and Network usage in real-time with dark aesthetics
"""

import psutil
import time
import os
import sys
from datetime import datetime
from typing import Dict, Any

class SoulMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()
        
    def get_system_vitals(self) -> Dict[str, Any]:
        """Extract the essence of system performance"""
        # Calculate network rates
        current_net_io = psutil.net_io_counters()
        current_time = time.time()
        time_diff = current_time - self.last_net_time
        
        net_stats = {
            'bytes_sent': current_net_io.bytes_sent,
            'bytes_recv': current_net_io.bytes_recv,
            'sent_rate': (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / time_diff,
            'recv_rate': (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / time_diff
        }
        
        self.last_net_io = current_net_io
        self.last_net_time = current_time
        
        # Get process count by status
        process_status = {}
        for proc in psutil.process_iter(['status']):
            status = proc.info['status']
            process_status[status] = process_status.get(status, 0) + 1
        
        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'cores': psutil.cpu_count(),
                'freq': psutil.cpu_freq().current if hasattr(psutil, 'cpu_freq') else 0
            },
            'memory': psutil.virtual_memory()._asdict(),
            'disk': psutil.disk_usage('/')._asdict(),
            'network': net_stats,
            'processes': {
                'total': len(psutil.pids()),
                'by_status': process_status
            },
            'uptime': time.time() - psutil.boot_time(),
            'soul_pressure': self.calculate_soul_pressure()
        }
    
    def calculate_soul_pressure(self) -> float:
        """Calculate a mystical 'soul pressure' metric"""
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        disk = psutil.disk_usage('/')
        
        # Weighted average of system metrics
        return (cpu * 0.4 + mem.percent * 0.3 + disk.percent * 0.3) / 100
    
    def dark_display(self, vitals: Dict[str, Any]):
        """Display system vitals in dark terminal format"""
        # Clear screen with cross-platform support
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Terminal colors for dark theme
        class Colors:
            RED = '\033[31m'
            GREEN = '\033[32m'
            YELLOW = '\033[33m'
            BLUE = '\033[34m'
            MAGENTA = '\033[35m'
            CYAN = '\033[36m'
            WHITE = '\033[37m'
            RESET = '\033[0m'
        
        # Header with timestamp
        print(f"{Colors.RED}🔥" * 50 + Colors.RESET)
        print(f"{Colors.MAGENTA}       SOUL MONITOR - SYSTEM VITALS {vitals['timestamp']}")
        print(f"{Colors.RED}🔥" * 50 + Colors.RESET)
        
        # CPU Section
        cpu_color = Colors.RED if vitals['cpu']['percent'] > 80 else Colors.YELLOW if vitals['cpu']['percent'] > 50 else Colors.GREEN
        print(f"{Colors.WHITE}💀 CPU: {cpu_color}{vitals['cpu']['percent']:.1f}%{Colors.WHITE} ({vitals['cpu']['cores']} cores, {vitals['cpu']['freq']:.0f} MHz){Colors.RESET}")
        
        # Memory Section
        mem = vitals['memory']
        mem_color = Colors.RED if mem['percent'] > 80 else Colors.YELLOW if mem['percent'] > 50 else Colors.GREEN
        print(f"{Colors.WHITE}🧠 Memory: {mem_color}{mem['percent']:.1f}%{Colors.WHITE} used ({mem['used']/1024/1024:.1f} MB / {mem['total']/1024/1024:.1f} MB){Colors.RESET}")
        
        # Disk Section
        disk = vitals['disk']
        disk_color = Colors.RED if disk['percent'] > 80 else Colors.YELLOW if disk['percent'] > 50 else Colors.GREEN
        print(f"{Colors.WHITE}💽 Disk: {disk_color}{disk['percent']:.1f}%{Colors.WHITE} used ({disk['used']/1024/1024/1024:.1f} GB / {disk['total']/1024/1024/1024:.1f} GB){Colors.RESET}")
        
        # Network Section
        net = vitals['network']
        print(f"{Colors.WHITE}🌐 Network: {Colors.CYAN}▲ {net['sent_rate']/1024:.1f} KB/s{Colors.WHITE} | {Colors.BLUE}▼ {net['recv_rate']/1024:.1f} KB/s{Colors.RESET}")
        
        # Processes Section
        print(f"{Colors.WHITE}⚡ Processes: {vitals['processes']['total']} souls (", end="")
        for status, count in vitals['processes']['by_status'].items():
            print(f"{count} {status}, ", end="")
        print("\b\b)" + Colors.RESET)
        
        # Soul Pressure Gauge
        pressure = vitals['soul_pressure']
        pressure_color = Colors.RED if pressure > 0.8 else Colors.YELLOW if pressure > 0.5 else Colors.GREEN
        gauge = "[" + "█" * int(pressure * 20) + " " * (20 - int(pressure * 20)) + "]"
        print(f"{Colors.WHITE}🖤 Soul Pressure: {pressure_color}{gauge} {pressure*100:.1f}%{Colors.RESET}")
        
        # Footer
        print(f"{Colors.WHITE}⏰ Uptime: {vitals['uptime']/3600:.1f} hours")
        print(f"{Colors.RED}🔥" * 50 + Colors.RESET)

if __name__ == "__main__":
    monitor = SoulMonitor()
    try:
        while True:
            vitals = monitor.get_system_vitals()
            monitor.dark_display(vitals)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n💀 Soul monitoring terminated...")
    except Exception as e:
        print(f"\n☠️ Critical soul failure: {e}")
        sys.exit(1)
