#!/usr/bin/env python3
"""
HYBRID BMAD EXTRACTOR
Combines pattern matching with AI analysis for maximum accuracy
Designed to fix the catastrophic failures of pure AI extraction
"""

import json
import requests
import re
from datetime import datetime
from typing import Dict, Optional, List, Tuple

class HybridBMADExtractor:
    """Hybrid extractor using pattern matching + AI verification"""

    def __init__(self):
        self.model = "gpt-oss:20b"
        self.endpoint = "http://localhost:11434/api/generate"

        # US States for pattern matching
        self.us_states = [
            'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
            'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
            'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
            'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
            'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
            'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
            'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
            'Wisconsin', 'Wyoming'
        ]

        # State abbreviations
        self.state_abbrevs = {
            'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
            'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
            'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
            'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
            'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
            'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
            'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
            'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
            'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
            'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
        }

    def extract_state_pattern_matching(self, content: str) -> Optional[str]:
        """Use pattern matching to find state mentions based on meeting flow pattern"""

        print("🔍 Pattern matching for state...")

        # Focus on beginning of transcript (first 3000 characters) where location question is asked
        beginning_content = content[:3000]

        # Look for the location question and response pattern
        location_question_patterns = [
            r"where.*world.*joining.*from.*today",
            r"where.*are.*you.*joining.*from",
            r"where.*in.*the.*world.*are.*you",
            r"where.*are.*you.*calling.*from",
            r"where.*are.*you.*located",
        ]

        # Find where the location question appears
        question_position = None
        for pattern in location_question_patterns:
            match = re.search(pattern, beginning_content, re.IGNORECASE)
            if match:
                question_position = match.end()
                print(f"✅ Found location question at position {question_position}")
                break

        # If we found the question, look for state in the next 500 characters after it
        if question_position:
            response_section = beginning_content[question_position:question_position + 500]
            print(f"🔍 Searching response section: '{response_section[:100]}...'")

            # Search for states in the response section first (highest priority)
            for state in self.us_states:
                # Look for state name in response to location question
                patterns = [
                    rf'\b{re.escape(state)}\b',  # Exact state name
                    rf'from\s+.*{re.escape(state)}',  # "from ... Maryland"
                    rf'in\s+{re.escape(state)}',  # "in Maryland"
                    rf'{re.escape(state)}\s*,',  # "Maryland,"
                    rf'joining.*from.*{re.escape(state)}',  # "joining from ... Maryland"
                ]

                for pattern in patterns:
                    if re.search(pattern, response_section, re.IGNORECASE):
                        print(f"✅ Found state in response section: {state}")
                        return state

            # Check state abbreviations in response section (but be careful with common words)
            for abbrev, full_name in self.state_abbrevs.items():
                # Skip problematic abbreviations that are common words
                if abbrev in ['ID', 'IN', 'OR', 'HI']:  # These can be confused with common words
                    continue

                patterns = [
                    rf'\b{abbrev}\b',  # "MD", "GA", etc.
                    rf'{abbrev}\s*,',  # "MD,"
                ]

                for pattern in patterns:
                    if re.search(pattern, response_section, re.IGNORECASE):
                        print(f"✅ Found state via abbreviation in response: {full_name} ({abbrev})")
                        return full_name

        # Fallback: search entire beginning section if no question found
        print("🔍 Fallback: searching entire beginning section...")

        # Look for common response patterns in beginning (prioritize specific contexts)
        for state in self.us_states:
            # High priority patterns - direct location responses
            high_priority_patterns = [
                rf'i\s+live\s+in\s+{re.escape(state)}',  # "I live in South Carolina"
                rf'joining.*from.*{re.escape(state)}',  # "I'm joining from Maryland"
                rf'calling.*from.*{re.escape(state)}',  # "I'm calling from Maryland"
                rf'located\s+in\s+{re.escape(state)}',  # "located in South Carolina"
                rf'we\'re\s+in\s+{re.escape(state)}',  # "we're in South Carolina"
            ]

            for pattern in high_priority_patterns:
                if re.search(pattern, beginning_content, re.IGNORECASE):
                    print(f"✅ Found state via HIGH PRIORITY pattern: {state}")
                    return state

        # Medium priority patterns
        for state in self.us_states:
            medium_priority_patterns = [
                rf'from\s+.*{re.escape(state)}',  # "from ... Maryland"
                rf'in\s+{re.escape(state)}',  # "in Maryland"
                rf'{re.escape(state)}\s*,',  # "Maryland,"
            ]

            for pattern in medium_priority_patterns:
                if re.search(pattern, beginning_content, re.IGNORECASE):
                    print(f"✅ Found state via MEDIUM PRIORITY pattern: {state}")
                    return state

        # Low priority - just the state name (last resort)
        for state in self.us_states:
            if re.search(rf'\b{re.escape(state)}\b', beginning_content, re.IGNORECASE):
                print(f"✅ Found state via LOW PRIORITY pattern: {state}")
                return state

        # Check state abbreviations in entire beginning (be very careful with common words)
        for abbrev, full_name in self.state_abbrevs.items():
            # Skip very problematic abbreviations that are common words
            if abbrev in ['ID', 'IN', 'OR', 'HI', 'ME', 'IS', 'IT', 'OF', 'TO']:  # These can be confused with common words
                continue

            # Only look for abbreviations in very specific contexts
            abbrev_patterns = [
                rf'\b{abbrev}\b\s*,',  # "MD," - with comma
                rf'\b{abbrev}\b\s*\.',  # "MD." - with period
                rf'from\s+{abbrev}\b',  # "from MD"
                rf'in\s+{abbrev}\b',  # "in MD"
            ]

            for pattern in abbrev_patterns:
                if re.search(pattern, beginning_content, re.IGNORECASE):
                    print(f"✅ Found state via SAFE abbreviation: {full_name} ({abbrev})")
                    return full_name

        print("❌ No state found via pattern matching")
        return None

    def extract_age_pattern_matching(self, content: str) -> Optional[int]:
        """Use pattern matching to find age mentions"""

        print("🔍 Pattern matching for age...")

        # Age patterns
        age_patterns = [
            r"I'm\s+(\d{1,3})\s+years?\s+old",  # "I'm 65 years old"
            r"I\s+am\s+(\d{1,3})\s+years?\s+old",  # "I am 65 years old"
            r"I'm\s+(\d{1,3})",  # "I'm 65"
            r"I\s+am\s+(\d{1,3})",  # "I am 65"
            r"(\d{1,3})\s+years?\s+old",  # "65 years old"
            r"age\s+(\d{1,3})",  # "age 65"
            r"turned\s+(\d{1,3})",  # "turned 65"
            r"(\d{1,3})-year-old",  # "65-year-old"
        ]

        for pattern in age_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                age = int(match)
                if 18 <= age <= 120:  # Reasonable age range
                    print(f"✅ Found age via pattern: {age}")
                    return age

        print("❌ No age found via pattern matching")
        return None

    def extract_marital_status_pattern_matching(self, content: str) -> Optional[str]:
        """Use pattern matching to find marital status"""

        print("🔍 Pattern matching for marital status...")

        # Marital status patterns (ordered by specificity)
        marital_patterns = [
            (r"my\s+wife\b", "Married"),
            (r"my\s+husband\b", "Married"),
            (r"my\s+spouse\b", "Married"),
            (r"I'm\s+married", "Married"),
            (r"I\s+am\s+married", "Married"),
            (r"we're\s+married", "Married"),
            (r"we\s+are\s+married", "Married"),
            (r"I'm\s+single", "Single"),
            (r"I\s+am\s+single", "Single"),
            (r"I'm\s+divorced", "Divorced"),
            (r"I\s+am\s+divorced", "Divorced"),
            (r"my\s+ex-wife", "Divorced"),
            (r"my\s+ex-husband", "Divorced"),
            (r"I'm\s+widowed", "Widowed"),
            (r"I\s+am\s+widowed", "Widowed"),
            (r"my\s+late\s+wife", "Widowed"),
            (r"my\s+late\s+husband", "Widowed"),
        ]

        for pattern, status in marital_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                print(f"✅ Found marital status via pattern: {status}")
                return status

        print("❌ No marital status found via pattern matching")
        return None

    def extract_children_count_pattern_matching(self, content: str) -> Optional[int]:
        """Use pattern matching to count children"""

        print("🔍 Pattern matching for children count...")

        # Direct number patterns
        children_patterns = [
            r"(\d+)\s+children",
            r"(\d+)\s+kids",
            r"have\s+(\d+)\s+children",
            r"have\s+(\d+)\s+kids",
            r"(\d+)\s+sons?\s+and\s+(\d+)\s+daughters?",
            r"(\d+)\s+daughters?\s+and\s+(\d+)\s+sons?",
        ]

        for pattern in children_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    count = sum(int(x) for x in match)
                else:
                    count = int(match)
                if 0 <= count <= 20:  # Reasonable range
                    print(f"✅ Found children count via pattern: {count}")
                    return count

        # Count individual mentions
        son_mentions = len(re.findall(r"\bmy\s+son\b", content, re.IGNORECASE))
        daughter_mentions = len(re.findall(r"\bmy\s+daughter\b", content, re.IGNORECASE))

        if son_mentions > 0 or daughter_mentions > 0:
            total = son_mentions + daughter_mentions
            print(f"✅ Found children count via mentions: {total} (sons: {son_mentions}, daughters: {daughter_mentions})")
            return total

        print("❌ No children count found via pattern matching")
        return None

    def extract_estate_value_pattern_matching(self, content: str) -> Optional[int]:
        """Use pattern matching to find estate values"""

        print("🔍 Pattern matching for estate value...")

        # Estate value patterns
        value_patterns = [
            r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*million",  # "$1.3 million"
            r"(\d{1,3}(?:\.\d+)?)\s*million\s*dollars?",  # "1.3 million dollars"
            r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*k",  # "$600k"
            r"(\d{1,3}(?:,\d{3})*)\s*k\s*dollars?",  # "600k dollars"
            r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",  # "$600,000"
            r"worth\s+about\s+\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",  # "worth about $600,000"
            r"estate\s+of\s+\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",  # "estate of $600,000"
            r"assets?\s+worth\s+\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",  # "assets worth $600,000"
        ]

        for pattern in value_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                try:
                    value_str = match.replace(',', '')
                    if 'million' in pattern:
                        value = int(float(value_str) * 1000000)
                    elif 'k' in pattern:
                        value = int(float(value_str) * 1000)
                    else:
                        value = int(float(value_str))

                    if 10000 <= value <= 100000000:  # Reasonable range
                        print(f"✅ Found estate value via pattern: ${value:,}")
                        return value
                except:
                    continue

        print("❌ No estate value found via pattern matching")
        return None

    def extract_meeting_outcome_pattern_matching(self, content: str) -> Optional[str]:
        """Use pattern matching to determine meeting outcome based on end-of-meeting flow"""

        print("🔍 Pattern matching for meeting outcome...")

        # Check the last 4000 characters where decisions are typically made
        ending_content = content[-4000:].lower()

        # Look for package/service offering and response patterns
        print("🔍 Analyzing end-of-meeting decision patterns...")

        # DEFERRAL/FOLLOW-UP INDICATORS (check these FIRST - they override positive signals)
        deferral_indicators = [
            r"won't\s+be\s+able\s+to\s+do.*today",
            r"can't\s+do.*today",
            r"don't\s+have\s+the\s+funds",
            r"i'll\s+reach\s+out\s+to\s+you",
            r"second\s+week\s+of.*month",
            r"follow\s+up\s+with\s+you",
            r"reach\s+out.*next\s+week",
            r"reach\s+out.*next\s+month",
            r"not\s+able\s+to\s+do\s+anything\s+today",
            r"didn't\s+know.*doing.*financing\s+today",
            r"won't\s+be\s+able\s+to\s+do\s+it\s+today",
            r"we'll\s+get\s+you\s+set\s+up\s+then",
        ]

        # Check for deferrals/follow-ups FIRST
        for pattern in deferral_indicators:
            if re.search(pattern, ending_content):
                print(f"✅ Found 'Follow Up' via DEFERRAL: {pattern}")
                return "Follow Up"

        # ACTUAL TRANSACTION INDICATORS (only if no deferral found)
        transaction_indicators = [
            r"processed\s+the\s+payment",
            r"already\s+processed\s+the\s+payment",
            r"building\s+out\s+your\s+documents",
            r"work\s+for\s+you\s+right\s+now.*building.*documents",
            r"finish\s+building\s+out\s+your\s+account",
            r"pull\s+the\s+trigger",
            r"decided\s+to.*pull\s+the\s+trigger",
            r"already\s+charged",
            r"payment\s+went\s+through",
            r"card\s+was\s+charged",
            r"transaction.*complete",
            r"mastercard",
            r"visa",
            r"american\s+express",
            r"discover\s+card",
        ]

        # Check for actual transaction completion (but not if it's just asking about card type)
        for pattern in transaction_indicators:
            match = re.search(pattern, ending_content)
            if match:
                # Verify it's not just asking about payment method without completion
                context_start = max(0, match.start() - 200)
                context_end = min(len(ending_content), match.end() + 200)
                context = ending_content[context_start:context_end]

                # If there are deferral phrases near the transaction indicator, it's still a follow-up
                if not any(re.search(defer, context) for defer in ["won't be able", "can't do", "don't have the funds"]):
                    print(f"✅ Found 'Closed Won' via TRANSACTION: {pattern}")
                    return "Closed Won"

        # COMMITMENT AND SCHEDULING INDICATORS (second priority)
        commitment_indicators = [
            r"schedule.*next\s+meeting",
            r"schedule.*client\s+meeting",
            r"next\s+meeting.*scheduled",
            r"we\s+just\s+schedule\s+the\s+next\s+meeting",
            r"building.*documents",
            r"get\s+you\s+taken\s+care\s+of",
            r"move\s+forward\s+in\s+the\s+process",
            r"let's\s+do\s+it",
            r"i'm\s+ready\s+to\s+move\s+forward",
            r"sign\s+me\s+up",
            r"sounds\s+good.*proceed",
            r"i\s+want\s+to\s+go\s+ahead",
            r"let's\s+move\s+forward",
            r"i'm\s+ready\s+to\s+proceed",
            r"yes.*let's\s+do\s+this",
            r"that\s+sounds\s+perfect",
            r"perfect.*let's\s+do\s+that",
            r"absolutely.*let's\s+proceed",
            r"yes.*that\s+works\s+for\s+me",
            r"i\s+think\s+that's\s+exactly\s+what\s+i\s+need",
            r"that\s+sounds\s+like\s+a\s+great\s+fit",
            r"i'm\s+ready\s+to\s+get\s+started",
            r"let's\s+get\s+this\s+going",
            r"i\s+want\s+to\s+move\s+ahead",
            r"sounds\s+like\s+a\s+plan",
            r"perfect.*i'm\s+in",
            r"absolutely.*i'm\s+ready",
        ]

        # Check for strong commitment patterns
        for pattern in commitment_indicators:
            if re.search(pattern, ending_content):
                print(f"✅ Found 'Closed Won' via COMMITMENT: {pattern}")
                return "Closed Won"

        # Closed Lost indicators (clear rejection)
        lost_patterns = [
            r"not\s+interested",
            r"too\s+expensive",
            r"can't\s+afford",
            r"maybe\s+later",
            r"not\s+ready",
            r"not\s+for\s+me",
            r"i'll\s+pass",
            r"no\s+thank\s+you",
            r"this\s+isn't\s+for\s+me",
            r"i\s+don't\s+think\s+so",
            r"not\s+at\s+this\s+time",
        ]

        for pattern in lost_patterns:
            if re.search(pattern, ending_content):
                print(f"✅ Found 'Closed Lost' via pattern: {pattern}")
                return "Closed Lost"

        # Follow Up indicators (need more time/discussion)
        followup_patterns = [
            r"need\s+to\s+think\s+about\s+it",
            r"let\s+me\s+discuss\s+with",
            r"call\s+me\s+back",
            r"i'll\s+get\s+back\s+to\s+you",
            r"need\s+to\s+talk\s+to\s+my",
            r"let\s+me\s+think\s+it\s+over",
            r"i\s+need\s+some\s+time",
            r"can\s+you\s+follow\s+up",
            r"let\s+me\s+consider",
            r"i'll\s+think\s+about\s+it",
            r"give\s+me\s+a\s+few\s+days",
            r"let\s+me\s+talk\s+to",
        ]

        for pattern in followup_patterns:
            if re.search(pattern, ending_content):
                print(f"✅ Found 'Follow Up' via pattern: {pattern}")
                return "Follow Up"

        # If no clear indicators, look for scheduling or positive engagement
        positive_engagement = [
            r"thank\s+you.*this\s+was\s+helpful",
            r"this\s+has\s+been\s+informative",
            r"i\s+appreciate.*information",
            r"very\s+helpful",
            r"good\s+information",
        ]

        for pattern in positive_engagement:
            if re.search(pattern, ending_content):
                print(f"✅ Found positive engagement (Follow Up): {pattern}")
                return "Follow Up"

        print("❌ No clear meeting outcome found via pattern matching")
        return None

    def ai_verification_pass(self, content: str, pattern_results: Dict) -> Dict:
        """Use AI to verify and fill gaps in pattern matching results"""

        print("\n🤖 AI verification pass...")

        # Create focused prompt based on what we found/missed
        missing_fields = [k for k, v in pattern_results.items() if v is None]

        if not missing_fields:
            print("✅ All fields found via pattern matching, skipping AI verification")
            return pattern_results

        verification_prompt = f"""You are a data verification specialist. Review this transcript excerpt and help fill missing information.

PATTERN MATCHING FOUND:
{json.dumps(pattern_results, indent=2)}

MISSING FIELDS: {', '.join(missing_fields)}

TRANSCRIPT EXCERPT:
{content[:4000]}

For MISSING fields only, search carefully and return JSON:
{{
  "verified_data": {{
    // Only include fields that were None in pattern_results
  }},
  "confidence": {{
    // Rate confidence 1-10 for each field you found
  }}
}}

Return ONLY valid JSON. Be conservative - only include data you're very confident about."""

        try:
            response = requests.post(
                self.endpoint,
                json={
                    "model": self.model,
                    "prompt": verification_prompt,
                    "temperature": 0.05,
                    "stream": False
                },
                timeout=60
            )

            if response.status_code == 200:
                gpt_response = response.json()['response']

                # Extract JSON
                json_match = re.search(r'\{.*\}', gpt_response, re.DOTALL)
                if json_match:
                    ai_results = json.loads(json_match.group())
                    verified_data = ai_results.get('verified_data', {})
                    confidence = ai_results.get('confidence', {})

                    # Merge high-confidence AI results with pattern results
                    for field, value in verified_data.items():
                        if field in pattern_results and pattern_results[field] is None:
                            field_confidence = confidence.get(field, 0)
                            if field_confidence >= 7:  # High confidence threshold
                                pattern_results[field] = value
                                print(f"✅ AI verified {field}: {value} (confidence: {field_confidence}/10)")
                            else:
                                print(f"⚠️  AI found {field}: {value} but low confidence ({field_confidence}/10)")

        except Exception as e:
            print(f"⚠️  AI verification failed: {e}")

        return pattern_results

    def extract_comprehensive(self, content: str, client_name: str) -> Dict:
        """Comprehensive extraction using hybrid approach"""

        print(f"🎯 HYBRID EXTRACTION: {client_name}")
        print("=" * 70)

        # Phase 1: Pattern Matching (high accuracy, limited coverage)
        print("\n📋 Phase 1: Pattern Matching...")

        pattern_results = {
            'state': self.extract_state_pattern_matching(content),
            'age': self.extract_age_pattern_matching(content),
            'marital_status': self.extract_marital_status_pattern_matching(content),
            'children_count': self.extract_children_count_pattern_matching(content),
            'estate_value': self.extract_estate_value_pattern_matching(content),
            'meeting_stage': self.extract_meeting_outcome_pattern_matching(content),
        }

        print(f"\n📊 Pattern Matching Results:")
        for field, value in pattern_results.items():
            if value is not None:
                print(f"   ✅ {field}: {value}")
            else:
                print(f"   ❌ {field}: None")

        # Phase 2: AI Verification for missing fields
        print("\n🔍 Phase 2: AI Verification...")
        final_results = self.ai_verification_pass(content, pattern_results)

        # Phase 3: Add defaults and structure
        comprehensive_data = {
            'client_name': client_name,
            'age': final_results.get('age'),
            'state': final_results.get('state'),
            'marital_status': final_results.get('marital_status', 'Unknown'),
            'children_count': final_results.get('children_count', 0),
            'estate_value': final_results.get('estate_value', 0),
            'real_estate_count': 1,  # Default assumption
            'llc_interest': 0,  # Default
            'meeting_stage': final_results.get('meeting_stage', 'Follow Up'),
            'pain_points': 'Estate planning consultation',
            'objections': '',
            'urgency_score': 5,  # Default medium urgency
            'follow_up_required': True,
        }

        print(f"\n📈 FINAL EXTRACTION RESULTS:")
        for field, value in comprehensive_data.items():
            if value and value not in ['Unknown', '', 0, None]:
                print(f"   ✅ {field}: {value}")
            else:
                print(f"   ⚠️  {field}: {value} (default/missing)")

        return comprehensive_data

def test_hybrid_extraction():
    """Test hybrid extraction on known problematic cases"""

    print("🧪 TESTING HYBRID EXTRACTION")
    print("=" * 70)

    extractor = HybridBMADExtractor()

    # Test cases with known expected results
    test_cases = [
        {
            'name': 'Alan Reinhard',
            'file': '/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts/Alan Reinhard: Estate Planning Advisor Meeting.txt',
            'expected': {'state': 'Maryland'}
        },
        {
            'name': 'Abbot Ware',
            'file': '/Users/joshuavaughan/Library/CloudStorage/GoogleDrive-jvaughan27@gmail.com/.shortcut-targets-by-id/1oyouGXIJLyId2y2H-JJVYay9GFpnLTDK/McAdams Transcripts/Abbot Ware: Estate Planning Advisor Meeting.txt',
            'expected': {'state': 'South Carolina', 'meeting_stage': 'Closed Won'}
        }
    ]

    accuracy_results = {}

    for test_case in test_cases:
        print(f"\n🔍 Testing: {test_case['name']}")
        print("-" * 50)

        try:
            with open(test_case['file'], 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract using hybrid approach
            results = extractor.extract_comprehensive(content, test_case['name'])

            # Check accuracy
            correct = 0
            total = len(test_case['expected'])

            for field, expected_value in test_case['expected'].items():
                actual_value = results.get(field)
                if actual_value == expected_value:
                    print(f"   ✅ {field}: {actual_value} (CORRECT)")
                    correct += 1
                else:
                    print(f"   ❌ {field}: {actual_value} (EXPECTED: {expected_value})")

            accuracy = (correct / total) * 100
            accuracy_results[test_case['name']] = accuracy
            print(f"   📊 Accuracy: {accuracy:.1f}% ({correct}/{total})")

        except Exception as e:
            print(f"   ❌ Test failed: {e}")
            accuracy_results[test_case['name']] = 0

    # Overall results
    print(f"\n📈 OVERALL HYBRID EXTRACTION RESULTS:")
    print("=" * 50)

    total_accuracy = sum(accuracy_results.values()) / len(accuracy_results)
    for name, accuracy in accuracy_results.items():
        print(f"   • {name}: {accuracy:.1f}%")

    print(f"\n🎯 AVERAGE ACCURACY: {total_accuracy:.1f}%")

    if total_accuracy >= 80:
        print("🎉 HYBRID EXTRACTION READY FOR PRODUCTION!")
        return True
    else:
        print("⚠️  HYBRID EXTRACTION NEEDS MORE IMPROVEMENT")
        return False

if __name__ == "__main__":
    success = test_hybrid_extraction()

    if success:
        print("\n✅ READY TO PROCESS ALL 352 TRANSCRIPTS WITH HYBRID EXTRACTION")
    else:
        print("\n❌ CONTINUE IMPROVING HYBRID EXTRACTION ACCURACY")