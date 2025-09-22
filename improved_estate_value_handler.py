#!/usr/bin/env python3
"""
Improved Estate Value Constraint Handler
Provides robust handling for Baserow unique constraint on estate_value field
"""

import hashlib
import requests

def handle_estate_value_constraint(base_value, client_name="", attempt=0):
    """
    Handle Baserow estate value unique constraint with intelligent variations

    Args:
        base_value: The actual estate value (e.g., 2000000)
        client_name: Client name for generating consistent variation
        attempt: Retry attempt number for collision handling

    Returns:
        Modified estate value that avoids constraint violations
    """
    if not base_value or base_value == 0:
        return 0

    # Generate consistent variation based on client name + attempt
    if client_name:
        # Combine name and attempt for unique hash
        hash_input = f"{client_name}_{attempt}".encode()
        name_hash = hashlib.md5(hash_input).hexdigest()
        variation = int(name_hash[:3], 16) % 1000  # 0-999 variation
    else:
        import random
        random.seed(base_value + attempt)  # Deterministic random
        variation = random.randint(1, 999)

    # Apply appropriate variation based on estate size
    if base_value >= 10000000:  # $10M+
        return base_value + variation + (attempt * 1000)
    elif base_value >= 1000000:  # $1M+
        return base_value + variation + (attempt * 100)
    elif base_value >= 100000:  # $100K+
        return base_value + (variation // 10) + (attempt * 10)
    else:
        return base_value + (variation // 100) + attempt

def add_record_with_retry(payload, max_retries=3):
    """
    Add record to Baserow with automatic retry for constraint violations
    """
    client_name = payload.get('field_6755', '')
    original_estate_value = payload.get('field_6759', 0)

    for attempt in range(max_retries):
        # Adjust estate value for this attempt
        if attempt > 0:
            adjusted_value = handle_estate_value_constraint(
                original_estate_value,
                client_name,
                attempt
            )
            payload['field_6759'] = adjusted_value
            print(f"🔄 Retry {attempt}: Adjusting estate value to ${adjusted_value:,}")

        try:
            response = requests.post(
                'http://localhost/api/database/rows/table/698/',
                headers={
                    'Authorization': 'Token h9JNHcGxmXZRIICUjpbHvVcKc5geaASA',
                    'Content-Type': 'application/json'
                },
                json=payload,
                timeout=30
            )

            if response.status_code in [200, 201]:
                record_data = response.json()
                record_id = record_data.get('id')
                final_value = payload.get('field_6759', 0)

                print(f"✅ Successfully added {client_name}")
                print(f"📋 Record ID: {record_id}")
                print(f"💰 Estate Value: ${final_value:,}")
                if attempt > 0:
                    print(f"🔧 Constraint resolved after {attempt} retries")

                return record_data

            elif response.status_code == 400 and "constraint" in response.text.lower():
                if attempt < max_retries - 1:
                    print(f"⚠️  Constraint violation detected, retrying...")
                    continue
                else:
                    print(f"❌ Max retries exceeded for constraint violations")
                    return None
            else:
                print(f"❌ Failed to add record: {response.status_code}")
                print(f"Response: {response.text}")
                return None

        except Exception as e:
            print(f"❌ Error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                return None

    return None

def test_estate_value_handler():
    """Test the estate value handler with common scenarios"""
    print("🧪 Testing Estate Value Handler")
    print("=" * 40)

    test_cases = [
        (2000000, "Amanda Jennings"),
        (2000000, "John Smith"),      # Same value, different client
        (1500000, "Sarah Johnson"),
        (3000000, "Mike Wilson"),
        (2000000, "Test Client"),     # Same value again
    ]

    print("Estate Value Variations:")
    for value, name in test_cases:
        for attempt in range(3):
            modified = handle_estate_value_constraint(value, name, attempt)
            print(f"  {name} (attempt {attempt}): ${value:,} → ${modified:,}")
        print()

if __name__ == "__main__":
    test_estate_value_handler()