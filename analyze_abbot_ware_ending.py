#!/usr/bin/env python3
"""
Analyze Abbot Ware transcript ending to identify Closed Won patterns
"""

def analyze_abbot_ware_ending():
    """Analyze the ending to understand what makes it Closed Won"""

    # Read transcript
    transcript_file = "/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts/Abbot Ware: Estate Planning Advisor Meeting.txt"

    with open(transcript_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look at the last 6000 characters to find commitment/transaction
    ending_section = content[-6000:]

    print("🔍 ANALYZING ABBOT WARE ENDING FOR CLOSED WON INDICATORS")
    print("=" * 80)

    # Split into manageable chunks
    chunks = [ending_section[i:i+1000] for i in range(0, len(ending_section), 1000)]

    for i, chunk in enumerate(chunks):
        print(f"\n📄 CHUNK {i+1} (Characters {i*1000}-{(i+1)*1000}):")
        print("-" * 60)
        print(chunk)
        print("-" * 60)

    # Look for specific transaction-related keywords
    print(f"\n🔍 SEARCHING FOR TRANSACTION INDICATORS:")

    transaction_keywords = [
        'payment', 'card', 'visa', 'mastercard', 'charge', 'billing',
        'process', 'transaction', 'schedule', 'next meeting', 'client meeting',
        'pull the trigger', 'go ahead', 'proceed', 'move forward',
        'money back guarantee', 'taken care of'
    ]

    for keyword in transaction_keywords:
        if keyword.lower() in ending_section.lower():
            print(f"✅ Found: '{keyword}'")
            # Find context around this keyword
            import re
            for match in re.finditer(re.escape(keyword), ending_section, re.IGNORECASE):
                start = max(0, match.start() - 100)
                end = min(len(ending_section), match.end() + 100)
                context = ending_section[start:end]
                print(f"   Context: ...{context}...")
                print()

if __name__ == "__main__":
    analyze_abbot_ware_ending()