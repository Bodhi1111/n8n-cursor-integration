#!/usr/bin/env python3
import requests
import json

# Your configuration
TOKEN = "h9JNHcGxmXZRIICUjpbHvVcKc5geaASA"
DATABASE_ID = "174"
BASE_URL = "http://localhost"

# Correct format according to the documentation
headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

print("Testing authentication...")
# Test with the CRM table endpoint shown in the documentation
response = requests.get(
    f"{BASE_URL}/api/database/rows/table/698/",
    headers=headers
)

if response.status_code == 200:
    print("✅ Authentication successful!")

    # Now create additional tables
    # Get list of existing tables first
    tables_response = requests.get(
        f"{BASE_URL}/api/database/tables/database/{DATABASE_ID}/",
        headers=headers
    )

    if tables_response.status_code == 200:
        print("✅ Can access database tables")
        existing_tables = tables_response.json()
        print(f"Found {len(existing_tables)} existing tables:")
        for table in existing_tables:
            print(f"  - {table['name']} (ID: {table['id']})")

        # Check if we need to create Pipeline table
        pipeline_exists = any(t['name'] == 'Pipeline' for t in existing_tables)
        email_queue_exists = any(t['name'] == 'Email Queue' for t in existing_tables)

        # Create Pipeline table if it doesn't exist
        if not pipeline_exists:
            print("\nCreating Pipeline table...")
            pipeline_data = {
                "name": "Pipeline"
            }
            pipeline_response = requests.post(
                f"{BASE_URL}/api/database/tables/database/{DATABASE_ID}/",
                headers=headers,
                json=pipeline_data
            )

            if pipeline_response.status_code == 200:
                pipeline_table = pipeline_response.json()
                print(f"✅ Created Pipeline table (ID: {pipeline_table['id']})")
                pipeline_table_id = pipeline_table['id']

                # Add fields to Pipeline table
                pipeline_fields = [
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
                        {"value": "Widowed", "color": "gray"},
                        {"value": "Divorced", "color": "orange"}
                    ]},
                    {"name": "children_count", "type": "number", "number_negative": False},
                    {"name": "estate_value", "type": "number", "number_negative": False, "number_decimal_places": 2},
                    {"name": "has_real_estate", "type": "boolean"},
                    {"name": "has_business", "type": "boolean"},
                    {"name": "pain_points", "type": "long_text"},
                    {"name": "objections", "type": "long_text"},
                    {"name": "urgency_score", "type": "rating", "max_value": 10},
                    {"name": "follow_up_required", "type": "boolean"},
                    {"name": "transcript_file", "type": "text"},
                    {"name": "processed_date", "type": "date_time", "date_include_time": True}
                ]

                print("Adding fields to Pipeline table...")
                for field in pipeline_fields:
                    field_response = requests.post(
                        f"{BASE_URL}/api/database/fields/table/{pipeline_table_id}/",
                        headers=headers,
                        json=field
                    )
                    if field_response.status_code == 200:
                        print(f"  ✅ Added field: {field['name']}")
                    else:
                        print(f"  ❌ Failed to add field {field['name']}: {field_response.status_code}")
            else:
                print(f"❌ Failed to create Pipeline table: {pipeline_response.status_code}")
        else:
            print("Pipeline table already exists")

        # Create Email Queue table if it doesn't exist
        if not email_queue_exists:
            print("\nCreating Email Queue table...")
            email_data = {
                "name": "Email Queue"
            }
            email_response = requests.post(
                f"{BASE_URL}/api/database/tables/database/{DATABASE_ID}/",
                headers=headers,
                json=email_data
            )

            if email_response.status_code == 200:
                email_table = email_response.json()
                print(f"✅ Created Email Queue table (ID: {email_table['id']})")
                email_table_id = email_table['id']

                # Add fields to Email Queue table
                email_fields = [
                    {"name": "client_name", "type": "text"},
                    {"name": "email_to", "type": "email"},
                    {"name": "email_subject", "type": "text"},
                    {"name": "email_body", "type": "long_text"},
                    {"name": "email_type", "type": "single_select", "select_options": [
                        {"value": "Welcome", "color": "green"},
                        {"value": "Follow Up", "color": "blue"},
                        {"value": "Re-engagement", "color": "orange"},
                        {"value": "Close Lost", "color": "red"}
                    ]},
                    {"name": "send_date", "type": "date_time", "date_include_time": True},
                    {"name": "sent", "type": "boolean"},
                    {"name": "pipeline_link", "type": "link_row", "link_row_table_id": pipeline_table_id if not pipeline_exists else next(t['id'] for t in existing_tables if t['name'] == 'Pipeline')}
                ]

                print("Adding fields to Email Queue table...")
                for field in email_fields:
                    field_response = requests.post(
                        f"{BASE_URL}/api/database/fields/table/{email_table_id}/",
                        headers=headers,
                        json=field
                    )
                    if field_response.status_code == 200:
                        print(f"  ✅ Added field: {field['name']}")
                    else:
                        print(f"  ❌ Failed to add field {field['name']}: {field_response.status_code}")
            else:
                print(f"❌ Failed to create Email Queue table: {email_response.status_code}")
        else:
            print("Email Queue table already exists")

        # Generate configuration file
        print("\n📝 Generating configuration file...")
        config = {
            "baserow": {
                "base_url": BASE_URL,
                "database_id": DATABASE_ID,
                "token": TOKEN,
                "tables": {}
            }
        }

        # Get final table list with IDs
        final_tables = requests.get(
            f"{BASE_URL}/api/database/tables/database/{DATABASE_ID}/",
            headers=headers
        ).json()

        for table in final_tables:
            config["baserow"]["tables"][table['name']] = {
                "id": table['id'],
                "fields": {}
            }

            # Get field IDs
            fields_response = requests.get(
                f"{BASE_URL}/api/database/fields/table/{table['id']}/",
                headers=headers
            )
            if fields_response.status_code == 200:
                for field in fields_response.json():
                    config["baserow"]["tables"][table['name']]["fields"][field['name']] = field['id']

        # Save configuration
        with open("baserow_config.json", "w") as f:
            json.dump(config, f, indent=2)

        print("✅ Configuration saved to baserow_config.json")
        print("\n🎉 Baserow setup complete!")
        print(f"Database ID: {DATABASE_ID}")
        print(f"Tables created/verified:")
        for table_name in config["baserow"]["tables"]:
            print(f"  - {table_name} (ID: {config['baserow']['tables'][table_name]['id']})")

    else:
        print(f"❌ Failed to get tables: {tables_response.status_code}")
        print(tables_response.text)
else:
    print(f"❌ Authentication failed: {response.status_code}")
    print(response.text)