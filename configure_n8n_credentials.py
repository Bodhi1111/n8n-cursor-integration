#!/usr/bin/env python3
"""
Configure n8n credentials for the BMAD Estate Planning workflow
"""

import requests
import json
import time
from datetime import datetime

def configure_n8n_credentials():
    """Configure all required credentials in n8n"""

    n8n_base_url = "http://localhost:5678"

    print("🔧 Configuring n8n Credentials for BMAD Workflow")
    print("=" * 50)

    # Load existing Baserow config
    try:
        with open("baserow_config.json", "r") as f:
            baserow_config = json.load(f)
        print("✅ Loaded Baserow configuration")
    except Exception as e:
        print(f"❌ Error loading Baserow config: {e}")
        return False

    # Credential configurations
    credentials = {
        "baserow": {
            "name": "Baserow - Estate Planning CRM",
            "type": "baserowApi",
            "data": {
                "host": baserow_config["baserow"]["base_url"],
                "username": "",  # Not needed for token auth
                "password": "",  # Not needed for token auth
                "token": baserow_config["baserow"]["token"]
            }
        },
        "openai": {
            "name": "OpenAI - BMAD Analysis",
            "type": "openAiApi",
            "data": {
                "apiKey": "sk-placeholder-key",  # You'll need to add your actual key
                "organizationId": ""
            }
        },
        "ollama": {
            "name": "Ollama - Local GPT",
            "type": "httpBasicAuth",
            "data": {
                "baseUrl": "http://localhost:11434",
                "username": "",
                "password": ""
            }
        }
    }

    print("\n📝 Credential Setup Instructions:")
    print("-" * 40)

    # Since n8n doesn't have a direct API for credentials, provide manual steps
    print("\n1. BASEROW CREDENTIALS:")
    print("   - Go to n8n → Credentials → Add Credential")
    print("   - Search for 'HTTP Request'")
    print("   - Name: 'Baserow - Estate Planning CRM'")
    print("   - Authentication: 'Header Auth'")
    print("   - Name: 'Authorization'")
    print(f"   - Value: 'Token {baserow_config['baserow']['token']}'")
    print("   - Save the credential")

    print("\n2. OPENAI CREDENTIALS (if using GPT-4):")
    print("   - Go to n8n → Credentials → Add Credential")
    print("   - Search for 'OpenAI'")
    print("   - Name: 'OpenAI - BMAD Analysis'")
    print("   - API Key: [Your OpenAI API key]")
    print("   - Save the credential")

    print("\n3. OLLAMA CREDENTIALS (for local models):")
    print("   - No credentials needed - Ollama runs locally")
    print("   - Ensure Ollama is running: http://localhost:11434")

    # Create a configuration file for the workflow
    workflow_config = {
        "baserow": {
            "url": baserow_config["baserow"]["base_url"],
            "token": baserow_config["baserow"]["token"],
            "database_id": baserow_config["baserow"]["database_id"],
            "table_id": baserow_config["baserow"]["tables"]["CRM"]["id"]
        },
        "ollama": {
            "url": "http://localhost:11434",
            "model": "llama2"  # or whatever model you have
        },
        "webhook": {
            "url": f"{n8n_base_url}/webhook/bmad-estate-planning",
            "test_url": f"{n8n_base_url}/webhook-test/bmad-estate-planning"
        },
        "transcripts": {
            "directory": "/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts",
            "total_count": 352
        }
    }

    # Save workflow configuration
    with open("n8n_workflow_config.json", "w") as f:
        json.dump(workflow_config, f, indent=2)
    print("\n✅ Created n8n_workflow_config.json")

    # Create a helper script to update workflow nodes
    update_script = """
// Paste this into n8n's browser console to update node configurations

const updateWorkflowNodes = () => {
    const baserowToken = '""" + baserow_config["baserow"]["token"] + """';
    const baserowUrl = '""" + baserow_config["baserow"]["base_url"] + """';
    const tableId = '""" + str(baserow_config["baserow"]["tables"]["CRM"]["id"]) + """';

    // Update all HTTP Request nodes that connect to Baserow
    const httpNodes = window.$store.getters.workflow.nodes.filter(n => n.type === 'n8n-nodes-base.httpRequest');

    httpNodes.forEach(node => {
        if (node.name.toLowerCase().includes('baserow')) {
            console.log('Updating node:', node.name);
            // This would update the node parameters
            // You'll need to manually select the credential in the UI
        }
    });

    console.log('Please manually update each Baserow node with:');
    console.log('- URL: ' + baserowUrl + '/api/database/rows/table/' + tableId + '/');
    console.log('- Authentication: Predefined Credential');
    console.log('- Credential: Baserow - Estate Planning CRM');
};

updateWorkflowNodes();
"""

    with open("update_workflow_nodes.js", "w") as f:
        f.write(update_script)
    print("✅ Created update_workflow_nodes.js helper script")

    print("\n" + "=" * 50)
    print("📋 NEXT STEPS:")
    print("=" * 50)

    print("\n1. Open n8n at http://localhost:5678")
    print("2. Create the credentials as described above")
    print("3. Open your 'bmad-n8n-cursor' workflow")
    print("4. For each node that needs credentials:")
    print("   - Click on the node")
    print("   - Select the appropriate credential from dropdown")
    print("   - Update any URLs or parameters as needed")

    print("\n5. Key nodes to update:")
    print("   - 'Read Transcript Content' → Set file path")
    print("   - 'Save to Baserow CRM' → Select Baserow credential")
    print("   - 'Create Follow-up Email' → Select Baserow credential")
    print("   - 'LLM Analyzer - Batch' → Select OpenAI or configure for Ollama")

    print("\n6. Test the workflow:")
    print("   - Click 'Execute Workflow'")
    print("   - Monitor the execution")

    return True

def create_quick_test():
    """Create a quick test script"""

    test_script = """#!/usr/bin/env python3
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
"""

    with open("test_connections.py", "w") as f:
        f.write(test_script)

    import os
    os.chmod("test_connections.py", 0o755)
    print("\n✅ Created test_connections.py")

if __name__ == "__main__":
    configure_n8n_credentials()
    create_quick_test()

    print("\n🧪 Testing connections...")
    print("-" * 40)
    import subprocess
    subprocess.run(["python3", "test_connections.py"])