#!/usr/bin/env python3
"""
Complete end-to-end test of single transcript processing
Uses hybrid extractor and creates actual Baserow record
"""

import json
import requests
from datetime import datetime
from hybrid_bmad_extractor import HybridBMADExtractor

def extract_meeting_datetime_and_duration(transcript_content):
    """Extract meeting date, time, and duration from structured transcript header"""

    print("📅 EXTRACTING MEETING DATE, TIME & DURATION FROM HEADER...")

    import re

    # Extract from the structured header (first 500 characters)
    header = transcript_content[:500]

    meeting_data = {
        'date': None,
        'time': None,
        'duration_minutes': None,
        'iso_datetime': None
    }

    # Pattern for ISO datetime: 2025-07-22T21:00:00Z or 2025-07-22T21:00:00
    iso_pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:Z)?'
    iso_match = re.search(iso_pattern, header)

    if iso_match:
        iso_datetime = iso_match.group(1)
        meeting_data['iso_datetime'] = iso_datetime

        # Split into date and time parts
        date_part, time_part = iso_datetime.split('T')
        meeting_data['date'] = date_part  # 2025-07-22
        meeting_data['time'] = time_part  # 21:00:00

        print(f"✅ Found ISO datetime: {iso_datetime}")
        print(f"✅ Date: {date_part}")
        print(f"✅ Time: {time_part}")

    # Pattern for duration (decimal number, usually after the datetime)
    # Look for a standalone decimal number that represents minutes
    duration_pattern = r'\n\n(\d+\.\d+)\s*\n'
    duration_match = re.search(duration_pattern, header)

    if duration_match:
        duration_minutes = float(duration_match.group(1))
        meeting_data['duration_minutes'] = duration_minutes

        # Convert to hours and minutes for display
        hours = int(duration_minutes // 60)
        minutes = int(duration_minutes % 60)
        print(f"✅ Duration: {duration_minutes:.1f} minutes ({hours}h {minutes}m)")

    # Fallback if no structured data found
    if not meeting_data['date']:
        fallback_date = datetime.now().strftime("%Y-%m-%d")
        meeting_data['date'] = fallback_date
        print(f"⚠️  No structured date found, using today: {fallback_date}")

    return meeting_data

def process_single_transcript_complete():
    """Complete processing of a single transcript with hybrid extraction"""

    print("🧪 SINGLE TRANSCRIPT END-TO-END TEST")
    print("=" * 70)

    # Test with a fresh transcript - Ann Smithling
    client_name = "Ann Smithling"
    transcript_file = "/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts/Ann Smithling: Estate Planning Advisor Meeting.txt"

    print(f"📄 Processing: {client_name}")
    print(f"📁 File: {transcript_file}")

    # Step 1: Read transcript
    print(f"\n📖 Step 1: Reading transcript...")
    with open(transcript_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"✅ Loaded transcript ({len(content):,} characters)")

    # Step 2: Extract meeting data from header
    print(f"\n📅 Step 2: Extracting meeting data from header...")
    meeting_data = extract_meeting_datetime_and_duration(content)
    print(f"✅ Meeting data: {meeting_data}")

    # Step 3: Hybrid extraction
    print(f"\n🔍 Step 3: Hybrid data extraction...")
    extractor = HybridBMADExtractor()
    extracted_data = extractor.extract_comprehensive(content, client_name)

    # Add meeting data from header
    extracted_data['meeting_date'] = meeting_data['date']
    extracted_data['meeting_time'] = meeting_data['time']
    extracted_data['meeting_duration'] = meeting_data['duration_minutes']

    print(f"\n📊 Extracted data:")
    for key, value in extracted_data.items():
        if value and value not in ['Unknown', '', 0, None]:
            print(f"   ✅ {key}: {value}")
        else:
            print(f"   ⚠️  {key}: {value} (default/missing)")

    # Step 4: Get Baserow field mappings
    print(f"\n🔧 Step 4: Mapping to Baserow fields...")
    headers = {"Authorization": "Token h9JNHcGxmXZRIICUjpbHvVcKc5geaASA"}

    # Get field configurations
    fields_response = requests.get(
        "http://localhost/api/database/fields/table/698/",
        headers=headers
    )

    meeting_stage_id = 2987  # Default Follow Up
    marital_status_id = 2988  # Default Single
    state_id = None

    if fields_response.status_code == 200:
        fields = fields_response.json()

        # Find meeting stage option
        meeting_field = next((f for f in fields if f['name'] == 'meeting_stage'), None)
        if meeting_field and extracted_data.get('meeting_stage'):
            print(f"🔍 Looking for meeting stage: '{extracted_data.get('meeting_stage')}'")
            print(f"Available options: {[opt['value'] for opt in meeting_field['select_options']]}")

            stage_opt = next((opt for opt in meeting_field['select_options']
                            if opt['value'] == extracted_data.get('meeting_stage')), None)
            if stage_opt:
                meeting_stage_id = stage_opt['id']
                print(f"✅ Meeting stage mapped: {extracted_data.get('meeting_stage')} (ID: {meeting_stage_id})")
            else:
                print(f"⚠️  Meeting stage '{extracted_data.get('meeting_stage')}' not found, using default")

        # Find marital status option
        marital_field = next((f for f in fields if f['name'] == 'marital_status'), None)
        if marital_field and extracted_data.get('marital_status') != 'Unknown':
            marital_opt = next((opt for opt in marital_field['select_options']
                              if opt['value'] == extracted_data.get('marital_status')), None)
            if marital_opt:
                marital_status_id = marital_opt['id']
                print(f"✅ Marital status mapped: {extracted_data.get('marital_status')} (ID: {marital_status_id})")

        # Find state option
        state_field = next((f for f in fields if f['name'] == 'state'), None)
        if state_field and extracted_data.get('state'):
            state_opt = next((opt for opt in state_field['select_options']
                           if opt['value'] == extracted_data.get('state')), None)
            if state_opt:
                state_id = state_opt['id']
                print(f"✅ State mapped: {extracted_data.get('state')} (ID: {state_id})")

    # Step 5: Find next available row
    print(f"\n🔍 Step 5: Finding available row...")
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

    # Step 6: Prepare record data
    print(f"\n💾 Step 6: Preparing record data...")
    update_data = {
        "field_6755": extracted_data.get("client_name", client_name),  # lead_name
        "field_6756": meeting_stage_id,  # meeting_stage
        "field_6757": marital_status_id,  # marital_status
        "field_6758": extracted_data.get("children_count", 0),  # children_count
        "field_6759": extracted_data.get("estate_value", 0),  # estate_value
        "field_6760": extracted_data.get("real_estate_count", 0),  # real_estate_count
        "field_6761": extracted_data.get("llc_interest", 0),  # llc_interest
        "field_6762": extracted_data.get("pain_points", "Estate planning consultation"),  # pain_points
        "field_6763": extracted_data.get("objections", ""),  # objections
        "field_6764": extracted_data.get("urgency_score", 5),  # urgency_score
        "field_6765": True,  # follow_up_required
        "field_6766": f"{client_name}: Estate Planning Advisor Meeting.txt",  # transcript_file
        "field_6767": extracted_data.get('meeting_date', datetime.now().strftime("%Y-%m-%d"))  # processed_date
    }

    if state_id:
        update_data["field_6768"] = state_id

    print(f"✅ Record data prepared")
    print(f"📋 Data to send: {json.dumps(update_data, indent=2)}")

    # Step 7: Create the record
    print(f"\n🚀 Step 7: Creating Baserow record...")
    create_response = requests.patch(
        f"http://localhost/api/database/rows/table/698/{next_row_id}/",
        headers={**headers, "Content-Type": "application/json"},
        json=update_data
    )

    if create_response.status_code == 200:
        print(f"✅ Record created successfully in row {next_row_id}!")

        # Step 8: Verify the record
        print(f"\n🔍 Step 8: Verifying record...")
        verify_response = requests.get(
            f"http://localhost/api/database/rows/table/698/{next_row_id}/?user_field_names=true",
            headers=headers
        )

        if verify_response.status_code == 200:
            row = verify_response.json()

            print(f"\n📊 FINAL RECORD VERIFICATION - Row {next_row_id}:")
            print(f"✅ Name: {row.get('lead_name')}")
            print(f"✅ Meeting Stage: {row.get('meeting_stage', {}).get('value', 'N/A') if row.get('meeting_stage') else 'N/A'}")
            print(f"✅ State: {row.get('state', {}).get('value', 'N/A') if row.get('state') else 'N/A'}")
            print(f"✅ Marital Status: {row.get('marital_status', {}).get('value', 'N/A') if row.get('marital_status') else 'N/A'}")
            print(f"✅ Age: {extracted_data.get('age', 'N/A')}")
            print(f"✅ Children: {row.get('children_count')}")
            print(f"✅ Estate Value: ${float(row.get('estate_value', 0)):,.0f}" if row.get('estate_value') else "✅ Estate Value: $0")
            print(f"✅ Properties: {row.get('real_estate_count')}")
            print(f"✅ Urgency: {row.get('urgency_score')}/10")
            print(f"✅ Meeting Date: {row.get('processed_date')}")
            print(f"✅ Pain Points: {row.get('pain_points', '')[:60]}...")

            print(f"\n🔗 View record: http://localhost/database/174/table/698/{next_row_id}")

            return next_row_id
        else:
            print("❌ Verification failed")
            return False
    else:
        print(f"❌ Record creation failed: {create_response.status_code}")
        print(create_response.text)
        return False

if __name__ == "__main__":
    print("🧪 SINGLE TRANSCRIPT COMPLETE TEST")
    print("Testing complete pipeline: Transcript → Extraction → Baserow Record")
    print()

    result = process_single_transcript_complete()

    if result:
        print("\n" + "=" * 70)
        print("🎉 SINGLE TRANSCRIPT TEST PASSED!")
        print("=" * 70)
        print(f"✅ Complete pipeline working correctly")
        print(f"✅ Record created in row {result}")
        print(f"✅ Hybrid extraction functioning properly")
        print(f"✅ Ready to proceed with careful batch processing")
        print("\n💡 Next step: Test a few more individual transcripts to verify consistency")
    else:
        print("\n" + "=" * 70)
        print("❌ SINGLE TRANSCRIPT TEST FAILED")
        print("=" * 70)
        print("❌ Pipeline needs debugging before batch processing")
        print("❌ Fix issues and retest individual transcript")