#!/usr/bin/env python3
"""
Simple Baserow Estate Planning CRM Setup
Creates tables and fields, outputs config for n8n integration.
"""

import json
import requests
import sys
from datetime import datetime

class SimpleBaserowSetup:
    def __init__(self):
        self.base_url = "http://localhost"
        self.session = requests.Session()
        self.token = None
        self.database_id = None

    def get_token(self):
        """Get API token from user"""
        print("🔑 Baserow API Token Setup")
        print("-" * 40)
        print(f"1. Open {self.base_url} in your browser")
        print("2. Login or create account")
        print("3. Go to Settings → API Tokens")
        print("4. Create new token (name: 'Estate Planning')")
        print("5. Copy and paste the token below")
        print()

        token = input("Enter your API token: ").strip()
        if not token:
            print("❌ No token provided")
            return False

        # Test token
        self.session.headers.update({"Authorization": f"Token {token}"})
        try:
            response = self.session.get(f"{self.base_url}/api/applications/")
            if response.status_code == 200:
                self.token = token
                print("✅ Token validated")
                return True
            else:
                print(f"❌ Invalid token: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def get_or_create_database(self):
        """Get existing database or create new one"""
        try:
            # Check existing databases
            response = self.session.get(f"{self.base_url}/api/applications/")
            apps = response.json()

            # Look for existing database
            for app in apps:
                if app['type'] == 'database':
                    self.database_id = app['id']
                    print(f"✅ Using existing database: {app['name']} (ID: {self.database_id})")
                    return True

            # Create new database if none found
            data = {"name": "Estate Planning CRM", "type": "database"}
            response = self.session.post(f"{self.base_url}/api/applications/", json=data)

            if response.status_code == 200:
                app = response.json()
                self.database_id = app['id']
                print(f"✅ Created database: {app['name']} (ID: {self.database_id})")
                return True
            else:
                print(f"❌ Failed to create database: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Database setup error: {e}")
            return False

    def create_table(self, name):
        """Create a table"""
        try:
            # Check if table exists
            response = self.session.get(f"{self.base_url}/api/database/tables/database/{self.database_id}/")
            tables = response.json()

            for table in tables:
                if table['name'] == name:
                    print(f"✅ Found existing table: {name} (ID: {table['id']})")
                    return table['id']

            # Create new table
            data = {"name": name, "database_id": self.database_id}
            response = self.session.post(f"{self.base_url}/api/database/tables/database/{self.database_id}/", json=data)

            if response.status_code == 200:
                table = response.json()
                print(f"✅ Created table: {name} (ID: {table['id']})")
                return table['id']
            else:
                print(f"❌ Failed to create table {name}: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Table creation error: {e}")
            return None

    def create_field(self, table_id, field_config):
        """Create a field in table"""
        try:
            # Check if field exists
            response = self.session.get(f"{self.base_url}/api/database/fields/table/{table_id}/")
            fields = response.json()

            for field in fields:
                if field['name'] == field_config['name']:
                    print(f"  ✅ Found field: {field_config['name']} (ID: {field['id']})")
                    return field['id']

            # Create new field
            response = self.session.post(f"{self.base_url}/api/database/fields/table/{table_id}/", json=field_config)

            if response.status_code == 200:
                field = response.json()
                print(f"  ✅ Created field: {field_config['name']} (ID: {field['id']})")
                return field['id']
            else:
                print(f"  ❌ Failed to create field {field_config['name']}: {response.status_code}")
                return None

        except Exception as e:
            print(f"  ❌ Field creation error: {e}")
            return None

    def setup_pipeline_table(self, table_id):
        """Create all fields for Pipeline table"""
        fields = [
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
            {"name": "estate_value", "type": "text"},
            {"name": "num_beneficiaries", "type": "number", "number_decimal_places": 0},
            {"name": "real_estate_count", "type": "number", "number_decimal_places": 0},
            {"name": "llc_interest", "type": "single_select", "select_options": [
                {"value": "Yes", "color": "green"},
                {"value": "No", "color": "red"},
                {"value": "Maybe", "color": "orange"}
            ]},
            {"name": "urgency_score", "type": "rating", "max_value": 5},
            {"name": "next_steps", "type": "long_text"},
            {"name": "key_pain_points", "type": "long_text"},
            {"name": "has_minor_children", "type": "boolean"},
            {"name": "business_owner", "type": "boolean"}
        ]

        field_ids = {}
        print("Creating Pipeline table fields...")
        for field_config in fields:
            field_id = self.create_field(table_id, field_config)
            if field_id:
                field_ids[field_config['name']] = field_id

        return field_ids

    def setup_followups_table(self, table_id):
        """Create all fields for Follow-ups table"""
        fields = [
            {"name": "client_name", "type": "text"},
            {"name": "email_subject", "type": "text"},
            {"name": "email_body", "type": "long_text"},
            {"name": "status", "type": "single_select", "select_options": [
                {"value": "Draft", "color": "orange"},
                {"value": "Ready", "color": "blue"},
                {"value": "Sent", "color": "green"}
            ]},
            {"name": "created_date", "type": "date", "date_format": "US"}
        ]

        field_ids = {}
        print("Creating Follow-ups table fields...")
        for field_config in fields:
            field_id = self.create_field(table_id, field_config)
            if field_id:
                field_ids[field_config['name']] = field_id

        return field_ids

    def create_test_record(self, table_id, field_ids):
        """Create a test record"""
        try:
            test_data = {}
            # Add some test data using the actual field IDs
            if 'client_name' in field_ids:
                test_data[f"field_{field_ids['client_name']}"] = "Test Client"
            if 'meeting_stage' in field_ids:
                test_data[f"field_{field_ids['meeting_stage']}"] = "Follow Up"
            if 'state' in field_ids:
                test_data[f"field_{field_ids['state']}"] = "TX"

            response = self.session.post(f"{self.base_url}/api/database/rows/table/{table_id}/", json=test_data)

            if response.status_code == 200:
                print("✅ Created test record")
                return True
            else:
                print(f"❌ Test record failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Test record error: {e}")
            return False

    def generate_config(self, pipeline_table_id, pipeline_fields, followups_table_id, followups_fields):
        """Generate config files"""

        # Main config
        config = {
            "baserow_url": self.base_url,
            "api_token": self.token,
            "database_id": self.database_id,
            "tables": {
                "pipeline": {
                    "id": pipeline_table_id,
                    "fields": pipeline_fields
                },
                "followups": {
                    "id": followups_table_id,
                    "fields": followups_fields
                }
            },
            "created": datetime.now().isoformat()
        }

        with open("baserow_config.json", "w") as f:
            json.dump(config, f, indent=2)

        # n8n Settings (simplified)
        n8n_config = {
            "tableId": str(pipeline_table_id),
            "emailTableId": str(followups_table_id),
            "baserowToken": self.token
        }

        with open("n8n_settings.json", "w") as f:
            json.dump(n8n_config, f, indent=2)

        # Field mapping for n8n workflow body
        pipeline_mapping = {}
        for field_name, field_id in pipeline_fields.items():
            pipeline_mapping[f"field_{field_id}"] = f"={{{{ $json.{field_name} }}}}"

        with open("pipeline_field_mapping.json", "w") as f:
            json.dump(pipeline_mapping, f, indent=2)

        print("\n📄 Generated files:")
        print("- baserow_config.json (complete configuration)")
        print("- n8n_settings.json (for n8n Settings node)")
        print("- pipeline_field_mapping.json (for n8n Create Record node)")

    def run(self):
        """Run the complete setup"""
        print("🚀 Baserow Estate Planning CRM Setup")
        print("="*50)

        # Get token
        if not self.get_token():
            return False

        # Setup database
        if not self.get_or_create_database():
            return False

        # Create tables
        pipeline_table_id = self.create_table("Pipeline")
        followups_table_id = self.create_table("Follow-ups")

        if not pipeline_table_id or not followups_table_id:
            return False

        # Setup fields
        pipeline_fields = self.setup_pipeline_table(pipeline_table_id)
        followups_fields = self.setup_followups_table(followups_table_id)

        # Create test record
        self.create_test_record(pipeline_table_id, pipeline_fields)

        # Generate config
        self.generate_config(pipeline_table_id, pipeline_fields, followups_table_id, followups_fields)

        print("\n✅ Setup Complete!")
        print(f"📊 View your tables at: {self.base_url}/database/{self.database_id}")
        print(f"Pipeline table: {pipeline_table_id}")
        print(f"Follow-ups table: {followups_table_id}")

        return True

def main():
    setup = SimpleBaserowSetup()

    try:
        if setup.run():
            print("\n🎉 Ready for n8n integration!")
            print("Next: Update your n8n workflow with the generated config files")
        else:
            print("\n❌ Setup failed")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()