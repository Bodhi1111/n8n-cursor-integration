#!/usr/bin/env python3
"""
BMAD-METHOD Auto Monitor for Estate Planning Transcripts
Watches for new transcripts and triggers automated processing
"""

import os
import time
import json
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BMADTranscriptHandler(FileSystemEventHandler):
    """Handles new transcript files with BMAD-METHOD processing"""

    def __init__(self, n8n_webhook_url, config_file="baserow_config.json"):
        self.n8n_webhook_url = n8n_webhook_url
        self.processed_files = set()
        self.load_config(config_file)

    def load_config(self, config_file):
        """Load Baserow configuration"""
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
            print(f"✅ Loaded config from {config_file}")
        except FileNotFoundError:
            print(f"⚠️ Config file {config_file} not found - using defaults")
            self.config = {}

    def on_created(self, event):
        """Handle new file creation"""
        if not event.is_directory and event.src_path.endswith('.txt'):
            self.process_new_transcript(event.src_path)

    def on_modified(self, event):
        """Handle file modifications (for synced files)"""
        if not event.is_directory and event.src_path.endswith('.txt'):
            # Avoid duplicate processing
            if event.src_path not in self.processed_files:
                time.sleep(2)  # Wait for file to be fully written
                self.process_new_transcript(event.src_path)

    def process_new_transcript(self, file_path):
        """Process new transcript with BMAD-METHOD"""
        file_path = Path(file_path)

        # Skip if already processed or too small
        if str(file_path) in self.processed_files or file_path.stat().st_size < 100:
            return

        print(f"\n🎯 BMAD-METHOD: New transcript detected")
        print(f"📄 File: {file_path.name}")
        print(f"📊 Size: {file_path.stat().st_size} bytes")
        print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")

        try:
            # Trigger n8n workflow
            payload = {
                "file_path": str(file_path),
                "filename": file_path.name,
                "triggered_by": "bmad_auto_monitor",
                "timestamp": datetime.now().isoformat()
            }

            response = requests.post(
                self.n8n_webhook_url,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                print(f"✅ BMAD processing triggered successfully")
                self.processed_files.add(str(file_path))

                # Log processing
                self.log_processing(file_path, "triggered")

            else:
                print(f"❌ Failed to trigger processing: {response.status_code}")

        except requests.RequestException as e:
            print(f"❌ Network error triggering processing: {e}")
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")

    def log_processing(self, file_path, status):
        """Log processing activity"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "file": str(file_path),
            "status": status,
            "size": file_path.stat().st_size
        }

        # Append to processing log
        with open("bmad_processing.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

class BMADAutoMonitor:
    """Main monitoring service for BMAD-METHOD automation"""

    def __init__(self):
        self.transcript_dir = "/Users/joshuavaughan/Documents/McAdams Transcripts"
        self.n8n_url = "http://localhost:5678"
        self.webhook_url = f"{self.n8n_url}/webhook/bmad-estate-planning"
        self.observer = None

    def check_services(self):
        """Verify required services are running"""
        services = {
            "n8n": "http://localhost:5678",
            "Baserow": "http://localhost",
            "Ollama": "http://localhost:11434"
        }

        print("🔍 Checking BMAD-METHOD services...")
        for name, url in services.items():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code in [200, 404]:
                    print(f"✅ {name} is running")
                else:
                    print(f"⚠️ {name} responded with {response.status_code}")
            except requests.RequestException:
                print(f"❌ {name} is not accessible")
                return False

        return True

    def setup_webhook(self):
        """Setup n8n webhook if not exists"""
        # This would typically be done through n8n UI
        # For now, just verify the webhook endpoint
        print(f"🔗 Webhook endpoint: {self.webhook_url}")
        print("ℹ️ Ensure your n8n workflow has a webhook trigger at this URL")

    def start_monitoring(self):
        """Start the file monitoring service"""
        if not os.path.exists(self.transcript_dir):
            print(f"❌ Transcript directory not found: {self.transcript_dir}")
            return False

        if not self.check_services():
            print("❌ Required services not running")
            return False

        print("🚀 Starting BMAD-METHOD Auto Monitor")
        print("="*50)
        print(f"📁 Monitoring: {self.transcript_dir}")
        print(f"🔗 Webhook: {self.webhook_url}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)

        # Setup file handler
        event_handler = BMADTranscriptHandler(self.webhook_url)

        # Setup observer
        self.observer = Observer()
        self.observer.schedule(
            event_handler,
            self.transcript_dir,
            recursive=True
        )

        try:
            self.observer.start()
            print("👀 Watching for new transcripts...")
            print("📊 BMAD-METHOD analysis will trigger automatically")
            print("⏹️ Press Ctrl+C to stop monitoring")

            # Keep running
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n⏹️ Stopping BMAD monitor...")
            self.observer.stop()

        self.observer.join()
        print("✅ BMAD Auto Monitor stopped")
        return True

    def process_existing_files(self):
        """Process any existing unprocessed files"""
        print("🔍 Checking for existing unprocessed transcripts...")

        transcript_files = list(Path(self.transcript_dir).glob("*.txt"))

        if not transcript_files:
            print("ℹ️ No transcript files found")
            return

        print(f"📄 Found {len(transcript_files)} transcript files")

        # Check which have been processed
        processed_log = "bmad_processing.log"
        processed_files = set()

        if os.path.exists(processed_log):
            with open(processed_log, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if entry.get('status') == 'triggered':
                            processed_files.add(entry['file'])
                    except:
                        continue

        unprocessed = [f for f in transcript_files if str(f) not in processed_files]

        if unprocessed:
            print(f"🎯 Found {len(unprocessed)} unprocessed files")

            process_all = input("Process all unprocessed files now? (y/N): ").lower().strip()

            if process_all == 'y':
                handler = BMADTranscriptHandler(self.webhook_url)
                for file_path in unprocessed:
                    handler.process_new_transcript(str(file_path))
                    time.sleep(2)  # Rate limiting
        else:
            print("✅ All files already processed")

def main():
    """Main execution"""
    print("🎯 BMAD-METHOD Estate Planning Auto Monitor")
    print("="*50)

    monitor = BMADAutoMonitor()

    try:
        # Check for existing files first
        monitor.process_existing_files()

        # Start monitoring
        monitor.start_monitoring()

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())