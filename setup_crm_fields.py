#!/usr/bin/env python3
import requests
import json

# Your configuration
TOKEN = "h9JNHcGxmXZRIICUjpbHvVcKc5geaASA"
DATABASE_ID = "174"
CRM_TABLE_ID = "698"  # From your screenshot
BASE_URL = "http://localhost"

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

print("🚀 Setting up Estate Planning CRM fields...")

# First check existing fields
print(f"Checking existing fields in CRM table {CRM_TABLE_ID}...")
fields_response = requests.get(
    f"{BASE_URL}/api/database/fields/table/{CRM_TABLE_ID}/",
    headers=headers
)

if fields_response.status_code == 200:
    existing_fields = fields_response.json()
    print(f"✅ Found {len(existing_fields)} existing fields:")
    field_names = [field['name'] for field in existing_fields]
    for field in existing_fields:
        print(f"  - {field['name']} ({field['type']})")

    # Define estate planning fields to add
    estate_planning_fields = [
        {"name": "meeting_stage", "type": "single_select", "select_options": [
            {"value": "Closed Won", "color": "green"},
            {"value": "Closed Lost", "color": "red"},
            {"value": "No Show", "color": "gray"},
            {"value": "Follow Up", "color": "blue"}
        ]},
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

    print(f"\n📝 Adding estate planning fields...")
    added_fields = []

    for field in estate_planning_fields:
        if field['name'] not in field_names:
            field_response = requests.post(
                f"{BASE_URL}/api/database/fields/table/{CRM_TABLE_ID}/",
                headers=headers,
                json=field
            )
            if field_response.status_code == 200:
                new_field = field_response.json()
                print(f"  ✅ Added field: {field['name']} (ID: {new_field['id']})")
                added_fields.append(new_field)
            else:
                print(f"  ❌ Failed to add field {field['name']}: {field_response.status_code}")
                if field_response.status_code != 200:
                    print(f"     Error: {field_response.text}")
        else:
            print(f"  ⚠️ Field already exists: {field['name']}")

    # Get updated field list
    print(f"\n🔄 Getting updated field list...")
    updated_fields_response = requests.get(
        f"{BASE_URL}/api/database/fields/table/{CRM_TABLE_ID}/",
        headers=headers
    )

    if updated_fields_response.status_code == 200:
        all_fields = updated_fields_response.json()

        # Generate configuration
        config = {
            "baserow": {
                "base_url": BASE_URL,
                "database_id": DATABASE_ID,
                "token": TOKEN,
                "tables": {
                    "CRM": {
                        "id": CRM_TABLE_ID,
                        "fields": {}
                    }
                }
            }
        }

        for field in all_fields:
            config["baserow"]["tables"]["CRM"]["fields"][field['name']] = field['id']

        # Save configuration
        with open("baserow_config.json", "w") as f:
            json.dump(config, f, indent=2)

        print(f"✅ Configuration saved to baserow_config.json")
        print(f"\n🎉 Estate Planning CRM setup complete!")
        print(f"Database ID: {DATABASE_ID}")
        print(f"CRM Table ID: {CRM_TABLE_ID}")
        print(f"Total fields: {len(all_fields)}")
        print(f"New fields added: {len(added_fields)}")

        # Create a sample record to test
        print(f"\n🧪 Creating test record...")
        test_data = {
            "Name": "Test Client",
            "meeting_stage": "Follow Up",
            "marital_status": "Married",
            "children_count": 2,
            "estate_value": 500000.00,
            "has_real_estate": True,
            "has_business": False,
            "urgency_score": 8,
            "follow_up_required": True
        }

        # Only include fields that exist
        filtered_data = {}
        for key, value in test_data.items():
            if key in config["baserow"]["tables"]["CRM"]["fields"] or key == "Name":
                filtered_data[key] = value

        test_response = requests.post(
            f"{BASE_URL}/api/database/rows/table/{CRM_TABLE_ID}/",
            headers=headers,
            json=filtered_data
        )

        if test_response.status_code == 200:
            print(f"✅ Test record created successfully")
        else:
            print(f"⚠️ Test record creation failed: {test_response.status_code}")

    else:
        print(f"❌ Failed to get updated fields: {updated_fields_response.status_code}")

else:
    print(f"❌ Failed to get existing fields: {fields_response.status_code}")
    print(fields_response.text)