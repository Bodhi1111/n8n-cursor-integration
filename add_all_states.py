#!/usr/bin/env python3
"""
Add all 50 US states to the Baserow state field
"""

import requests
import json

def add_all_states():
    """Add all US states to the state field"""

    print("🇺🇸 Adding All 50 US States to Baserow")
    print("=" * 50)

    # All 50 US states with District of Columbia
    all_states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
        "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
        "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
        "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
        "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
        "New Hampshire", "New Jersey", "New Mexico", "New York",
        "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
        "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
        "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
        "West Virginia", "Wisconsin", "Wyoming", "Washington DC"
    ]

    # Create select options with colors
    colors = [
        "light-blue", "light-green", "light-orange", "light-purple", "light-red",
        "light-brown", "light-gray", "blue", "green", "orange", "purple", "red",
        "brown", "gray", "dark-blue", "dark-green", "dark-orange", "dark-purple",
        "dark-red", "dark-brown", "dark-gray"
    ]

    select_options = []
    for i, state in enumerate(all_states):
        color = colors[i % len(colors)]
        select_options.append({
            "value": state,
            "color": color
        })

    # Update the state field with all options
    headers = {
        "Authorization": "Token h9JNHcGxmXZRIICUjpbHvVcKc5geaASA",
        "Content-Type": "application/json"
    }

    print(f"📍 Adding {len(all_states)} states to the field...")

    response = requests.patch(
        "http://localhost/api/database/fields/table/698/6768/",
        headers=headers,
        json={"select_options": select_options}
    )

    if response.status_code == 200:
        print("✅ All US states added successfully!")

        # Get the Georgia option ID
        updated_field = response.json()
        georgia_option = next((opt for opt in updated_field['select_options'] if opt['value'] == 'Georgia'), None)

        if georgia_option:
            georgia_id = georgia_option['id']
            print(f"✅ Georgia option created with ID: {georgia_id}")

            # Now update Thomas Edwards with Closed Won and Georgia
            print("\n🔄 Updating Thomas Edwards with correct meeting stage and state...")

            update_data = {
                "field_6756": 2984,  # Closed Won
                "field_6768": georgia_id  # Georgia
            }

            update_response = requests.patch(
                "http://localhost/api/database/rows/table/698/1/",
                headers=headers,
                json=update_data
            )

            if update_response.status_code == 200:
                print("✅ Thomas Edwards updated with:")
                print("   • Meeting Stage: Closed Won")
                print("   • State: Georgia")
                return True
            else:
                print(f"❌ Failed to update Thomas Edwards: {update_response.status_code}")
                return False
        else:
            print("❌ Georgia option not found in response")
            return False
    else:
        print(f"❌ Failed to add states: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    if add_all_states():
        print("\n" + "=" * 50)
        print("🎉 SUCCESS! Complete setup:")
        print("=" * 50)
        print("✅ All 50 US states available in dropdown")
        print("✅ Thomas Edwards set to 'Closed Won'")
        print("✅ Thomas Edwards location set to 'Georgia'")
        print("\n📋 Now any transcript can be assigned to any US state!")
    else:
        print("\n❌ Setup failed")