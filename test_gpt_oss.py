#!/usr/bin/env python3
"""Test gpt-oss:20b model for estate planning analysis"""

import requests
import json

def test_gpt_oss():
    """Test the gpt-oss:20b model with a sample estate planning query"""

    print("🧪 Testing gpt-oss:20b Model")
    print("-" * 40)

    # Test prompt
    test_prompt = """
    Extract estate planning information from this transcript excerpt:

    "John Smith, age 65, married to Jane for 40 years. They have 3 adult children
    and 5 grandchildren. Estate value approximately $3.5 million including primary
    residence worth $800k and rental property worth $500k. Concerned about estate
    taxes and wants to ensure smooth transition to children."
    """

    # Prepare request
    payload = {
        "model": "gpt-oss:20b",
        "prompt": test_prompt,
        "system": "You are an expert estate planning analyst. Extract key information in JSON format.",
        "temperature": 0.1,
        "stream": False
    }

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ gpt-oss:20b is working!")
            print("\nSample response:")
            print(result.get('response', '')[:500])
        else:
            print(f"❌ Error: {response.status_code}")

    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_gpt_oss()
