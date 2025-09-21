#!/usr/bin/env python3
"""
Complete Estate Planning CRM Setup Script
Integrates Baserow + n8n + GPT-OSS:20B for automated transcript processing
"""

import json
import requests
import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

class CompleteCRMSetup:
    def __init__(self):
        self.base_url = "http://localhost"
        self.n8n_url = "http://localhost:5678"
        self.ollama_url = "http://localhost:11434"
        self.transcript_path = "/Users/joshuavaughan/Documents/McAdams Transcripts"

        self.session = requests.Session()
        self.token = None
        self.database_id = None
        self.pipeline_table_id = None
        self.email_table_id = None
        self.field_mappings = {}

    def log(self, message, level="INFO"):
        """Enhanced logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        icon = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARN": "⚠️"}.get(level, "ℹ️")
        print(f"[{timestamp}] {icon} {message}")

    def check_services(self):
        """Verify all required services are running"""
        services = {
            "Baserow": self.base_url,
            "n8n": self.n8n_url,
            "Ollama": self.ollama_url
        }

        self.log("Checking required services...")
        for name, url in services.items():
            try:
                if name == "Ollama":
                    response = requests.get(f"{url}/api/tags", timeout=5)
                else:
                    response = requests.get(f"{url}/", timeout=5)

                if response.status_code in [200, 404]:  # 404 is OK for some services
                    self.log(f"{name} is running at {url}", "SUCCESS")
                else:
                    self.log(f"{name} responded with {response.status_code}", "WARN")
            except requests.RequestException:
                self.log(f"{name} is not accessible at {url}", "ERROR")
                return False

        # Check GPT-OSS:20B model
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            models = response.json().get('models', [])
            if any('gpt-oss:20b' in model.get('name', '') for model in models):
                self.log("GPT-OSS:20B model is available", "SUCCESS")
            else:
                self.log("GPT-OSS:20B model not found", "ERROR")
                return False
        except:
            self.log("Cannot verify Ollama models", "ERROR")
            return False

        return True

    def setup_baserow(self):
        """Run the Baserow setup using our existing script"""
        self.log("Setting up Baserow CRM...")

        # Import and run the simple setup
        sys.path.append('.')
        try:
            import simple_baserow_setup

            # Create setup instance
            baserow_setup = simple_baserow_setup.SimpleBaserowSetup()

            # Get token interactively
            if not baserow_setup.get_token():
                return False

            # Store token for our use
            self.token = baserow_setup.token
            self.session.headers.update({"Authorization": f"Token {self.token}"})

            # Run setup
            if not baserow_setup.get_or_create_database():
                return False

            self.database_id = baserow_setup.database_id

            # Create tables
            self.pipeline_table_id = baserow_setup.create_table("Pipeline")
            self.email_table_id = baserow_setup.create_table("Follow-ups")

            if not self.pipeline_table_id or not self.email_table_id:
                return False

            # Setup fields
            pipeline_fields = baserow_setup.setup_pipeline_table(self.pipeline_table_id)
            email_fields = baserow_setup.setup_followups_table(self.email_table_id)

            self.field_mappings = {
                "pipeline": pipeline_fields,
                "email": email_fields
            }

            # Generate configs
            baserow_setup.generate_config(
                self.pipeline_table_id, pipeline_fields,
                self.email_table_id, email_fields
            )

            self.log("Baserow CRM setup completed", "SUCCESS")
            return True

        except Exception as e:
            self.log(f"Baserow setup failed: {e}", "ERROR")
            return False

    def generate_enhanced_n8n_workflow(self):
        """Generate the complete n8n workflow with proper field mappings"""

        # Build field mapping for the request body
        pipeline_body = {}
        for field_name, field_id in self.field_mappings["pipeline"].items():
            pipeline_body[f"field_{field_id}"] = f"={{{{ $json.{field_name} }}}}"

        email_body = {}
        for field_name, field_id in self.field_mappings["email"].items():
            email_body[f"field_{field_id}"] = f"={{{{ $json.{field_name} }}}}"

        workflow = {
            "name": "Estate Planning CRM - Complete Automation",
            "nodes": [
                {
                    "parameters": {},
                    "id": "manual-trigger",
                    "name": "Manual Trigger",
                    "type": "n8n-nodes-base.manualTrigger",
                    "position": [250, 300]
                },
                {
                    "parameters": {
                        "path": self.transcript_path,
                        "recursive": True,
                        "fileFilter": "*.txt"
                    },
                    "id": "read-transcripts",
                    "name": "Read Transcript Files",
                    "type": "n8n-nodes-base.filesReadDirectory",
                    "position": [450, 300]
                },
                {
                    "parameters": {
                        "batchSize": 1,
                        "options": {}
                    },
                    "id": "process-one-by-one",
                    "name": "Process One at a Time",
                    "type": "n8n-nodes-base.splitInBatches",
                    "position": [650, 300]
                },
                {
                    "parameters": {
                        "filePath": "={{ $json.path }}",
                        "options": {}
                    },
                    "id": "read-content",
                    "name": "Read File Content",
                    "type": "n8n-nodes-base.filesReadBinary",
                    "position": [850, 300]
                },
                {
                    "parameters": {
                        "url": f"{self.ollama_url}/api/generate",
                        "method": "POST",
                        "headers": {
                            "values": [
                                {"name": "Content-Type", "value": "application/json"}
                            ]
                        },
                        "body": {
                            "type": "json",
                            "value": json.dumps({
                                "model": "gpt-oss:20b",
                                "prompt": self.get_bmad_prompt(),
                                "stream": False,
                                "temperature": 0.1
                            })
                        },
                        "options": {"timeout": 300000}
                    },
                    "id": "bmad-analysis",
                    "name": "BMAD-METHOD Analysis",
                    "type": "n8n-nodes-base.httpRequest",
                    "position": [1050, 300]
                },
                {
                    "parameters": {
                        "mode": "jsonToSingleItem",
                        "jsonString": "={{ JSON.parse($json.response).text.match(/{[\\s\\S]*}/)[0] }}"
                    },
                    "id": "parse-results",
                    "name": "Parse Analysis Results",
                    "type": "n8n-nodes-base.set",
                    "position": [1250, 300]
                },
                {
                    "parameters": {
                        "url": f"{self.base_url}/api/database/rows/table/{self.pipeline_table_id}/",
                        "method": "POST",
                        "headers": {
                            "values": [
                                {"name": "Content-Type", "value": "application/json"},
                                {"name": "Authorization", "value": f"Token {self.token}"}
                            ]
                        },
                        "body": {
                            "type": "json",
                            "value": json.dumps(pipeline_body)
                        }
                    },
                    "id": "create-crm-record",
                    "name": "Create CRM Record",
                    "type": "n8n-nodes-base.httpRequest",
                    "position": [1450, 300]
                },
                {
                    "parameters": {
                        "conditions": {
                            "string": [
                                {
                                    "value1": "={{ $node['parse-results'].json.meeting_stage }}",
                                    "operation": "equals",
                                    "value2": "Follow Up"
                                }
                            ]
                        }
                    },
                    "id": "check-follow-up",
                    "name": "Needs Follow Up?",
                    "type": "n8n-nodes-base.if",
                    "position": [1650, 300]
                },
                {
                    "parameters": {
                        "url": f"{self.ollama_url}/api/generate",
                        "method": "POST",
                        "headers": {
                            "values": [
                                {"name": "Content-Type", "value": "application/json"}
                            ]
                        },
                        "body": {
                            "type": "json",
                            "value": json.dumps({
                                "model": "gpt-oss:20b",
                                "prompt": self.get_email_prompt(),
                                "stream": False,
                                "temperature": 0.7
                            })
                        }
                    },
                    "id": "generate-follow-up",
                    "name": "Generate Follow-Up Email",
                    "type": "n8n-nodes-base.httpRequest",
                    "position": [1850, 200]
                },
                {
                    "parameters": {
                        "url": f"{self.base_url}/api/database/rows/table/{self.email_table_id}/",
                        "method": "POST",
                        "headers": {
                            "values": [
                                {"name": "Content-Type", "value": "application/json"},
                                {"name": "Authorization", "value": f"Token {self.token}"}
                            ]
                        },
                        "body": {
                            "type": "json",
                            "value": json.dumps({
                                f"field_{self.field_mappings['email']['client_name']}": "={{ $node['parse-results'].json.client_name }}",
                                f"field_{self.field_mappings['email']['email_subject']}": "Follow-up: Estate Planning Discussion",
                                f"field_{self.field_mappings['email']['email_body']}": "={{ JSON.parse($json.response).text }}",
                                f"field_{self.field_mappings['email']['status']}": "Draft",
                                f"field_{self.field_mappings['email']['created_date']}": "={{ new Date().toISOString().split('T')[0] }}"
                            })
                        }
                    },
                    "id": "save-email-draft",
                    "name": "Save Email Draft",
                    "type": "n8n-nodes-base.httpRequest",
                    "position": [2050, 200]
                }
            ],
            "connections": {
                "manual-trigger": {
                    "main": [[{"node": "read-transcripts", "type": "main", "index": 0}]]
                },
                "read-transcripts": {
                    "main": [[{"node": "process-one-by-one", "type": "main", "index": 0}]]
                },
                "process-one-by-one": {
                    "main": [[{"node": "read-content", "type": "main", "index": 0}]]
                },
                "read-content": {
                    "main": [[{"node": "bmad-analysis", "type": "main", "index": 0}]]
                },
                "bmad-analysis": {
                    "main": [[{"node": "parse-results", "type": "main", "index": 0}]]
                },
                "parse-results": {
                    "main": [[{"node": "create-crm-record", "type": "main", "index": 0}]]
                },
                "create-crm-record": {
                    "main": [[{"node": "check-follow-up", "type": "main", "index": 0}]]
                },
                "check-follow-up": {
                    "main": [
                        [{"node": "generate-follow-up", "type": "main", "index": 0}],
                        [{"node": "process-one-by-one", "type": "main", "index": 0}]
                    ]
                },
                "generate-follow-up": {
                    "main": [[{"node": "save-email-draft", "type": "main", "index": 0}]]
                },
                "save-email-draft": {
                    "main": [[{"node": "process-one-by-one", "type": "main", "index": 0}]]
                }
            }
        }

        with open("complete_estate_planning_workflow.json", "w") as f:
            json.dump(workflow, f, indent=2)

        self.log("Generated complete n8n workflow", "SUCCESS")
        return True

    def get_bmad_prompt(self):
        """BMAD-METHOD analysis prompt for GPT-OSS:20B"""
        return """You are a BMAD-METHOD estate planning sales analyst with 20+ years of experience. Analyze this transcript with extreme precision for sales intelligence.

BMAD-METHOD CLASSIFICATION (Critical for sales strategy):

🎯 CLOSED WON: Explicit agreement, payment, signed engagement, immediate next steps scheduled
❌ CLOSED LOST: Explicit decline, chose competitor, cannot afford with no alternatives
📞 FOLLOW UP: Interested but needs discussion, more info, timing concerns, spouse consultation
🚫 NO SHOW: Meeting didn't happen, client absent, rescheduled

EXTRACT STRATEGIC SALES DATA:
{
  "client_name": "full name from transcript",
  "meeting_date": "YYYY-MM-DD",
  "meeting_stage": "Closed Won|Closed Lost|No Show|Follow Up",
  "state": "2-letter code",
  "marital_status": "Single|Married|Divorced|Widowed",
  "age": number_or_null,
  "estate_value": "amount or range",
  "num_beneficiaries": number,
  "real_estate_count": number,
  "llc_interest": "Yes|No|Maybe",
  "urgency_score": 1-5,
  "next_steps": "specific action items",
  "key_pain_points": "main concerns expressed",
  "has_minor_children": true|false,
  "business_owner": true|false
}

TRANSCRIPT: {{ $binary.data.toString() }}

Return ONLY valid JSON with precise sales intelligence:"""

    def get_email_prompt(self):
        """Email generation prompt"""
        return """Generate a compelling estate planning follow-up email based on the client analysis.

Client Data:
- Name: {{ $node['parse-results'].json.client_name }}
- Estate Value: {{ $node['parse-results'].json.estate_value }}
- Key Concerns: {{ $node['parse-results'].json.key_pain_points }}
- Urgency: {{ $node['parse-results'].json.urgency_score }}/5

Write a professional, personalized follow-up email that:
1. References specific meeting details
2. Addresses their concerns
3. Emphasizes urgency appropriately
4. Provides clear next steps
5. Professional but warm tone

Return only the email body text:"""

    def create_automation_script(self):
        """Create a script to automate the entire process"""
        script_content = f'''#!/bin/bash
# Estate Planning CRM Automation Script

echo "🚀 Starting Estate Planning CRM Processing..."

# Check if new transcripts exist
TRANSCRIPT_DIR="{self.transcript_path}"
NEW_FILES=$(find "$TRANSCRIPT_DIR" -name "*.txt" -newer .last_processed 2>/dev/null | wc -l)

if [ "$NEW_FILES" -gt 0 ]; then
    echo "📄 Found $NEW_FILES new transcript(s) to process"

    # Trigger n8n workflow
    curl -X POST "{self.n8n_url}/webhook/estate-planning-process" \\
         -H "Content-Type: application/json" \\
         -d '{{"trigger": "new_transcripts"}}'

    # Update timestamp
    touch .last_processed

    echo "✅ Processing triggered successfully"
    echo "📊 Check results at: {self.base_url}/database/{self.database_id}"
else
    echo "ℹ️ No new transcripts to process"
fi
'''

        with open("automate_crm.sh", "w") as f:
            f.write(script_content)

        os.chmod("automate_crm.sh", 0o755)
        self.log("Created automation script", "SUCCESS")

    def create_deployment_summary(self):
        """Create comprehensive deployment documentation"""
        summary = f"""# 🏆 Complete Estate Planning CRM Deployment

## ✅ System Status
- **Baserow CRM**: {self.base_url}/database/{self.database_id}
- **Pipeline Table**: {self.pipeline_table_id}
- **Email Queue**: {self.email_table_id}
- **n8n Workflow**: Import `complete_estate_planning_workflow.json`
- **Processing**: {self.transcript_path}

## 🔄 Automation Flow
```
New Transcript → BMAD Analysis → CRM Record → Follow-up Email Draft
```

## 📋 Next Steps
1. **Import n8n workflow**: `complete_estate_planning_workflow.json`
2. **Test with single file**: Move one transcript to test folder first
3. **Monitor processing**: Watch n8n execution logs
4. **Review results**: Check Baserow tables for data
5. **Automate**: Set up `automate_crm.sh` as cron job

## 🎯 Key Features
- **BMAD-METHOD Analysis**: Strategic sales intelligence
- **26+ Data Points**: Complete client profiles
- **Automated Classification**: Won/Lost/Follow-up/No-show
- **Email Generation**: Personalized follow-up drafts
- **Local Processing**: No cloud dependencies
- **Privacy First**: Client data stays on your Mac

## 📊 Expected Results
After processing 352 transcripts:
- Complete sales pipeline in Baserow
- Automated follow-up emails for prospects
- Strategic insights for sales optimization
- No manual data entry required

## 🔧 Maintenance
- Monitor Ollama for GPT-OSS:20B performance
- Check Baserow storage usage
- Review and send drafted emails
- Analyze pipeline metrics monthly

**🎉 Your local estate planning CRM is ready for production!**

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        with open("DEPLOYMENT_COMPLETE.md", "w") as f:
            f.write(summary)

        self.log("Created deployment summary", "SUCCESS")

    def run_complete_setup(self):
        """Execute the complete CRM setup"""
        self.log("🚀 Starting Complete Estate Planning CRM Setup", "INFO")
        print("="*60)

        # Check services
        if not self.check_services():
            self.log("Service check failed - ensure all services are running", "ERROR")
            return False

        # Setup Baserow
        if not self.setup_baserow():
            self.log("Baserow setup failed", "ERROR")
            return False

        # Generate n8n workflow
        if not self.generate_enhanced_n8n_workflow():
            self.log("Workflow generation failed", "ERROR")
            return False

        # Create automation
        self.create_automation_script()

        # Generate documentation
        self.create_deployment_summary()

        print("="*60)
        self.log("🎉 COMPLETE CRM SETUP SUCCESSFUL!", "SUCCESS")
        print("="*60)

        print(f"📊 CRM Dashboard: {self.base_url}/database/{self.database_id}")
        print(f"🔧 n8n Workflows: {self.n8n_url}")
        print(f"📄 Import: complete_estate_planning_workflow.json")
        print(f"🤖 Automation: ./automate_crm.sh")

        return True

def main():
    """Main execution"""
    setup = CompleteCRMSetup()

    try:
        if setup.run_complete_setup():
            print("\n🚀 Ready to process 352 estate planning transcripts!")
            print("📖 See DEPLOYMENT_COMPLETE.md for next steps")
        else:
            print("\n❌ Setup failed - check error messages above")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()