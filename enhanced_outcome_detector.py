#!/usr/bin/env python3
"""
Enhanced meeting outcome detection for BMAD agent
Focus specifically on improving Closed Won vs Follow Up accuracy
"""

import requests

def analyze_meeting_outcome_enhanced(transcript_content):
    """Enhanced meeting outcome analysis focusing on the end of the conversation"""

    print("🎯 ENHANCED MEETING OUTCOME ANALYSIS")
    print("=" * 50)

    # Focus on the last part of the conversation where decisions are made
    ending_portion = transcript_content[-5000:]  # Last 5000 characters
    middle_portion = transcript_content[len(transcript_content)//2:len(transcript_content)//2+3000]

    # Ultra-specific outcome detection prompt
    outcome_prompt = f"""You are a sales outcome expert. Analyze ONLY the ending of this conversation to determine if the client COMMITTED or just showed interest.

CRITICAL INDICATORS:
- CLOSED WON: "let's do it", "I'm ready to move forward", "sign me up", "sounds good, let's proceed", "I want to go ahead", definitive agreement
- FOLLOW UP: "let me think about it", "I need to discuss this", "call me back", "maybe", hesitation, uncertainty

CONVERSATION ENDING:
{ending_portion}

Also check this middle section for commitment signals:
{middle_portion}

Based on the CLIENT'S FINAL DECISION, return ONLY:
Closed Won
OR
Follow Up
OR
Closed Lost
OR
No Show

Answer:"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gpt-oss:20b",
                "prompt": outcome_prompt,
                "temperature": 0.01,  # Very low for consistency
                "stream": False
            },
            timeout=45
        )

        if response.status_code == 200:
            outcome = response.json()['response'].strip()
            print(f"✅ Outcome analysis: {outcome}")

            # Validate response
            valid_outcomes = ["Closed Won", "Follow Up", "Closed Lost", "No Show"]
            for valid_outcome in valid_outcomes:
                if valid_outcome.lower() in outcome.lower():
                    return valid_outcome

            # Fallback pattern matching
            outcome_lower = outcome.lower()
            if any(phrase in outcome_lower for phrase in ["won", "closed won", "success", "proceed", "signed"]):
                return "Closed Won"
            elif any(phrase in outcome_lower for phrase in ["follow", "think", "discuss", "call back"]):
                return "Follow Up"
            elif any(phrase in outcome_lower for phrase in ["lost", "declined", "rejected"]):
                return "Closed Lost"
            else:
                return "Follow Up"  # Default

        else:
            print(f"❌ API call failed: {response.status_code}")
            return "Follow Up"

    except Exception as e:
        print(f"❌ Error in outcome analysis: {e}")
        return "Follow Up"

def test_abbot_ware_outcome():
    """Test specifically on Abbot Ware to see if we can detect Closed Won"""

    print("🧪 TESTING: Abbot Ware Meeting Outcome Detection")
    print("=" * 60)

    # Read transcript
    transcript_file = "/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts/Abbot Ware: Estate Planning Advisor Meeting.txt"

    with open(transcript_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"📄 Transcript length: {len(content)} characters")
    print(f"📄 Analyzing last 5000 characters for outcome...")

    # Run enhanced outcome detection
    detected_outcome = analyze_meeting_outcome_enhanced(content)

    print(f"\n📊 DETECTION RESULTS:")
    print(f"   • Detected: {detected_outcome}")
    print(f"   • Expected: Closed Won")

    if detected_outcome == "Closed Won":
        print("✅ CORRECT! Enhanced outcome detection working")
        return True
    else:
        print("❌ INCORRECT! Still not detecting Closed Won properly")

        # Let's examine the actual ending
        print(f"\n📝 TRANSCRIPT ENDING (last 500 chars):")
        print(content[-500:])
        print("\n💡 Manual analysis needed to understand why Closed Won wasn't detected")
        return False

if __name__ == "__main__":
    success = test_abbot_ware_outcome()

    if success:
        print("\n🎉 OUTCOME DETECTION FIXED!")
        print("✅ Ready to integrate into full BMAD agent")
    else:
        print("\n⚠️  OUTCOME DETECTION NEEDS MORE WORK")
        print("❌ Manual review of transcript endings required")