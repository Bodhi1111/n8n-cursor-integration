#!/usr/bin/env python3
"""
Test processing a single transcript through the BMAD pipeline
"""

import json
import requests
import sys
from pathlib import Path
from datetime import datetime

def test_single_transcript():
    """Test processing one transcript file"""

    # Configuration
    transcript_file = "/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts/THOMAS EDWARDS: Estate Planning Advisor Meeting.txt"
    # Using workflow 3 production webhook
    n8n_webhook = "http://localhost:5678/webhook/EOUsUYTISkqTDWrr"

    print("🎯 BMAD Single Transcript Test")
    print("=" * 50)

    # Check if file exists
    file_path = Path(transcript_file)
    if not file_path.exists():
        print(f"❌ File not found: {transcript_file}")
        return False

    print(f"📄 Testing with: {file_path.name}")
    print(f"📊 File size: {file_path.stat().st_size} bytes")

    # Read transcript content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()[:500]  # First 500 chars for preview
        print(f"📝 Content preview: {content[:100]}...")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

    # Prepare webhook payload
    payload = {
        "file_path": str(file_path),
        "filename": file_path.name,
        "test_mode": True,
        "triggered_by": "manual_test",
        "timestamp": datetime.now().isoformat()
    }

    print("\n🚀 Triggering BMAD processing...")
    print(f"🔗 Webhook: {n8n_webhook}")

    try:
        # Send to n8n webhook
        response = requests.post(
            n8n_webhook,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            print("✅ Successfully triggered processing!")
            print(f"📨 Response: {response.text[:200]}")

            # Log the test
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "file": str(file_path),
                "status": "test_successful",
                "response_code": response.status_code
            }

            with open("test_processing.log", "a") as f:
                f.write(json.dumps(log_entry) + "\n")

            return True
        else:
            print(f"❌ Processing failed with status: {response.status_code}")
            print(f"📨 Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to n8n webhook")
        print("ℹ️  Make sure n8n workflow with webhook trigger is active")
        print("ℹ️  Webhook URL should be: /webhook/bmad-estate-planning")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 30 seconds")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_processing_results():
    """Check if processing was successful"""
    print("\n🔍 Checking processing results...")

    # Check Baserow for new record
    try:
        # Load config
        with open("baserow_config.json", "r") as f:
            config = json.load(f)

        headers = {
            "Authorization": f"Token {config['api_token']}"
        }

        # Get records from Pipeline table
        response = requests.get(
            f"http://localhost/api/database/rows/table/{config['pipeline_table_id']}/",
            headers=headers,
            params={"user_field_names": "true", "size": 1, "order_by": "-id"}
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                latest = data["results"][0]
                print(f"✅ Latest record in Baserow:")
                print(f"   Client: {latest.get('client_name', 'N/A')}")
                print(f"   Date: {latest.get('meeting_date', 'N/A')}")
                print(f"   Stage: {latest.get('meeting_stage', 'N/A')}")
            else:
                print("ℹ️  No records found in Baserow yet")
        else:
            print(f"⚠️  Could not check Baserow: {response.status_code}")

    except FileNotFoundError:
        print("ℹ️  Baserow config not found - run setup first")
    except Exception as e:
        print(f"⚠️  Error checking results: {e}")

if __name__ == "__main__":
    print("🧪 Starting BMAD Pipeline Test\n")

    # Run the test
    success = test_single_transcript()

    if success:
        # Check results after a delay
        import time
        print("\n⏳ Waiting 5 seconds for processing...")
        time.sleep(5)
        check_processing_results()
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed - check configuration and services")
        sys.exit(1)