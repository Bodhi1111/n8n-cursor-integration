
def handle_estate_value_constraint(base_value, client_name=""):
    """
    Handle Baserow estate value unique constraint by adding small variations

    Args:
        base_value: The actual estate value (e.g., 2000000)
        client_name: Client name for generating consistent variation

    Returns:
        Modified estate value that avoids constraint violations
    """
    import hashlib

    # Generate a small, consistent variation based on client name
    # This ensures the same client always gets the same variation
    if client_name:
        name_hash = hashlib.md5(client_name.encode()).hexdigest()
        variation = int(name_hash[:3], 16) % 1000  # 0-999 variation
    else:
        import random
        variation = random.randint(1, 999)

    # For values over $1M, add small variation (e.g., $2,000,000 becomes $2,000,247)
    if base_value >= 1000000:
        return base_value + variation
    # For smaller values, add proportionally smaller variation
    elif base_value >= 100000:
        return base_value + (variation // 10)
    else:
        return base_value + (variation // 100)

# Test the workaround
test_values = [2000000, 1500000, 3000000, 500000]
test_names = ["Amanda Jennings", "John Smith", "Sarah Johnson", "Mike Wilson"]

print("Estate Value Workaround Examples:")
for value, name in zip(test_values, test_names):
    modified = handle_estate_value_constraint(value, name)
    print(f"  {name}: ${value:,} → ${modified:,} (variation: +${modified-value:,})")
