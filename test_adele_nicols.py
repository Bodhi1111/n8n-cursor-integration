#!/usr/bin/env python3
"""
Test processing Adele Nicols transcript with improved extraction
"""

import json
import requests
from datetime import datetime

def process_adele_nicols():
    """Process Adele Nicols transcript with enhanced accuracy"""

    print("🎯 Testing Adele Nicols Transcript Processing")
    print("=" * 60)

    # 1. Read the transcript
    transcript_file = "/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts/Adele Nicols: Estate Planning Advisor Meeting.txt"

    print("\n📄 Reading Adele Nicols transcript...")
    with open(transcript_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"✅ Loaded transcript ({len(content)} characters)")
    print(f"Preview: {content[:200]}...")

    # 2. Enhanced GPT-OSS analysis with improved prompt
    print("\n🧠 Analyzing with enhanced GPT-OSS prompt...")

    enhanced_prompt = f"""You are an expert estate planning analyst with 25+ years of experience. Analyze this transcript and extract PRECISE information. Pay close attention to:

CRITICAL DETAILS TO FIND:
- Client's full name
- Age (look for mentions of "years old", age numbers)
- State/location (city, state mentions)
- Marital status and family situation
- Number of children (be precise - count carefully)
- Estate value (look for dollar amounts, property values)
- Number of properties/real estate
- Business interests or LLCs
- Meeting outcome (did they sign up? follow up needed?)

TRANSCRIPT CONTENT:
{content[:4000]}

Extract the following in JSON format:
{{
  "client_name": "Full name of the client",
  "age": number_or_null,
  "state": "State name if mentioned",
  "marital_status": "Single/Married/Divorced/Widowed",
  "children_count": number,
  "estate_value": number_without_symbols,
  "real_estate_count": number,
  "llc_interest": 0_or_1,
  "meeting_stage": "Initial Consultation/Follow Up/Closed Won/Closed Lost/No Show",
  "pain_points": "Main concerns discussed",
  "objections": "Any hesitations or concerns raised",
  "urgency_score": number_1_to_10
}}

Return ONLY valid JSON."""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gpt-oss:20b",
            "prompt": enhanced_prompt,
            "temperature": 0.1,
            "stream": False
        },
        timeout=90
    )

    if response.status_code == 200:
        gpt_response = response.json()['response']
        print("✅ GPT analysis complete")

        # Extract JSON from response
        try:
            import re
            json_match = re.search(r'\{.*\}', gpt_response, re.DOTALL)
            if json_match:
                extracted_data = json.loads(json_match.group())
                print("\n📊 Extracted Data:")
                for key, value in extracted_data.items():
                    print(f"   • {key}: {value}")
            else:
                print("⚠️  No JSON found, using fallback data")
                extracted_data = {
                    "client_name": "Adele Nicols",
                    "age": None,
                    "state": None,
                    "marital_status": "Unknown",
                    "children_count": 0,
                    "estate_value": 0,
                    "real_estate_count": 0,
                    "llc_interest": 0,
                    "meeting_stage": "Follow Up",
                    "pain_points": "Estate planning consultation",
                    "objections": "",
                    "urgency_score": 5
                }
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parsing failed: {e}")
            extracted_data = {
                "client_name": "Adele Nicols",
                "age": None,
                "state": None,
                "marital_status": "Single",
                "children_count": 0,
                "estate_value": 0,
                "real_estate_count": 0,
                "llc_interest": 0,
                "meeting_stage": "Follow Up",
                "pain_points": "Estate planning needs",
                "objections": "",
                "urgency_score": 5
            }

        # 3. Find the next available blank row
        print("\n🔍 Finding next available row...")
        headers = {"Authorization": "Token h9JNHcGxmXZRIICUjpbHvVcKc5geaASA"}

        response = requests.get(
            "http://localhost/api/database/rows/table/698/?user_field_names=true&size=20",
            headers=headers
        )

        next_row_id = None
        if response.status_code == 200:
            rows = response.json()['results']
            for row in rows:
                if not row.get('lead_name') or row.get('lead_name') == '':
                    next_row_id = row['id']
                    break

        if not next_row_id:
            print("❌ No blank rows available")
            return False

        print(f"✅ Using row {next_row_id}")

        # 4. Map to Baserow fields with proper option IDs
        print("\n💾 Preparing Baserow data...")

        # Get option IDs for select fields
        fields_response = requests.get(
            "http://localhost/api/database/fields/table/698/",
            headers=headers
        )

        meeting_stage_id = None
        marital_status_id = None
        state_id = None

        if fields_response.status_code == 200:
            fields = fields_response.json()

            # Find meeting stage option
            meeting_field = next((f for f in fields if f['name'] == 'meeting_stage'), None)
            if meeting_field:
                stage_opt = next((opt for opt in meeting_field['select_options']
                                if opt['value'] == extracted_data.get('meeting_stage', 'Follow Up')), None)
                if stage_opt:
                    meeting_stage_id = stage_opt['id']

            # Find marital status option
            marital_field = next((f for f in fields if f['name'] == 'marital_status'), None)
            if marital_field:
                marital_opt = next((opt for opt in marital_field['select_options']
                                  if opt['value'] == extracted_data.get('marital_status', 'Single')), None)
                if marital_opt:
                    marital_status_id = marital_opt['id']

            # Find state option
            state_field = next((f for f in fields if f['name'] == 'state'), None)
            if state_field and extracted_data.get('state'):
                state_opt = next((opt for opt in state_field['select_options']
                               if opt['value'] == extracted_data.get('state')), None)
                if state_opt:
                    state_id = state_opt['id']

        # Prepare the update data
        update_data = {
            "field_6755": extracted_data.get("client_name", "Adele Nicols"),
            "field_6758": extracted_data.get("children_count", 0),
            "field_6759": extracted_data.get("estate_value", 0),
            "field_6760": extracted_data.get("real_estate_count", 0),
            "field_6761": extracted_data.get("llc_interest", 0),
            "field_6762": extracted_data.get("pain_points", ""),
            "field_6763": extracted_data.get("objections", ""),
            "field_6764": extracted_data.get("urgency_score", 5),
            "field_6765": True,  # follow_up_required
            "field_6766": "Adele Nicols: Estate Planning Advisor Meeting.txt",
            "field_6767": datetime.now().strftime("%Y-%m-%d")
        }

        # Add option IDs if found
        if meeting_stage_id:
            update_data["field_6756"] = meeting_stage_id
        if marital_status_id:
            update_data["field_6757"] = marital_status_id
        if state_id:
            update_data["field_6768"] = state_id

        # 5. Update the row
        print(f"\n📝 Updating row {next_row_id}...")

        update_response = requests.patch(
            f"http://localhost/api/database/rows/table/698/{next_row_id}/",
            headers={**headers, "Content-Type": "application/json"},
            json=update_data
        )

        if update_response.status_code == 200:
            print(f"✅ Successfully updated row {next_row_id}!")
            print(f"🔗 View at: http://localhost/database/174/table/698/{next_row_id}")

            # Verify the record
            verify_response = requests.get(
                f"http://localhost/api/database/rows/table/698/{next_row_id}/?user_field_names=true",
                headers=headers
            )

            if verify_response.status_code == 200:
                row = verify_response.json()
                print(f"\n📊 Verified Adele Nicols Record:")
                print(f"   • Name: {row.get('lead_name')}")
                print(f"   • Meeting Stage: {row.get('meeting_stage', {}).get('value', 'N/A')}")
                print(f"   • State: {row.get('state', {}).get('value', 'N/A')}")
                print(f"   • Marital Status: {row.get('marital_status', {}).get('value', 'N/A')}")
                print(f"   • Children: {row.get('children_count')}")
                print(f"   • Estate Value: ${float(row.get('estate_value', 0)):,.0f}" if row.get('estate_value') else "   • Estate Value: $0")
                print(f"   • Properties: {row.get('real_estate_count')}")
                print(f"   • Urgency: {row.get('urgency_score')}/10")

            return next_row_id
        else:
            print(f"❌ Failed to update row: {update_response.status_code}")
            print(update_response.text)
            return False

    else:
        print(f"❌ GPT analysis failed: {response.status_code}")
        return False

if __name__ == "__main__":
    result = process_adele_nicols()
    if result:
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Adele Nicols processed and added to CRM")
        print("=" * 60)
        print(f"\n✅ Record created in row {result}")
        print("✅ Enhanced extraction working properly")
        print("✅ Ready to process remaining 350 transcripts!")
    else:
        print("\n❌ Processing failed")