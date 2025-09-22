#!/usr/bin/env python3
"""
Test each field individually to identify the constraint issue
"""

import requests
import json

def test_fields_individually():
    """Test each field one by one to find the problematic field"""

    headers = {"Authorization": "Token h9JNHcGxmXZRIICUjpbHvVcKc5geaASA"}

    # The data that was failing
    test_data = {
        "field_6755": "Alan Reinhard",
        "field_6756": 2987,  # meeting_stage
        "field_6757": 2989,  # marital_status
        "field_6758": 1,  # children_count
        "field_6759": 2000000,  # estate_value
        "field_6760": 1,  # real_estate_count
        "field_6761": 0,  # llc_interest
        "field_6762": "Estate planning consultation",  # pain_points
        "field_6763": "",  # objections
        "field_6764": 5,  # urgency_score
        "field_6765": True,  # follow_up_required
        "field_6766": "Alan Reinhard: Estate Planning Advisor Meeting.txt",  # transcript_file
        "field_6767": "2025-08-15",  # processed_date
        "field_6768": 3011  # state
    }

    # Test each field incrementally
    print("Testing fields incrementally...")
    print("=" * 60)

    accumulated_data = {}

    for field_id, field_value in test_data.items():
        accumulated_data[field_id] = field_value

        print(f"\n🔍 Testing with {field_id}: {field_value}")

        response = requests.patch(
            "http://localhost/api/database/rows/table/698/5/",
            headers={**headers, "Content-Type": "application/json"},
            json=accumulated_data
        )

        if response.status_code == 200:
            print(f"✅ {field_id} successful")
        else:
            print(f"❌ {field_id} FAILED: {response.status_code}")
            print(f"   Error: {response.text}")
            print(f"   This is the problematic field!")

            # Try to understand the issue
            if field_id == "field_6767":  # processed_date
                print("\n💡 Testing different date formats...")

                # Try different formats
                date_formats = [
                    "2025-08-15",
                    "08/15/2025",
                    "2025-08-15T00:00:00",
                    "2025-08-15T00:00:00Z"
                ]

                for date_format in date_formats:
                    test_date_data = accumulated_data.copy()
                    test_date_data["field_6767"] = date_format

                    response = requests.patch(
                        "http://localhost/api/database/rows/table/698/5/",
                        headers={**headers, "Content-Type": "application/json"},
                        json=test_date_data
                    )

                    if response.status_code == 200:
                        print(f"   ✅ Date format '{date_format}' works!")
                        accumulated_data["field_6767"] = date_format
                        break
                    else:
                        print(f"   ❌ Date format '{date_format}' failed")

            else:
                # Remove the problematic field and continue testing
                del accumulated_data[field_id]
                print(f"   Removed {field_id} from data and continuing...")

    print("\n" + "=" * 60)
    print("📊 FINAL WORKING DATA:")
    print(json.dumps(accumulated_data, indent=2))

    return accumulated_data

if __name__ == "__main__":
    working_data = test_fields_individually()

    if working_data:
        print("\n✅ Successfully identified working field combination")
        print(f"✅ {len(working_data)} fields can be updated successfully")