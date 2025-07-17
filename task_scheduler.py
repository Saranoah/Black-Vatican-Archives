#!/usr/bin/env python3
"""
⏰ TASK SCHEDULER - Automate rituals at predetermined times
Schedule and execute tasks with dark magic precision
"""

import schedule
import time
import subprocess
import json
from datetime import datetime
import logging

class TaskScheduler:
    def __init__(self):
        self.tasks = []
        self.setup_logging()
        
    def setup_logging(self):
        """Setup dark logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - 🔮 %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scheduler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def add_ritual(self, name, command, schedule_time, repeat=True):
        """Add a new automated ritual"""
        task = {
            'name': name,
            'command': command,
            'schedule_time': schedule_time,
            'repeat': repeat,
            'last_run': None,
            'run_count': 0
        }
        self.tasks.append(task)
        self.logger.info(f"🔮 Added ritual: {name}")
    
    def execute_ritual(self, task):
        """Execute a scheduled ritual"""
        try:
            self.logger.info(f"⚡ Executing ritual: {task['name']}")
            result = subprocess.run(
                task['command'],
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            task['last_run'] = datetime.now().isoformat()
            task['run_count'] += 1
            
            if result.returncode == 0:
                self.logger.info(f"✅ Ritual completed: {task['name']}")
            else:
                self.logger.error(f"❌ Ritual failed: {task['name']} - {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"⏰ Ritual timeout: {task['name']}")
        except Exception as e:
            self.logger.error(f"💀 Ritual error: {task['name']} - {str(e)}")
    
    def start_dark_scheduler(self):
        """Begin the automated ritual cycle"""
        self.logger.info("🌙 Starting dark scheduler...")
        
        # Schedule tasks
        for task in self.tasks:
            if task['repeat']:
                schedule.every().day.at(task['schedule_time']).do(
                    self.execute_ritual, task
                )
            
        self.logger.info(f"📅 Scheduled {len(self.tasks)} rituals")
        
        # Main scheduler loop
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

# Example usage
if __name__ == "__main__":
    scheduler = TaskScheduler()
    
    # Add some example rituals
    scheduler.add_ritual(
        "System Backup",
        "tar -czf /backup/system_$(date +%Y%m%d).tar.gz /home",
        "03:00"
    )
    
    scheduler.add_ritual(
        "Log Cleanup",
        "find /var/log -name '*.log' -mtime +30 -delete",
        "02:00"
    )
    
    scheduler.add_ritual(
        "Security Scan",
        "python3 /scripts/security_scan.py",
        "04:00"
    )
    
    scheduler.start_dark_scheduler()
