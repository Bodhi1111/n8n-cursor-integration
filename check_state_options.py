#!/usr/bin/env python3
"""
Check state field options
"""

import requests

headers = {"Authorization": "Token h9JNHcGxmXZRIICUjpbHvVcKc5geaASA"}

response = requests.get(
    "http://localhost/api/database/fields/table/698/",
    headers=headers
)

if response.status_code == 200:
    fields = response.json()
    state_field = next((f for f in fields if f['name'] == 'state'), None)

    if state_field:
        print(f"State field type: {state_field['type']}")
        print(f"State field ID: {state_field['id']}")
        print(f"\nState field options:")

        if 'select_options' in state_field:
            for opt in state_field['select_options']:
                if opt['value'] == 'Maryland':
                    print(f"✅ Maryland: ID={opt['id']}, value={opt['value']}")

            # Check if 3011 exists
            if any(opt['id'] == 3011 for opt in state_field['select_options']):
                print(f"✅ Option ID 3011 exists")
            else:
                print(f"❌ Option ID 3011 does NOT exist")

            # Show all available IDs
            print(f"\nAll state option IDs: {[opt['id'] for opt in state_field['select_options'][:10]]}")
        else:
            print("No select_options in state field")