#!/usr/bin/env python3
"""
Focused test on Abbot Ware to debug state and meeting outcome extraction
"""

import re
from hybrid_bmad_extractor import HybridBMADExtractor

def debug_abbot_ware():
    """Debug Abbot Ware extraction step by step"""

    print("🔍 DEBUGGING ABBOT WARE EXTRACTION")
    print("=" * 60)

    # Read transcript
    transcript_file = "/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts/Abbot Ware: Estate Planning Advisor Meeting.txt"

    with open(transcript_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"📄 Transcript length: {len(content)} characters")

    # Debug beginning section for state
    beginning = content[:3000]
    print(f"\n📍 BEGINNING SECTION (first 3000 chars):")
    print(f"First 500 chars: {beginning[:500]}")
    print("...")
    print(f"Last 500 chars: {beginning[-500:]}")

    # Look for location question manually
    location_patterns = [
        r"where.*world.*joining.*from.*today",
        r"where.*are.*you.*joining.*from",
        r"where.*in.*the.*world.*are.*you",
        r"where.*are.*you.*calling.*from",
        r"where.*are.*you.*located",
    ]

    print(f"\n🔍 MANUAL LOCATION QUESTION SEARCH:")
    for pattern in location_patterns:
        matches = re.findall(pattern, beginning, re.IGNORECASE)
        if matches:
            print(f"✅ Found location question pattern: {pattern}")
            print(f"   Matches: {matches}")

    # Search for South Carolina specifically
    print(f"\n🔍 MANUAL SOUTH CAROLINA SEARCH:")
    sc_patterns = [
        r"south\s+carolina",
        r"s\.?\s*c\.?",
        r"\bsc\b",
        r"carolina",
    ]

    for pattern in sc_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 100)
            context = content[start:end]
            print(f"✅ Found '{match.group()}' at position {match.start()}")
            print(f"   Context: ...{context}...")
            print()

    # Debug end section for meeting outcome
    ending = content[-4000:]
    print(f"\n📍 ENDING SECTION (last 4000 chars):")
    print(f"First 500 chars: {ending[:500]}")
    print("...")
    print(f"Last 500 chars: {ending[-500:]}")

    # Look for commitment patterns manually
    commitment_patterns = [
        r"let's\s+do\s+it",
        r"perfect.*let's\s+do\s+that",
        r"sounds\s+good",
        r"that\s+sounds\s+perfect",
        r"i'm\s+ready",
        r"let's\s+move\s+forward",
        r"absolutely",
        r"yes.*that\s+works",
    ]

    print(f"\n🔍 MANUAL COMMITMENT PATTERN SEARCH:")
    for pattern in commitment_patterns:
        matches = re.finditer(pattern, ending, re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 50)
            end = min(len(ending), match.end() + 50)
            context = ending[start:end]
            print(f"✅ Found commitment pattern '{match.group()}' at position {match.start()}")
            print(f"   Context: ...{context}...")
            print()

    # Now test with hybrid extractor
    print(f"\n🤖 HYBRID EXTRACTOR TEST:")
    print("-" * 40)

    extractor = HybridBMADExtractor()
    results = extractor.extract_comprehensive(content, "Abbot Ware")

    print(f"\n📊 EXPECTED vs ACTUAL:")
    expected = {
        'state': 'South Carolina',
        'meeting_stage': 'Closed Won'
    }

    for field, expected_value in expected.items():
        actual_value = results.get(field)
        status = "✅ CORRECT" if actual_value == expected_value else "❌ INCORRECT"
        print(f"   {field}: {actual_value} (expected: {expected_value}) {status}")

if __name__ == "__main__":
    debug_abbot_ware()