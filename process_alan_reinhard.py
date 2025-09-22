#!/usr/bin/env python3
"""
Process Alan Reinhard with hyper-aggressive extraction and meeting date detection
"""

import json
import requests
import re
from datetime import datetime

def extract_meeting_datetime(transcript_content):
    """Extract actual meeting date and time from transcript"""

    print("📅 EXTRACTING MEETING DATE & TIME...")

    # Look for date patterns in transcript
    date_patterns = [
        r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',  # 2025-07-11T21:00:00
        r'(\d{4}-\d{2}-\d{2})',  # 2025-07-11
        r'(\d{1,2}/\d{1,2}/\d{4})',  # 7/11/2025 or 07/11/2025
    ]

    meeting_date = None
    for pattern in date_patterns:
        matches = re.findall(pattern, transcript_content[:2000])  # Check first 2000 chars
        if matches:
            meeting_date = matches[0]
            print(f"✅ Found meeting date: {meeting_date}")
            break

    if not meeting_date:
        # Fallback: today's date
        meeting_date = datetime.now().strftime("%Y-%m-%d")
        print(f"⚠️  No date found, using today: {meeting_date}")

    return meeting_date

def hyper_aggressive_extraction(transcript_content, client_name):
    """Hyper-aggressive extraction based on lessons learned"""

    print(f"🎯 HYPER-AGGRESSIVE EXTRACTION: {client_name}")
    print("=" * 70)

    # STRATEGY: Use multiple ultra-specific prompts
    results = {}

    # 1. HYPER-SPECIFIC AGE EXTRACTION
    age_prompt = f"""FIND THE CLIENT'S AGE. Look for these EXACT phrases:
- "I'm 65", "I am 65"
- "65 years old"
- "I turned 65"
- "I'm in my 60s", "I'm in my 70s"
- "65-year-old"

CLIENT NAME: {client_name}
TRANSCRIPT: {transcript_content[:3000]}

If you find an age, respond with ONLY the number. If not found, respond with "NONE".
Age: """

    # 2. HYPER-SPECIFIC MARITAL STATUS
    marital_prompt = f"""FIND MARITAL STATUS. Look for these EXACT phrases:
- "my wife", "my husband"
- "I'm married", "I am married"
- "I'm single", "I am single"
- "my spouse"
- "I'm divorced", "I'm widowed"
- "my ex-wife", "my ex-husband"

CLIENT: {client_name}
TRANSCRIPT: {transcript_content[:3000]}

Respond with ONLY: Married, Single, Divorced, Widowed, or NONE
Status: """

    # 3. HYPER-SPECIFIC CHILDREN COUNT
    children_prompt = f"""COUNT THE CLIENT'S CHILDREN. Look for:
- "my son", "my daughter"
- "3 children", "3 kids"
- "I have 2 boys"
- "my oldest son", "my youngest daughter"
- Count mentions of children/kids/sons/daughters

CLIENT: {client_name}
TRANSCRIPT: {transcript_content[:3000]}

Respond with ONLY the number of children. If none mentioned, respond with "0".
Children: """

    # 4. HYPER-SPECIFIC ESTATE VALUE
    estate_prompt = f"""FIND ESTATE VALUE. Look for these EXACT phrases:
- "$600,000", "$600k", "600 thousand"
- "half a million", "1.3 million"
- "worth about", "estate of"
- "my assets are worth"
- Any dollar amounts related to total wealth/estate

CLIENT: {client_name}
TRANSCRIPT: {transcript_content[:4000]}

Respond with ONLY the number (no $ or commas). If not found, respond with "NONE".
Value: """

    # 5. HYPER-SPECIFIC STATE DETECTION
    state_prompt = f"""FIND THE US STATE. Look for:
- Direct state names: Georgia, Florida, Texas, California, South Carolina, Vermont, etc.
- Cities that indicate states
- "I live in", "I'm from"
- Area codes

CLIENT: {client_name}
TRANSCRIPT: {transcript_content[:2000]}

Respond with ONLY the state name. If not found, respond with "NONE".
State: """

    # Execute all extractions
    prompts = [
        ("Age", age_prompt),
        ("Marital Status", marital_prompt),
        ("Children Count", children_prompt),
        ("Estate Value", estate_prompt),
        ("State", state_prompt)
    ]

    for field_name, prompt in prompts:
        print(f"\n🔍 Extracting {field_name}...")

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "gpt-oss:20b",
                    "prompt": prompt,
                    "temperature": 0.01,
                    "stream": False
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()['response'].strip()
                print(f"   Raw response: {result}")

                # Process the response
                if field_name == "Age":
                    if result.isdigit():
                        results['age'] = int(result)
                        print(f"   ✅ Age: {result}")
                    else:
                        print(f"   ❌ Age not found")

                elif field_name == "Marital Status":
                    valid_statuses = ["Married", "Single", "Divorced", "Widowed"]
                    for status in valid_statuses:
                        if status.lower() in result.lower():
                            results['marital_status'] = status
                            print(f"   ✅ Marital Status: {status}")
                            break

                elif field_name == "Children Count":
                    if result.isdigit():
                        results['children_count'] = int(result)
                        print(f"   ✅ Children: {result}")

                elif field_name == "Estate Value":
                    # Try to extract number from response
                    numbers = re.findall(r'(\d+(?:,\d{3})*)', result)
                    if numbers:
                        value = int(numbers[0].replace(',', ''))
                        results['estate_value'] = value
                        print(f"   ✅ Estate Value: ${value:,}")

                elif field_name == "State":
                    us_states = [
                        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
                        'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                        'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
                        'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                        'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                        'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                        'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
                        'Wisconsin', 'Wyoming'
                    ]

                    for state in us_states:
                        if state.lower() in result.lower():
                            results['state'] = state
                            print(f"   ✅ State: {state}")
                            break

        except Exception as e:
            print(f"   ❌ Error extracting {field_name}: {e}")

    return results

def process_alan_reinhard():
    """Process Alan Reinhard with improved extraction"""

    print("🧪 TESTING: Alan Reinhard (Improved Extraction)")
    print("=" * 70)

    # Read transcript
    transcript_file = "/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts/Alan Reinhard: Estate Planning Advisor Meeting.txt"

    with open(transcript_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"📄 Transcript length: {len(content)} characters")

    # Extract meeting date
    meeting_date = extract_meeting_datetime(content)

    # Hyper-aggressive extraction
    extracted_data = hyper_aggressive_extraction(content, "Alan Reinhard")

    # Add defaults for missing data
    final_data = {
        "client_name": "Alan Reinhard",
        "age": extracted_data.get('age'),
        "marital_status": extracted_data.get('marital_status', 'Unknown'),
        "children_count": extracted_data.get('children_count', 0),
        "estate_value": extracted_data.get('estate_value', 0),
        "state": extracted_data.get('state'),
        "meeting_date": meeting_date,
        "meeting_stage": "Follow Up",  # Default, will update based on your notes
        "real_estate_count": 1,  # Default
        "llc_interest": 0,  # Default
        "urgency_score": 5,  # Default
        "pain_points": "Estate planning consultation needs"
    }

    print(f"\n📊 EXTRACTION SUMMARY:")
    for key, value in final_data.items():
        if value and value not in ['Unknown', 0, None]:
            print(f"   ✅ {key}: {value}")
        else:
            print(f"   ⚠️  {key}: {value} (default/missing)")

    # Find next available row
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

    if next_row_id:
        print(f"\n💾 Creating record in row {next_row_id}...")

        # Prepare data for Baserow
        update_data = {
            "field_6755": final_data["client_name"],  # lead_name
            "field_6756": 2987,  # meeting_stage (Follow Up default)
            "field_6757": 2988,  # marital_status (Single default)
            "field_6758": final_data["children_count"],  # children_count
            "field_6759": final_data["estate_value"],  # estate_value
            "field_6760": final_data["real_estate_count"],  # real_estate_count
            "field_6761": final_data["llc_interest"],  # llc_interest
            "field_6762": final_data["pain_points"],  # pain_points
            "field_6763": "",  # objections
            "field_6764": final_data["urgency_score"],  # urgency_score
            "field_6765": True,  # follow_up_required
            "field_6766": "Alan Reinhard: Estate Planning Advisor Meeting.txt",  # transcript_file
            "field_6767": final_data["meeting_date"]  # processed_date (now actual meeting date)
        }

        # Add option IDs if we found them
        if final_data.get('marital_status') == 'Married':
            update_data["field_6757"] = 2989
        if final_data.get('age'):
            # Update pain points to include age
            update_data["field_6762"] = f"{final_data['age']}-year-old client. {final_data['pain_points']}"

        # Create the record
        create_response = requests.patch(
            f"http://localhost/api/database/rows/table/698/{next_row_id}/",
            headers={**headers, "Content-Type": "application/json"},
            json=update_data
        )

        if create_response.status_code == 200:
            print(f"✅ Alan Reinhard record created in row {next_row_id}!")
            print(f"🔗 View at: http://localhost/database/174/table/698/{next_row_id}")
            return next_row_id, final_data
        else:
            print(f"❌ Failed to create record: {create_response.status_code}")
            return None, final_data
    else:
        print("❌ No available rows")
        return None, final_data

if __name__ == "__main__":
    row_id, data = process_alan_reinhard()

    if row_id:
        print("\n" + "=" * 70)
        print("✅ ALAN REINHARD PROCESSED")
        print("=" * 70)
        print(f"✅ Record created in row {row_id}")
        print("✅ Meeting date extracted and used instead of process date")
        print("✅ Hyper-aggressive extraction implemented")
        print("\n📋 Please provide your notes for Alan Reinhard to verify accuracy!")
    else:
        print("\n❌ Processing failed")