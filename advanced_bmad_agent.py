#!/usr/bin/env python3
"""
ADVANCED BMAD EXTRACTION AGENT
Completely redesigned for maximum accuracy and reliability
"""

import json
import requests
import re
from datetime import datetime

class AdvancedBMADAgent:
    """Advanced BMAD agent with multiple extraction strategies"""

    def __init__(self):
        self.model = "gpt-oss:20b"
        self.endpoint = "http://localhost:11434/api/generate"

    def extract_with_targeted_prompts(self, transcript_content, client_name):
        """Use multiple targeted prompts for maximum accuracy"""

        print(f"🎯 ADVANCED BMAD ANALYSIS: {client_name}")
        print("=" * 70)

        results = {}

        # Strategy 1: Location and Demographics Specialist
        location_prompt = f"""You are a location and demographics specialist. Your ONLY job is to find location and age information.

TRANSCRIPT EXCERPT:
{transcript_content[:4000]}

Search for:
- State names (Georgia, Florida, Texas, California, South Carolina, etc.)
- Age mentions ("I'm 65", "65 years old", "I turned 70")
- Cities that indicate states
- Phone area codes that indicate states

Return ONLY JSON:
{{
  "state": "State name if found",
  "age": number_if_found_else_null,
  "city": "City if mentioned"
}}"""

        # Strategy 2: Family Structure Specialist
        family_prompt = f"""You are a family structure specialist. Find family information.

TRANSCRIPT EXCERPT:
{transcript_content[:4000]}

Look for:
- Marital status ("my wife", "my husband", "I'm married", "I'm single", "I'm divorced", "I'm widowed")
- Children ("my son", "my daughter", "3 kids", "children", "grandchildren")
- Family relationships

Return ONLY JSON:
{{
  "marital_status": "Married/Single/Divorced/Widowed",
  "children_count": number,
  "spouse_mentioned": true_or_false
}}"""

        # Strategy 3: Financial Assets Specialist
        financial_prompt = f"""You are a financial assets specialist. Find money and property information.

TRANSCRIPT EXCERPT:
{transcript_content[:5000]}

Look for:
- Dollar amounts ("$500,000", "half a million", "240k", "1.3 million")
- Property mentions ("my house", "rental property", "properties", "real estate")
- Business ownership ("my business", "LLC", "corporation", "I own")

Return ONLY JSON:
{{
  "estate_value": number_without_symbols,
  "real_estate_count": number,
  "business_interests": true_or_false
}}"""

        # Strategy 4: Meeting Outcome Specialist
        outcome_prompt = f"""You are a meeting outcome specialist. Determine if this was successful.

TRANSCRIPT EXCERPT:
{transcript_content[:3000]}

Look for indicators of:
- SUCCESS: "let's move forward", "I want to proceed", "sign me up", "sounds good", "I'm ready"
- FOLLOW UP: "need to think about it", "call me back", "let me discuss with family"
- REJECTION: "not interested", "too expensive", "maybe later", "not ready"

Meeting outcome clues:
- Enthusiastic responses = Closed Won
- Hesitation but interest = Follow Up
- Clear rejection = Closed Lost
- Did not attend = No Show

Return ONLY JSON:
{{
  "meeting_stage": "Closed Won/Follow Up/Closed Lost/No Show",
  "urgency_score": 1_to_10,
  "pain_points": "main concerns"
}}"""

        # Execute all specialist extractions
        specialists = [
            ("Location/Demographics", location_prompt),
            ("Family Structure", family_prompt),
            ("Financial Assets", financial_prompt),
            ("Meeting Outcome", outcome_prompt)
        ]

        for specialist_name, prompt in specialists:
            print(f"\n🔍 {specialist_name} Specialist...")

            try:
                response = requests.post(
                    self.endpoint,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "temperature": 0.05,
                        "stream": False
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    gpt_response = response.json()['response']

                    # Extract JSON with multiple strategies
                    extracted = self._extract_json_robust(gpt_response)

                    if extracted:
                        results.update(extracted)
                        print(f"✅ {specialist_name} found:")
                        for key, value in extracted.items():
                            if value and value not in ["Unknown", "", 0, None]:
                                print(f"   • {key}: {value}")
                    else:
                        print(f"⚠️  {specialist_name} - no data extracted")
                else:
                    print(f"❌ {specialist_name} failed: {response.status_code}")

            except Exception as e:
                print(f"❌ {specialist_name} error: {e}")

        return results

    def _extract_json_robust(self, text):
        """Multiple strategies to extract JSON from text"""

        # Strategy 1: Direct JSON parsing
        try:
            # Look for JSON-like structures
            json_patterns = [
                r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Nested JSON
                r'\{.*?\}',  # Simple JSON
            ]

            for pattern in json_patterns:
                matches = re.findall(pattern, text, re.DOTALL)
                for match in matches:
                    try:
                        return json.loads(match)
                    except:
                        continue
        except:
            pass

        # Strategy 2: Manual extraction of key-value pairs
        try:
            result = {}

            # Extract common patterns
            patterns = {
                'state': r'"state":\s*"([^"]+)"',
                'age': r'"age":\s*(\d+)',
                'marital_status': r'"marital_status":\s*"([^"]+)"',
                'children_count': r'"children_count":\s*(\d+)',
                'estate_value': r'"estate_value":\s*(\d+)',
                'real_estate_count': r'"real_estate_count":\s*(\d+)',
                'meeting_stage': r'"meeting_stage":\s*"([^"]+)"',
                'urgency_score': r'"urgency_score":\s*(\d+)',
            }

            for key, pattern in patterns.items():
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    value = match.group(1)
                    if key in ['age', 'children_count', 'estate_value', 'real_estate_count', 'urgency_score']:
                        result[key] = int(value)
                    else:
                        result[key] = value

            return result if result else None

        except:
            return None

    def verify_and_enhance_data(self, extracted_data, transcript_content):
        """Final verification and enhancement pass"""

        print(f"\n🔍 VERIFICATION & ENHANCEMENT PASS...")

        # Verify state extraction with comprehensive search
        if not extracted_data.get('state'):
            state_verification_prompt = f"""Find the US STATE mentioned in this text. Look carefully for:

- Direct state names: Georgia, Florida, Texas, California, South Carolina, Vermont, etc.
- Cities that indicate states
- Area codes (404=Georgia, 843=South Carolina, etc.)
- Regional references

TEXT: {transcript_content[:2000]}

State found: """

            try:
                response = requests.post(
                    self.endpoint,
                    json={
                        "model": self.model,
                        "prompt": state_verification_prompt,
                        "temperature": 0.01,
                        "stream": False
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    state_response = response.json()['response'].strip()

                    # List of US states to match against
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
                        if state.lower() in state_response.lower():
                            extracted_data['state'] = state
                            print(f"✅ State verification found: {state}")
                            break

            except Exception as e:
                print(f"⚠️  State verification failed: {e}")

        return extracted_data

def test_advanced_agent():
    """Test the advanced agent on Abbot Ware to verify improvements"""

    print("🧪 TESTING ADVANCED BMAD AGENT")
    print("=" * 70)

    # Read Abbot Ware transcript
    transcript_file = "/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts/Abbot Ware: Estate Planning Advisor Meeting.txt"

    with open(transcript_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Initialize advanced agent
    agent = AdvancedBMADAgent()

    # Extract with multiple strategies
    extracted_data = agent.extract_with_targeted_prompts(content, "Abbot Ware")

    # Verification pass
    final_data = agent.verify_and_enhance_data(extracted_data, content)

    print(f"\n📊 FINAL EXTRACTION RESULTS:")
    print(f"   • Client: Abbot Ware")

    expected_results = {
        'state': 'South Carolina',
        'meeting_stage': 'Closed Won'
    }

    accuracy_score = 0
    total_checks = len(expected_results)

    for key, expected in expected_results.items():
        actual = final_data.get(key)
        if actual == expected:
            print(f"   ✅ {key}: {actual} (CORRECT)")
            accuracy_score += 1
        else:
            print(f"   ❌ {key}: {actual} (EXPECTED: {expected})")

    print(f"\n📈 ACCURACY: {accuracy_score}/{total_checks} ({accuracy_score/total_checks*100:.1f}%)")

    if accuracy_score == total_checks:
        print("🎉 ADVANCED AGENT READY FOR PRODUCTION!")
        return True
    else:
        print("⚠️  AGENT NEEDS FURTHER IMPROVEMENT")
        return False

if __name__ == "__main__":
    success = test_advanced_agent()

    if success:
        print("\n✅ READY TO PROCESS ALL 352 TRANSCRIPTS")
    else:
        print("\n❌ CONTINUE IMPROVING EXTRACTION ACCURACY")