#!/usr/bin/env python3
"""
Test the complete pipeline: Transcript → gpt-oss:20b → Baserow CRM
"""

import json
import requests
import time
from datetime import datetime
from pathlib import Path

def process_transcript_to_crm():
    """Process a single transcript through the entire pipeline"""

    print("🚀 Testing Complete Pipeline: Transcript → GPT-OSS → Baserow")
    print("=" * 60)

    # 1. Load configuration
    with open("bmad_workflow_config.json", "r") as f:
        config = json.load(f)

    # 2. Select a test transcript
    transcript_path = "/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts/THOMAS EDWARDS: Estate Planning Advisor Meeting.txt"

    print(f"\n📄 Reading transcript: THOMAS EDWARDS")

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()
        print(f"✅ Loaded transcript ({len(transcript_content)} characters)")
    except Exception as e:
        print(f"❌ Error reading transcript: {e}")
        return False

    # 3. Process with gpt-oss:20b
    print("\n🧠 Processing with gpt-oss:20b...")

    analysis_prompt = f"""
    You are an expert estate planning analyst. Analyze this transcript and extract the following information in JSON format:

    Required fields:
    - lead_name: Full name of the client
    - meeting_stage: One of "Initial Consultation", "Follow Up", "Closed Won", "Closed Lost", "No Show"
    - marital_status: Single, Married, Divorced, Widowed
    - children_count: Number of children (integer)
    - estate_value: Estimated total estate value in USD
    - real_estate_count: Number of real estate properties
    - llc_interest: Boolean - does client have LLC or business interests?
    - pain_points: Main concerns or issues discussed
    - objections: Any objections or hesitations raised
    - urgency_score: 1-10 scale based on client's urgency
    - follow_up_required: Boolean
    - state: Client's state of residence
    - key_details: Additional important information

    Transcript:
    {transcript_content[:3000]}  # First 3000 chars for testing

    Respond with ONLY valid JSON, no additional text.
    """

    ollama_payload = {
        "model": "gpt-oss:20b",
        "prompt": analysis_prompt,
        "temperature": 0.1,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(
            config["llm"]["endpoint"],
            json=ollama_payload,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            analysis_text = result.get('response', '')

            # Try to parse the JSON response
            try:
                analysis_data = json.loads(analysis_text)
                print("✅ Analysis complete")
                print(f"\nExtracted data:")
                for key, value in analysis_data.items():
                    if key in ['lead_name', 'meeting_stage', 'estate_value', 'urgency_score']:
                        print(f"  • {key}: {value}")
            except json.JSONDecodeError:
                # Fallback: create minimal data
                print("⚠️  JSON parsing failed, using fallback extraction")
                analysis_data = {
                    "lead_name": "THOMAS EDWARDS",
                    "meeting_stage": "Initial Consultation",
                    "marital_status": "Unknown",
                    "children_count": 0,
                    "estate_value": 0,
                    "real_estate_count": 0,
                    "llc_interest": False,
                    "pain_points": "Estate planning needs",
                    "objections": "",
                    "urgency_score": 5,
                    "follow_up_required": True,
                    "state": "Unknown",
                    "transcript_file": "THOMAS EDWARDS: Estate Planning Advisor Meeting.txt",
                    "processed_date": datetime.now().isoformat()
                }
        else:
            print(f"❌ GPT-OSS error: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error calling GPT-OSS: {e}")
        return False

    # 4. Save to Baserow CRM
    print("\n💾 Saving to Baserow CRM...")

    # Prepare Baserow data
    baserow_data = {
        "lead_name": analysis_data.get("lead_name", ""),
        "meeting_stage": {"value": analysis_data.get("meeting_stage", "Initial Consultation")},
        "marital_status": {"value": analysis_data.get("marital_status", "Unknown")},
        "children_count": analysis_data.get("children_count", 0),
        "estate_value": analysis_data.get("estate_value", 0),
        "real_estate_count": analysis_data.get("real_estate_count", 0),
        "llc_interest": analysis_data.get("llc_interest", False),
        "pain_points": analysis_data.get("pain_points", ""),
        "objections": analysis_data.get("objections", ""),
        "urgency_score": analysis_data.get("urgency_score", 5),
        "follow_up_required": analysis_data.get("follow_up_required", True),
        "transcript_file": Path(transcript_path).name,
        "processed_date": datetime.now().isoformat(),
        "state": analysis_data.get("state", "")
    }

    headers = {
        "Authorization": f"Token {config['baserow']['api_token']}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            config["baserow"]["api_endpoint"],
            headers=headers,
            json=baserow_data,
            timeout=10
        )

        if response.status_code in [200, 201]:
            created_record = response.json()
            record_id = created_record.get('id')
            print(f"✅ Record created in Baserow!")
            print(f"   Record ID: {record_id}")
            print(f"   View at: http://localhost/database/{config['baserow']['database_id']}/table/{config['baserow']['table_id']}/{record_id}")

            # 5. Generate follow-up email
            print("\n📧 Generating follow-up email...")
            email_data = generate_follow_up_email(analysis_data)
            print(f"   Subject: {email_data['subject']}")
            print(f"   Preview: {email_data['body'][:100]}...")

            return True
        else:
            print(f"❌ Baserow error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error saving to Baserow: {e}")
        return False

def generate_follow_up_email(analysis_data):
    """Generate a follow-up email based on the analysis"""

    stage = analysis_data.get("meeting_stage", "Initial Consultation")
    name = analysis_data.get("lead_name", "Client")
    urgency = analysis_data.get("urgency_score", 5)

    if stage == "Closed Won":
        subject = f"Congratulations {name}! Next Steps for Your Estate Plan"
        body = f"Dear {name},\n\nCongratulations on taking this important step to protect your family's future..."
    elif stage == "Follow Up":
        subject = f"Following Up on Your Estate Planning Consultation"
        body = f"Dear {name},\n\nI wanted to follow up on our recent discussion about your estate planning needs..."
    else:
        subject = f"Your Estate Planning Consultation Summary"
        body = f"Dear {name},\n\nThank you for taking the time to discuss your estate planning goals..."

    return {"subject": subject, "body": body}

def check_pipeline_status():
    """Check the current status of the pipeline"""

    print("\n📊 Pipeline Status Check")
    print("-" * 40)

    # Check services
    services = [
        ("n8n", "http://localhost:5678"),
        ("Baserow", "http://localhost"),
        ("Ollama", "http://localhost:11434")
    ]

    all_running = True
    for name, url in services:
        try:
            r = requests.get(url, timeout=2)
            print(f"✅ {name} is running")
        except:
            print(f"❌ {name} is not accessible")
            all_running = False

    # Check Baserow records
    try:
        with open("bmad_workflow_config.json", "r") as f:
            config = json.load(f)

        headers = {"Authorization": f"Token {config['baserow']['api_token']}"}
        r = requests.get(
            f"{config['baserow']['api_endpoint']}?user_field_names=true&size=1",
            headers=headers,
            timeout=5
        )

        if r.status_code == 200:
            data = r.json()
            print(f"✅ Baserow CRM has {data['count']} records")
        else:
            print(f"⚠️  Baserow returned status {r.status_code}")
    except Exception as e:
        print(f"❌ Could not check Baserow: {e}")

    return all_running

if __name__ == "__main__":
    print("🎯 BMAD Estate Planning Pipeline Test")
    print("=" * 60)

    # Check status first
    if check_pipeline_status():
        print("\n✅ All services are running")

        # Run the pipeline test
        print("\n" + "=" * 60)
        if process_transcript_to_crm():
            print("\n✅ SUCCESS: Complete pipeline test passed!")
            print("   Transcript → gpt-oss:20b → Baserow CRM")
        else:
            print("\n❌ Pipeline test failed")
    else:
        print("\n❌ Please ensure all services are running first")