#!/usr/bin/env python3
import requests
import json

# Test Baserow connection
def test_baserow():
    config = json.load(open('baserow_config.json'))
    headers = {
        "Authorization": f"Token {config['baserow']['token']}"
    }

    url = f"{config['baserow']['base_url']}/api/database/tables/"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("✅ Baserow connection successful")
        return True
    else:
        print(f"❌ Baserow connection failed: {response.status_code}")
        return False

# Test Ollama connection
def test_ollama():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            print("✅ Ollama connection successful")
            models = response.json().get('models', [])
            if models:
                print(f"   Available models: {', '.join([m['name'] for m in models])}")
            return True
    except:
        print("❌ Ollama connection failed")
        return False

# Test n8n connection
def test_n8n():
    try:
        response = requests.get("http://localhost:5678")
        if response.status_code in [200, 302]:
            print("✅ n8n is running")
            return True
    except:
        print("❌ n8n is not accessible")
        return False

print("🧪 Testing Service Connections")
print("=" * 40)
test_n8n()
test_baserow()
test_ollama()
