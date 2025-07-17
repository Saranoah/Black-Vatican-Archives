#!/usr/bin/env python3
"""
📊 LOG ANALYZER - Resurrect insights from the digital dead
Analyzes log files for patterns, errors, and anomalies
"""

import re
import json
from collections import Counter, defaultdict
from datetime import datetime
import matplotlib.pyplot as plt

class LogNecromancer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.entries = []
        self.patterns = {
            'ip': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'timestamp': r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
            'error': r'ERROR|FATAL|CRITICAL',
            'warning': r'WARN|WARNING',
            'status_code': r'\s([1-5]\d{2})\s'
        }
    
    def resurrect_logs(self):
        """Read and parse log entries"""
        print("🔮 Resurrecting log entries...")
        try:
            with open(self.log_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    entry = {
                        'line_number': line_num,
                        'raw': line.strip(),
                        'timestamp': self.extract_pattern(line, 'timestamp'),
                        'ip': self.extract_pattern(line, 'ip'),
                        'status_code': self.extract_pattern(line, 'status_code'),
                        'has_error': bool(re.search(self.patterns['error'], line)),
                        'has_warning': bool(re.search(self.patterns['warning'], line))
                    }
                    self.entries.append(entry)
            print(f"💀 Resurrected {len(self.entries)} log entries")
        except FileNotFoundError:
            print(f"🚫 Log file not found: {self.log_file}")
    
    def extract_pattern(self, text, pattern_name):
        """Extract specific patterns from log line"""
        match = re.search(self.patterns[pattern_name], text)
        return match.group() if match else None
    
    def analyze_dark_patterns(self):
        """Analyze log patterns for insights"""
        print("📊 Analyzing dark patterns...")
        
        # IP frequency analysis
        ips = [entry['ip'] for entry in self.entries if entry['ip']]
        ip_counter = Counter(ips)
        
        # Error analysis
        errors = sum(1 for entry in self.entries if entry['has_error'])
        warnings = sum(1 for entry in self.entries if entry['has_warning'])
        
        # Status code analysis
        status_codes = [entry['status_code'] for entry in self.entries if entry['status_code']]
        status_counter = Counter(status_codes)
        
        report = {
            'total_entries': len(self.entries),
            'unique_ips': len(ip_counter),
            'top_ips': ip_counter.most_common(10),
            'error_count': errors,
            'warning_count': warnings,
            'status_codes': dict(status_counter),
            'error_rate': (errors / len(self.entries)) * 100 if self.entries else 0
        }
        
        return report
    
    def generate_dark_report(self):
        """Generate comprehensive analysis report"""
        report = self.analyze_dark_patterns()
        
        print("💀" * 50)
        print("         NECROMANCY REPORT")
        print("💀" * 50)
        print(f"📊 Total Entries: {report['total_entries']}")
        print(f"🌐 Unique IPs: {report['unique_ips']}")
        print(f"❌ Errors: {report['error_count']}")
        print(f"⚠️ Warnings: {report['warning_count']}")
        print(f"📈 Error Rate: {report['error_rate']:.2f}%")
        print("\n🔥 Top IPs:")
        for ip, count in report['top_ips']:
            print(f"   {ip}: {count} requests")
        
        # Save detailed report
        with open('necromancy_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print("\n💾 Detailed report saved to necromancy_report.json")

if __name__ == "__main__":
    log_file = input("📂 Enter log file path: ")
    necromancer = LogNecromancer(log_file)
    necromancer.resurrect_logs()
    necromancer.generate_dark_report()
