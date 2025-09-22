#!/usr/bin/env python3
"""
Test minimal Baserow update to identify constraint issue
"""

import requests

def test_minimal_update():
    """Test minimal Baserow update"""

    headers = {"Authorization": "Token h9JNHcGxmXZRIICUjpbHvVcKc5geaASA"}

    # Try just updating the name field
    minimal_data = {
        "field_6755": "Test Client"  # lead_name only
    }

    print("Testing minimal update with just name...")

    response = requests.patch(
        "http://localhost/api/database/rows/table/698/5/",
        headers={**headers, "Content-Type": "application/json"},
        json=minimal_data
    )

    if response.status_code == 200:
        print("✅ Minimal update successful")

        # Now try adding meeting stage
        stage_data = {
            "field_6755": "Test Client",
            "field_6756": 2987  # Follow Up
        }

        print("Testing with meeting stage...")
        response2 = requests.patch(
            "http://localhost/api/database/rows/table/698/5/",
            headers={**headers, "Content-Type": "application/json"},
            json=stage_data
        )

        if response2.status_code == 200:
            print("✅ Meeting stage update successful")
        else:
            print(f"❌ Meeting stage failed: {response2.status_code}")
            print(response2.text)

    else:
        print(f"❌ Minimal update failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_minimal_update()