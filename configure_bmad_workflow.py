#!/usr/bin/env python3
"""
Configure BMAD n8n workflow with gpt-oss:20b and Baserow
"""

import json
import os
from datetime import datetime

def configure_bmad_workflow():
    """Generate configuration for n8n workflow using gpt-oss:20b"""

    print("🎯 Configuring BMAD Workflow for n8n")
    print("=" * 50)

    # Load existing Baserow config
    with open("baserow_config.json", "r") as f:
        baserow_config = json.load(f)

    # Create comprehensive workflow configuration
    workflow_config = {
        "llm": {
            "model": "gpt-oss:20b",
            "endpoint": "http://localhost:11434/api/generate",
            "temperature": 0.1,
            "max_tokens": 2000,
            "system_prompt": "You are an expert estate planning analyst with 25+ years experience."
        },
        "baserow": {
            "base_url": baserow_config["baserow"]["base_url"],
            "api_token": baserow_config["baserow"]["token"],
            "database_id": baserow_config["baserow"]["database_id"],
            "table_id": baserow_config["baserow"]["tables"]["CRM"]["id"],
            "api_endpoint": f"{baserow_config['baserow']['base_url']}/api/database/rows/table/{baserow_config['baserow']['tables']['CRM']['id']}/"
        },
        "transcripts": {
            "directory": "/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts",
            "file_pattern": "*.txt",
            "batch_size": 10,
            "total_files": 352
        },
        "webhook": {
            "production": "http://localhost:5678/webhook/bmad-estate-planning",
            "test": "http://localhost:5678/webhook-test/bmad-estate-planning"
        },
        "processing": {
            "parallel_batches": 3,
            "retry_attempts": 3,
            "quality_threshold": 75,
            "auto_approve_threshold": 90
        }
    }

    # Save workflow configuration
    with open("bmad_workflow_config.json", "w") as f:
        json.dump(workflow_config, f, indent=2)

    print("✅ Created bmad_workflow_config.json")

    # Create n8n credential setup instructions
    print("\n📋 MANUAL CONFIGURATION STEPS FOR N8N:")
    print("=" * 50)

    print("\n1. CREATE HTTP REQUEST CREDENTIAL (for Baserow):")
    print("   • Go to n8n → Credentials → Add Credential")
    print("   • Choose: HTTP Request")
    print("   • Name: 'Baserow API'")
    print("   • Authentication: Header Auth")
    print("   • Header Name: Authorization")
    print(f"   • Header Value: Token {baserow_config['baserow']['token']}")
    print("   • Click 'Save'")

    print("\n2. CREATE HTTP REQUEST CREDENTIAL (for Ollama/gpt-oss):")
    print("   • Go to n8n → Credentials → Add Credential")
    print("   • Choose: HTTP Request")
    print("   • Name: 'Ollama GPT-OSS'")
    print("   • Authentication: None")
    print("   • Click 'Save'")

    print("\n3. UPDATE WORKFLOW NODES:")
    print("   • Open your 'bmad-n8n-cursor' workflow")

    print("\n   A. Update 'Read Transcript Content' node:")
    print("      • File Path: Use expression")
    print(f"      • {{{{ $json.filePath }}}}")

    print("\n   B. Update 'LLM Analyzer - Batch' node:")
    print("      • Change to HTTP Request node")
    print("      • Method: POST")
    print(f"      • URL: {workflow_config['llm']['endpoint']}")
    print("      • Authentication: Ollama GPT-OSS credential")
    print("      • Body (JSON):")

    llm_body = {
        "model": "gpt-oss:20b",
        "prompt": "{{ $json.transcript }}",
        "system": workflow_config["llm"]["system_prompt"],
        "temperature": 0.1,
        "stream": False
    }

    print(f"      {json.dumps(llm_body, indent=6)}")

    print("\n   C. Update 'Save to Baserow CRM' node:")
    print("      • Method: POST")
    print(f"      • URL: {workflow_config['baserow']['api_endpoint']}")
    print("      • Authentication: Baserow API credential")
    print("      • Body: Map extracted fields")

    print("\n   D. Update 'Create Follow-up Email' node:")
    print("      • Method: POST")
    print(f"      • URL: {workflow_config['baserow']['api_endpoint']}")
    print("      • Authentication: Baserow API credential")

    # Create a test script for gpt-oss:20b
    test_script = '''#!/usr/bin/env python3
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
            print("\\nSample response:")
            print(result.get('response', '')[:500])
        else:
            print(f"❌ Error: {response.status_code}")

    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_gpt_oss()
'''

    with open("test_gpt_oss.py", "w") as f:
        f.write(test_script)

    os.chmod("test_gpt_oss.py", 0o755)
    print("\n✅ Created test_gpt_oss.py")

    # Create helper JavaScript for n8n console
    js_helper = """
// Paste this in n8n browser console to quickly update nodes

const updateForGptOss = () => {
    console.log('Updating nodes for gpt-oss:20b configuration...');
    console.log('Baserow API Endpoint: """ + workflow_config['baserow']['api_endpoint'] + """');
    console.log('Ollama Endpoint: """ + workflow_config['llm']['endpoint'] + """');
    console.log('Model: gpt-oss:20b');
    console.log('\\nPlease manually update each node with these values');
};

updateForGptOss();
"""

    with open("n8n_console_helper.js", "w") as f:
        f.write(js_helper)

    print("✅ Created n8n_console_helper.js")

    return workflow_config

def test_services():
    """Test all required services"""

    print("\n🔍 Testing Required Services")
    print("-" * 40)

    # Test n8n
    try:
        r = requests.get("http://localhost:5678", timeout=5)
        print("✅ n8n is running")
    except:
        print("❌ n8n is not accessible")

    # Test Ollama with gpt-oss:20b
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        if r.status_code == 200:
            models = r.json().get('models', [])
            model_names = [m['name'] for m in models]
            if 'gpt-oss:20b' in model_names:
                print("✅ Ollama with gpt-oss:20b is ready")
            else:
                print("⚠️  Ollama is running but gpt-oss:20b not found")
                print(f"   Available models: {', '.join(model_names)}")
    except:
        print("❌ Ollama is not accessible")

    # Test Baserow
    try:
        with open("baserow_config.json", "r") as f:
            config = json.load(f)

        headers = {"Authorization": f"Token {config['baserow']['token']}"}
        r = requests.get(
            f"{config['baserow']['base_url']}/api/database/tables/{config['baserow']['tables']['CRM']['id']}/",
            headers=headers,
            timeout=5
        )

        if r.status_code == 200:
            print("✅ Baserow CRM table is accessible")
        else:
            print(f"⚠️  Baserow returned status {r.status_code}")
    except Exception as e:
        print(f"❌ Baserow connection failed: {e}")

if __name__ == "__main__":
    config = configure_bmad_workflow()
    test_services()

    print("\n" + "=" * 50)
    print("🚀 READY TO CONFIGURE N8N")
    print("=" * 50)
    print("\n1. Follow the manual configuration steps above")
    print("2. Test the workflow with one transcript")
    print("3. Run: python3 test_gpt_oss.py to verify model")
    print("\n✅ Configuration complete!")