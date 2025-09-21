#!/usr/bin/env python3
"""
Baserow Estate Planning CRM Setup Script
Creates workspace, tables, fields, and generates configuration files for n8n integration.
"""

import json
import requests
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

class BaserowSetup:
    def __init__(self, base_url: str = "http://localhost"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.workspace_id = None
        self.database_id = None
        self.pipeline_table_id = None
        self.email_table_id = None
        self.field_mappings = {}

    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def check_baserow_connection(self) -> bool:
        """Check if Baserow is accessible"""
        try:
            response = self.session.get(f"{self.base_url}/api/health/")
            if response.status_code == 200:
                self.log("✅ Baserow is accessible")
                return True
            else:
                self.log(f"❌ Baserow health check failed: {response.status_code}", "ERROR")
                return False
        except requests.RequestException as e:
            self.log(f"❌ Cannot connect to Baserow: {e}", "ERROR")
            return False

    def get_or_create_token(self) -> bool:
        """Get API token - requires manual creation in Baserow UI"""
        print("\n" + "="*60)
        print("API TOKEN SETUP REQUIRED")
        print("="*60)
        print("Please create an API token in Baserow:")
        print(f"1. Open {self.base_url} in your browser")
        print("2. Log in to your Baserow account")
        print("3. Go to Settings → API Tokens")
        print("4. Click 'Create Token'")
        print("5. Name it 'Estate Planning CRM'")
        print("6. Copy the token and paste it below")
        print("="*60)

        token = input("Enter your Baserow API token: ").strip()
        if not token:
            self.log("❌ No token provided", "ERROR")
            return False

        # Test the token
        self.session.headers.update({"Authorization": f"Token {token}"})
        try:
            response = self.session.get(f"{self.base_url}/api/applications/")
            if response.status_code == 200:
                self.token = token
                self.log("✅ API token validated successfully")
                return True
            else:
                self.log(f"❌ Invalid API token: {response.status_code}", "ERROR")
                return False
        except requests.RequestException as e:
            self.log(f"❌ Error validating token: {e}", "ERROR")
            return False

    def create_workspace(self) -> bool:
        """Create Estate Planning CRM workspace"""
        try:
            # Check if workspace already exists
            response = self.session.get(f"{self.base_url}/api/workspaces/")
            if response.status_code == 200:
                workspaces = response.json()
                for workspace in workspaces:
                    if workspace['name'] == 'Estate Planning CRM':
                        self.workspace_id = workspace['id']
                        self.log(f"✅ Found existing workspace: {self.workspace_id}")
                        return True

            # Create new workspace
            data = {"name": "Estate Planning CRM"}
            response = self.session.post(f"{self.base_url}/api/workspaces/", json=data)

            if response.status_code == 200:
                workspace = response.json()
                self.workspace_id = workspace['id']
                self.log(f"✅ Created workspace: {self.workspace_id}")
                return True
            else:
                self.log(f"❌ Failed to create workspace: {response.status_code} - {response.text}", "ERROR")
                return False

        except requests.RequestException as e:
            self.log(f"❌ Error creating workspace: {e}", "ERROR")
            return False

    def create_database(self) -> bool:
        """Create database in the workspace"""
        try:
            # Check if database already exists
            response = self.session.get(f"{self.base_url}/api/applications/")
            if response.status_code == 200:
                applications = response.json()
                for app in applications:
                    if app['name'] == 'Estate Planning Database' and app['workspace']['id'] == self.workspace_id:
                        self.database_id = app['id']
                        self.log(f"✅ Found existing database: {self.database_id}")
                        return True

            # Create new database
            data = {
                "name": "Estate Planning Database",
                "type": "database",
                "workspace_id": self.workspace_id
            }
            response = self.session.post(f"{self.base_url}/api/applications/", json=data)

            if response.status_code == 200:
                database = response.json()
                self.database_id = database['id']
                self.log(f"✅ Created database: {self.database_id}")
                return True
            else:
                self.log(f"❌ Failed to create database: {response.status_code} - {response.text}", "ERROR")
                return False

        except requests.RequestException as e:
            self.log(f"❌ Error creating database: {e}", "ERROR")
            return False

    def create_table(self, table_name: str) -> Optional[int]:
        """Create a table in the database"""
        try:
            # Check if table already exists
            response = self.session.get(f"{self.base_url}/api/database/tables/database/{self.database_id}/")
            if response.status_code == 200:
                tables = response.json()
                for table in tables:
                    if table['name'] == table_name:
                        self.log(f"✅ Found existing table '{table_name}': {table['id']}")
                        return table['id']

            # Create new table
            data = {"name": table_name, "database_id": self.database_id}
            response = self.session.post(f"{self.base_url}/api/database/tables/database/{self.database_id}/", json=data)

            if response.status_code == 200:
                table = response.json()
                self.log(f"✅ Created table '{table_name}': {table['id']}")
                return table['id']
            else:
                self.log(f"❌ Failed to create table '{table_name}': {response.status_code} - {response.text}", "ERROR")
                return None

        except requests.RequestException as e:
            self.log(f"❌ Error creating table '{table_name}': {e}", "ERROR")
            return None

    def create_field(self, table_id: int, field_config: Dict[str, Any]) -> Optional[Dict]:
        """Create a field in a table"""
        try:
            # Check if field already exists
            response = self.session.get(f"{self.base_url}/api/database/fields/table/{table_id}/")
            if response.status_code == 200:
                existing_fields = response.json()
                for field in existing_fields:
                    if field['name'] == field_config['name']:
                        self.log(f"✅ Found existing field '{field_config['name']}': {field['id']}")
                        return field

            # Create new field
            response = self.session.post(f"{self.base_url}/api/database/fields/table/{table_id}/", json=field_config)

            if response.status_code == 200:
                field = response.json()
                self.log(f"✅ Created field '{field_config['name']}': {field['id']}")
                return field
            else:
                self.log(f"❌ Failed to create field '{field_config['name']}': {response.status_code} - {response.text}", "ERROR")
                return None

        except requests.RequestException as e:
            self.log(f"❌ Error creating field '{field_config['name']}': {e}", "ERROR")
            return None

    def get_pipeline_field_configs(self) -> List[Dict[str, Any]]:
        """Define all fields for the Pipeline table"""
        return [
            {"name": "client_name", "type": "text"},
            {"name": "meeting_date", "type": "date", "date_format": "US"},
            {"name": "meeting_stage", "type": "single_select", "select_options": [
                {"value": "Closed Won", "color": "green"},
                {"value": "Closed Lost", "color": "red"},
                {"value": "No Show", "color": "gray"},
                {"value": "Follow Up", "color": "blue"}
            ]},
            {"name": "state", "type": "text"},
            {"name": "marital_status", "type": "single_select", "select_options": [
                {"value": "Single", "color": "blue"},
                {"value": "Married", "color": "green"},
                {"value": "Divorced", "color": "orange"},
                {"value": "Widowed", "color": "gray"}
            ]},
            {"name": "age", "type": "number", "number_decimal_places": 0},
            {"name": "spouse_name", "type": "text"},
            {"name": "estate_value", "type": "text"},
            {"name": "num_beneficiaries", "type": "number", "number_decimal_places": 0},
            {"name": "primary_beneficiaries", "type": "long_text"},
            {"name": "real_estate_count", "type": "number", "number_decimal_places": 0},
            {"name": "real_estate_locations", "type": "long_text"},
            {"name": "llc_interest", "type": "single_select", "select_options": [
                {"value": "Yes", "color": "green"},
                {"value": "No", "color": "red"},
                {"value": "Maybe", "color": "orange"}
            ]},
            {"name": "entity_type", "type": "single_select", "select_options": [
                {"value": "LLC", "color": "blue"},
                {"value": "Trust", "color": "green"},
                {"value": "Corporation", "color": "purple"},
                {"value": "None", "color": "gray"}
            ]},
            {"name": "urgency_score", "type": "rating", "max_value": 5},
            {"name": "next_steps", "type": "long_text"},
            {"name": "key_pain_points", "type": "long_text"},
            {"name": "decision_factors", "type": "long_text"},
            {"name": "objections_raised", "type": "long_text"},
            {"name": "follow_up_timeline", "type": "text"},
            {"name": "has_minor_children", "type": "boolean"},
            {"name": "business_owner", "type": "boolean"},
            {"name": "meeting_quality", "type": "single_select", "select_options": [
                {"value": "Excellent", "color": "green"},
                {"value": "Good", "color": "blue"},
                {"value": "Fair", "color": "orange"},
                {"value": "Poor", "color": "red"}
            ]},
            {"name": "advisor_notes", "type": "long_text"},
            {"name": "processing_status", "type": "single_select", "select_options": [
                {"value": "Pending", "color": "orange"},
                {"value": "Processed", "color": "green"},
                {"value": "Error", "color": "red"}
            ]},
            {"name": "source_transcript", "type": "text"}
        ]

    def get_email_field_configs(self) -> List[Dict[str, Any]]:
        """Define all fields for the Email Queue table"""
        return [
            {"name": "client_name", "type": "text"},
            {"name": "email_subject", "type": "text"},
            {"name": "email_body", "type": "long_text"},
            {"name": "status", "type": "single_select", "select_options": [
                {"value": "Draft", "color": "orange"},
                {"value": "Ready to Send", "color": "blue"},
                {"value": "Sent", "color": "green"},
                {"value": "Response Received", "color": "purple"}
            ]},
            {"name": "created_date", "type": "date", "date_format": "US"},
            {"name": "meeting_stage", "type": "text"},
            {"name": "original_record_id", "type": "number", "number_decimal_places": 0}
        ]

    def setup_tables_and_fields(self) -> bool:
        """Create all tables and fields"""
        # Create Pipeline table
        self.pipeline_table_id = self.create_table("Pipeline")
        if not self.pipeline_table_id:
            return False

        # Create Email Queue table
        self.email_table_id = self.create_table("Email Queue")
        if not self.email_table_id:
            return False

        # Create Pipeline fields
        self.log("Creating Pipeline table fields...")
        pipeline_fields = {}
        for field_config in self.get_pipeline_field_configs():
            field = self.create_field(self.pipeline_table_id, field_config)
            if field:
                pipeline_fields[field_config['name']] = field['id']
            time.sleep(0.5)  # Rate limiting

        # Create Email Queue fields
        self.log("Creating Email Queue table fields...")
        email_fields = {}
        for field_config in self.get_email_field_configs():
            field = self.create_field(self.email_table_id, field_config)
            if field:
                email_fields[field_config['name']] = field['id']
            time.sleep(0.5)  # Rate limiting

        self.field_mappings = {
            "pipeline": pipeline_fields,
            "email_queue": email_fields
        }

        return True

    def create_test_record(self) -> bool:
        """Create a test record to verify setup"""
        try:
            test_data = {
                f"field_{self.field_mappings['pipeline']['client_name']}": "Test Client - John Smith",
                f"field_{self.field_mappings['pipeline']['meeting_date']}": "2024-03-15",
                f"field_{self.field_mappings['pipeline']['meeting_stage']}": "Follow Up",
                f"field_{self.field_mappings['pipeline']['state']}": "TX",
                f"field_{self.field_mappings['pipeline']['estate_value']}": "$2.5M",
                f"field_{self.field_mappings['pipeline']['processing_status']}": "Processed"
            }

            response = self.session.post(
                f"{self.base_url}/api/database/rows/table/{self.pipeline_table_id}/",
                json=test_data
            )

            if response.status_code == 200:
                record = response.json()
                self.log(f"✅ Created test record: {record['id']}")
                return True
            else:
                self.log(f"❌ Failed to create test record: {response.status_code} - {response.text}", "ERROR")
                return False

        except requests.RequestException as e:
            self.log(f"❌ Error creating test record: {e}", "ERROR")
            return False

    def generate_config_files(self):
        """Generate configuration files for n8n integration"""
        # Main config file
        config = {
            "baserow": {
                "base_url": self.base_url,
                "api_token": self.token,
                "workspace_id": self.workspace_id,
                "database_id": self.database_id
            },
            "tables": {
                "pipeline": {
                    "id": self.pipeline_table_id,
                    "name": "Pipeline"
                },
                "email_queue": {
                    "id": self.email_table_id,
                    "name": "Email Queue"
                }
            },
            "field_mappings": self.field_mappings
        }

        # Save main config
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        self.log("✅ Generated config.json")

        # n8n Settings node configuration
        n8n_settings = {
            "tableId": str(self.pipeline_table_id),
            "emailTableId": str(self.email_table_id),
            "baserowToken": self.token,
            "baserowUrl": self.base_url
        }

        with open("n8n_settings.json", "w") as f:
            json.dump(n8n_settings, f, indent=2)
        self.log("✅ Generated n8n_settings.json")

        # Field mapping for n8n workflow body
        field_mapping_body = {}
        for field_name, field_id in self.field_mappings['pipeline'].items():
            field_mapping_body[f"field_{field_id}"] = f"={{{{ $json.{field_name} }}}}"

        with open("n8n_field_mapping.json", "w") as f:
            json.dump(field_mapping_body, f, indent=2)
        self.log("✅ Generated n8n_field_mapping.json")

        # Setup verification report
        verification = f"""# Baserow Estate Planning CRM Setup Verification

## ✅ Setup Complete - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Created Resources:
- **Workspace**: Estate Planning CRM (ID: {self.workspace_id})
- **Database**: Estate Planning Database (ID: {self.database_id})
- **Pipeline Table**: {self.pipeline_table_id} ({len(self.field_mappings['pipeline'])} fields)
- **Email Queue Table**: {self.email_table_id} ({len(self.field_mappings['email_queue'])} fields)

### Access Information:
- **Baserow URL**: {self.base_url}
- **API Token**: {self.token[:8]}...{self.token[-4:]}

### Pipeline Table Fields:
"""
        for field_name, field_id in self.field_mappings['pipeline'].items():
            verification += f"- {field_name}: field_{field_id}\n"

        verification += f"""
### Email Queue Table Fields:
"""
        for field_name, field_id in self.field_mappings['email_queue'].items():
            verification += f"- {field_name}: field_{field_id}\n"

        verification += f"""
### Generated Files:
- `config.json` - Complete configuration
- `n8n_settings.json` - Ready for n8n Settings node
- `n8n_field_mapping.json` - Field mapping for workflow body
- `setup_verification.md` - This verification report

### Next Steps:
1. Import the corrected n8n workflow: `estate-planning-workflow-fixed.json`
2. Update the Settings node with values from `n8n_settings.json`
3. Update the Baserow create nodes with field mappings from `n8n_field_mapping.json`
4. Test with one transcript file
5. Process all 352 transcripts

### Test Access:
Access your CRM at: {self.base_url}/database/{self.database_id}/table/{self.pipeline_table_id}
"""

        with open("setup_verification.md", "w") as f:
            f.write(verification)
        self.log("✅ Generated setup_verification.md")

    def run_setup(self) -> bool:
        """Run the complete setup process"""
        self.log("🚀 Starting Baserow Estate Planning CRM Setup")

        # Check connection
        if not self.check_baserow_connection():
            return False

        # Get API token
        if not self.get_or_create_token():
            return False

        # Create workspace
        if not self.create_workspace():
            return False

        # Create database
        if not self.create_database():
            return False

        # Create tables and fields
        if not self.setup_tables_and_fields():
            return False

        # Create test record
        if not self.create_test_record():
            return False

        # Generate config files
        self.generate_config_files()

        self.log("🎉 Setup completed successfully!")
        self.log(f"📊 Access your CRM: {self.base_url}/database/{self.database_id}/table/{self.pipeline_table_id}")

        return True

def main():
    """Main execution function"""
    print("="*60)
    print("BASEROW ESTATE PLANNING CRM SETUP")
    print("="*60)

    setup = BaserowSetup()

    try:
        if setup.run_setup():
            print("\n" + "="*60)
            print("✅ SETUP COMPLETED SUCCESSFULLY!")
            print("="*60)
            print("Generated files:")
            print("- config.json")
            print("- n8n_settings.json")
            print("- n8n_field_mapping.json")
            print("- setup_verification.md")
            print("\nReady to integrate with n8n workflow!")
            sys.exit(0)
        else:
            print("\n" + "="*60)
            print("❌ SETUP FAILED")
            print("="*60)
            print("Check the error messages above and try again.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()