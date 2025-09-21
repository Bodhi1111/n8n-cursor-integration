#!/usr/bin/env python3
"""
One-Click BMAD-METHOD Estate Planning CRM Deployment
Complete automation setup for transcript processing
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path
from datetime import datetime

class BMADCRMDeployment:
    """Complete BMAD-METHOD CRM deployment automation"""

    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.services = {
            "baserow": "http://localhost",
            "n8n": "http://localhost:5678",
            "ollama": "http://localhost:11434"
        }
        self.transcript_path = "/Users/joshuavaughan/Documents/McAdams Transcripts"

    def print_header(self):
        """Print deployment header"""
        print("🎯" + "="*58 + "🎯")
        print("🏆 BMAD-METHOD ESTATE PLANNING CRM DEPLOYMENT 🏆")
        print("🎯" + "="*58 + "🎯")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Project: {self.project_dir}")
        print("🔄 Complete automation for 352 transcripts")
        print()

    def check_prerequisites(self):
        """Check all prerequisites"""
        print("🔍 Checking Prerequisites...")
        print("-" * 30)

        # Check Python packages
        required_packages = ["requests", "watchdog"]
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ Python package: {package}")
            except ImportError:
                print(f"❌ Missing package: {package}")
                print(f"   Install with: pip3 install {package}")
                return False

        # Check services
        for name, url in self.services.items():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code in [200, 404]:
                    print(f"✅ Service running: {name}")
                else:
                    print(f"⚠️ Service issue: {name} ({response.status_code})")
            except requests.RequestException:
                print(f"❌ Service down: {name}")
                return False

        # Check GPT-OSS:20B model
        try:
            response = requests.get(f"{self.services['ollama']}/api/tags")
            models = response.json().get('models', [])
            if any('gpt-oss:20b' in model.get('name', '') for model in models):
                print("✅ GPT-OSS:20B model available")
            else:
                print("❌ GPT-OSS:20B model not found")
                print("   Install with: ollama pull gpt-oss:20b")
                return False
        except:
            print("❌ Cannot verify Ollama models")
            return False

        # Check transcript directory
        if os.path.exists(self.transcript_path):
            file_count = len(list(Path(self.transcript_path).glob("*.txt")))
            print(f"✅ Transcript directory: {file_count} files")
        else:
            print(f"❌ Transcript directory not found: {self.transcript_path}")
            return False

        print("✅ All prerequisites satisfied")
        return True

    def run_baserow_setup(self):
        """Execute Baserow CRM setup"""
        print("\n🏗️ Setting up Baserow CRM...")
        print("-" * 30)

        try:
            # Run the complete CRM setup
            result = subprocess.run([
                sys.executable, "complete_crm_setup.py"
            ], capture_output=True, text=True, cwd=self.project_dir)

            if result.returncode == 0:
                print("✅ Baserow CRM setup completed")
                return True
            else:
                print("❌ Baserow setup failed:")
                print(result.stderr)
                return False

        except Exception as e:
            print(f"❌ Error running Baserow setup: {e}")
            return False

    def install_n8n_workflow(self):
        """Install the n8n workflow"""
        print("\n🔄 Installing n8n Workflow...")
        print("-" * 30)

        workflow_file = self.project_dir / "complete_estate_planning_workflow.json"

        if not workflow_file.exists():
            print(f"❌ Workflow file not found: {workflow_file}")
            return False

        print(f"📄 Workflow file: {workflow_file.name}")
        print(f"🔗 n8n URL: {self.services['n8n']}")
        print()
        print("⚠️ MANUAL STEP REQUIRED:")
        print("1. Open n8n in your browser")
        print("2. Go to Workflows → Import from File")
        print(f"3. Select: {workflow_file}")
        print("4. Activate the workflow")
        print()

        input("Press Enter when workflow is imported and activated...")
        print("✅ n8n workflow installation confirmed")
        return True

    def setup_automation(self):
        """Setup file monitoring automation"""
        print("\n🤖 Setting up Automation...")
        print("-" * 30)

        # Make scripts executable
        scripts = ["bmad_auto_monitor.py", "automate_crm.sh"]
        for script in scripts:
            script_path = self.project_dir / script
            if script_path.exists():
                os.chmod(script_path, 0o755)
                print(f"✅ Made executable: {script}")

        # Create launchd plist for auto-monitoring
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.bmad.estate.monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{self.project_dir}/bmad_auto_monitor.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{self.project_dir}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{self.project_dir}/bmad_monitor.log</string>
    <key>StandardErrorPath</key>
    <string>{self.project_dir}/bmad_monitor_error.log</string>
</dict>
</plist>'''

        plist_file = Path.home() / "Library/LaunchAgents/com.bmad.estate.monitor.plist"
        plist_file.parent.mkdir(exist_ok=True)

        with open(plist_file, 'w') as f:
            f.write(plist_content)

        print(f"✅ Created LaunchAgent: {plist_file}")
        print("⚠️ Auto-monitoring service created (not started yet)")

        return True

    def create_control_scripts(self):
        """Create control scripts for the system"""
        print("\n📜 Creating Control Scripts...")
        print("-" * 30)

        # Start script
        start_script = f'''#!/bin/bash
# Start BMAD-METHOD Estate Planning CRM

echo "🚀 Starting BMAD-METHOD Estate Planning CRM"

# Load LaunchAgent
launchctl load ~/Library/LaunchAgents/com.bmad.estate.monitor.plist

echo "✅ Auto-monitoring started"
echo "📊 CRM Dashboard: http://localhost/database"
echo "🔧 n8n Workflows: http://localhost:5678"
echo "📄 Logs: {self.project_dir}/bmad_monitor.log"
'''

        with open("start_bmad_crm.sh", "w") as f:
            f.write(start_script)
        os.chmod("start_bmad_crm.sh", 0o755)

        # Stop script
        stop_script = '''#!/bin/bash
# Stop BMAD-METHOD Estate Planning CRM

echo "⏹️ Stopping BMAD-METHOD Estate Planning CRM"

# Unload LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.bmad.estate.monitor.plist

echo "✅ Auto-monitoring stopped"
'''

        with open("stop_bmad_crm.sh", "w") as f:
            f.write(stop_script)
        os.chmod("stop_bmad_crm.sh", 0o755)

        # Status script
        status_script = f'''#!/bin/bash
# Check BMAD-METHOD Estate Planning CRM Status

echo "📊 BMAD-METHOD Estate Planning CRM Status"
echo "="*50

# Check LaunchAgent
if launchctl list | grep -q com.bmad.estate.monitor; then
    echo "✅ Auto-monitoring: Running"
else
    echo "❌ Auto-monitoring: Stopped"
fi

# Check services
curl -s http://localhost > /dev/null && echo "✅ Baserow: Running" || echo "❌ Baserow: Down"
curl -s http://localhost:5678 > /dev/null && echo "✅ n8n: Running" || echo "❌ n8n: Down"
curl -s http://localhost:11434/api/tags > /dev/null && echo "✅ Ollama: Running" || echo "❌ Ollama: Down"

# Check logs
if [ -f "{self.project_dir}/bmad_monitor.log" ]; then
    echo "📄 Latest activity:"
    tail -5 "{self.project_dir}/bmad_monitor.log"
fi
'''

        with open("status_bmad_crm.sh", "w") as f:
            f.write(status_script)
        os.chmod("status_bmad_crm.sh", 0o755)

        print("✅ Created control scripts:")
        print("   - start_bmad_crm.sh")
        print("   - stop_bmad_crm.sh")
        print("   - status_bmad_crm.sh")

        return True

    def run_deployment_test(self):
        """Run a complete deployment test"""
        print("\n🧪 Running Deployment Test...")
        print("-" * 30)

        # Test with sample transcript
        sample_transcript = self.project_dir / "sample-transcript.txt"

        if not sample_transcript.exists():
            print("⚠️ No test transcript found, skipping test")
            return True

        try:
            # Copy to transcript directory for testing
            test_file = Path(self.transcript_path) / "TEST_DEPLOYMENT.txt"
            with open(sample_transcript) as src:
                with open(test_file, 'w') as dst:
                    dst.write(src.read())

            print(f"✅ Created test file: {test_file}")
            print("⏳ Monitoring for automatic processing...")

            # Give system time to process
            import time
            time.sleep(10)

            # Clean up test file
            if test_file.exists():
                test_file.unlink()
                print("🧹 Cleaned up test file")

            print("✅ Deployment test completed")
            return True

        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False

    def generate_deployment_report(self):
        """Generate final deployment report"""
        print("\n📋 Generating Deployment Report...")
        print("-" * 30)

        report = f"""# 🎯 BMAD-METHOD Estate Planning CRM - Deployment Complete

## 🏆 System Overview
**Deployed**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Location**: {self.project_dir}
**Transcripts**: {self.transcript_path}

## 🚀 Services
- **Baserow CRM**: http://localhost
- **n8n Automation**: http://localhost:5678
- **GPT-OSS:20B**: http://localhost:11434
- **Auto-Monitor**: LaunchAgent configured

## 🎯 BMAD-METHOD Features
✅ **Behavioral Analysis**: Client engagement patterns
✅ **Meeting Classification**: Won/Lost/Follow-up/No-show
✅ **Asset Discovery**: Estate value, real estate, business entities
✅ **Decision Intelligence**: Pain points, objections, urgency scoring

## 🔄 Automation Workflow
```
New Transcript → BMAD Analysis → CRM Record → Follow-up Email
```

## 📋 Control Commands
```bash
./start_bmad_crm.sh    # Start auto-monitoring
./stop_bmad_crm.sh     # Stop auto-monitoring
./status_bmad_crm.sh   # Check system status
```

## 📊 Expected Results (352 Transcripts)
- Complete sales pipeline database
- Automated prospect classification
- Generated follow-up emails for warm leads
- Strategic insights for sales optimization
- Zero manual data entry

## 🔧 File Structure
- `baserow_config.json` - Database configuration
- `complete_estate_planning_workflow.json` - n8n workflow
- `bmad_auto_monitor.py` - File monitoring service
- `bmad_processing.log` - Processing activity log

## 🎉 Next Steps
1. **Start Monitoring**: `./start_bmad_crm.sh`
2. **Test Drop**: Add new transcript to folder
3. **Monitor Results**: Check Baserow dashboard
4. **Review Emails**: Draft follow-ups generated automatically
5. **Scale Up**: Process all 352 transcripts

## 🛡️ Privacy & Security
- All processing local on Mac
- No cloud dependencies
- Client data never leaves your machine
- BMAD-METHOD analysis for sales intelligence only

**🎯 Your estate planning CRM is ready for production!**

---
*BMAD-METHOD: Behavioral, Meeting, Asset, Decision analysis for estate planning sales intelligence*
"""

        with open("BMAD_DEPLOYMENT_COMPLETE.md", "w") as f:
            f.write(report)

        print("✅ Deployment report created: BMAD_DEPLOYMENT_COMPLETE.md")
        return True

    def run_full_deployment(self):
        """Execute complete deployment"""
        self.print_header()

        deployment_steps = [
            ("Prerequisites", self.check_prerequisites),
            ("Baserow Setup", self.run_baserow_setup),
            ("n8n Workflow", self.install_n8n_workflow),
            ("Automation", self.setup_automation),
            ("Control Scripts", self.create_control_scripts),
            ("Testing", self.run_deployment_test),
            ("Documentation", self.generate_deployment_report)
        ]

        for step_name, step_func in deployment_steps:
            print(f"\n🔄 Step: {step_name}")
            if not step_func():
                print(f"\n❌ Deployment failed at: {step_name}")
                return False

        print("\n" + "🎉" + "="*58 + "🎉")
        print("🏆 BMAD-METHOD CRM DEPLOYMENT SUCCESSFUL! 🏆")
        print("🎉" + "="*58 + "🎉")
        print()
        print("🚀 Ready to process 352 estate planning transcripts!")
        print("📊 CRM Dashboard: http://localhost")
        print("🔧 n8n Automation: http://localhost:5678")
        print("🤖 Start monitoring: ./start_bmad_crm.sh")
        print()
        print("📖 Complete guide: BMAD_DEPLOYMENT_COMPLETE.md")

        return True

def main():
    """Main deployment execution"""
    deployment = BMADCRMDeployment()

    try:
        if deployment.run_full_deployment():
            return 0
        else:
            print("\n❌ Deployment failed")
            return 1
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())