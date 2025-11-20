# -*- coding: utf-8 -*-
"""
Gemini-only Test
Direct test of Gemini models with hardcoded API key
"""

import os
import time
import requests
import json
import re

# Hardcode API key for testing
GEMINI_API_KEY = "AIzaSyC2IFc-4yh-TJoymob2xr7X4HDIXkEI7T8"

# Test data
TEST_STRATEGIC_TEXT = """
Foreign currency bonds account for 37% of the allocations, making them the most important asset class.
Equities account for 28%. They offer attractive returns in the long term, but are subject to higher short-
term risks. Bonds and other fixed-income instruments denominated in CHF account for 17%, which is
lower than the other two asset classes due to their low return potential. Real estate, which accounts for
15% of the allocations, is particularly interesting in terms of long-term growth. To further diversify the
portfolio and protect against inflation, compenswiss also invests 3% in precious metals.
"""

TEST_PERFORMANCE_HTML = """
<table class="table--chart">
<tbody>
<tr><td>Money market investments</td><td>452</td></tr>
<tr><td>Loans to public entities in Switzerland</td><td>1,295</td></tr>
<tr><td>Swiss francs bonds</td><td>5,624</td></tr>
<tr><td>Foreign currency bonds:</td><td>15,829</td></tr>
<tr><td>Equities:</td><td>12,278</td></tr>
<tr><td>Real estate:</td><td>6,049</td></tr>
<tr><td>Gold</td><td>1,447</td></tr>
</tbody>
</table>
"""

EXPECTED_STRATEGIC = {
    "Foreign currency bonds": "37",
    "Equities": "28",
    "Bonds in CHF": "17",
    "Real estate": "15",
    "Precious metals": "3"
}

EXPECTED_PERFORMANCE = {
    "Money market investments": "452",
    "Loans to public entities in Switzerland": "1295",
    "Swiss francs bonds": "5624",
    "Foreign currency bonds:": "15829",
    "Equities:": "12278",
    "Real estate:": "6049",
    "Gold": "1447"
}


def call_gemini(prompt, model_name):
    """Call Gemini API"""
    try:
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}',
            headers={'Content-Type': 'application/json'},
            json={
                'contents': [{
                    'parts': [{'text': prompt}]
                }],
                'generationConfig': {
                    'temperature': 0.1,
                    'maxOutputTokens': 2000
                }
            },
            timeout=60
        )

        if response.status_code == 200:
            content = response.json()['candidates'][0]['content']['parts'][0]['text']
            return content
        else:
            print(f"  [ERROR] {response.status_code}: {response.text[:200]}")
            return None

    except Exception as e:
        print(f"  [EXCEPTION] {str(e)}")
        return None


def create_strategic_prompt(text):
    """Create prompt for strategic allocation extraction"""
    return f"""You are a data extraction expert. Extract strategic allocation percentages from the text below.

EXPECTED ASSETS:
- Foreign currency bonds
- Equities
- Bonds in CHF
- Real estate
- Precious metals

INSTRUCTIONS:
1. Find percentage allocations for each asset class
2. Return ONLY a JSON object with asset names as keys and percentages as values
3. Include ONLY the numeric value (e.g., "43" not "43%")
4. Support decimal percentages (e.g., "23.5")
5. If an asset is not mentioned, omit it from the JSON

TEXT CONTENT:
{text}

Return format:
{{
  "Foreign currency bonds": "37",
  "Equities": "28",
  "Bonds in CHF": "17",
  "Real estate": "15",
  "Precious metals": "3"
}}

JSON OUTPUT:"""


def create_performance_prompt(html_text, expected_categories):
    """Create prompt for performance data extraction"""
    categories_list = "\n".join([f"- {cat}" for cat in expected_categories])

    return f"""You are a data extraction expert. Extract investment performance data from the HTML table below.

EXPECTED CATEGORIES:
{categories_list}

INSTRUCTIONS:
1. Find each category in the table
2. Extract the corresponding amount (in CHF millions)
3. Return ONLY a JSON object with category names as keys and amounts as values
4. If a category is not found, omit it from the JSON
5. Remove all formatting (commas, spaces) from numbers
6. Handle negative numbers correctly (e.g., -582)

HTML CONTENT:
{html_text}

Return format:
{{
  "Money market investments": "452",
  "Foreign currency bonds:": "15829",
  ...
}}

JSON OUTPUT:"""


def parse_response(response):
    """Parse JSON from LLM response"""
    try:
        # Extract JSON from response (handle markdown code blocks)
        json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
        if not json_match:
            print(f"  [WARNING] No JSON found in response")
            return {}

        data = json.loads(json_match.group())
        return data

    except Exception as e:
        print(f"  [ERROR] Parse error: {str(e)}")
        return {}


def test_model(model_name):
    """Test a specific Gemini model"""
    print(f"\n{'='*80}")
    print(f"  TESTING: {model_name}")
    print(f"{'='*80}")

    # Test 1: Strategic Allocation
    print(f"\n[TEST 1] Strategic Allocation Extraction")
    print("-"*80)

    start_time = time.time()
    prompt = create_strategic_prompt(TEST_STRATEGIC_TEXT)
    response = call_gemini(prompt, model_name)
    strategic_time = time.time() - start_time

    if response:
        result = parse_response(response)
        correct = 0
        for asset, expected_value in EXPECTED_STRATEGIC.items():
            actual_value = result.get(asset, "NOT FOUND")
            if actual_value == expected_value:
                correct += 1
                print(f"  [OK] {asset}: {actual_value}%")
            else:
                print(f"  [FAIL] {asset}: {actual_value}% (expected {expected_value}%)")

        print(f"\n  Result: {correct}/5 correct ({strategic_time:.2f}s)")
    else:
        print("  [FAIL] No response from model")
        correct = 0

    strategic_score = correct

    # Test 2: Performance Data
    print(f"\n[TEST 2] Performance Data Extraction")
    print("-"*80)

    start_time = time.time()
    expected_categories = list(EXPECTED_PERFORMANCE.keys())
    prompt = create_performance_prompt(TEST_PERFORMANCE_HTML, expected_categories)
    response = call_gemini(prompt, model_name)
    performance_time = time.time() - start_time

    if response:
        result = parse_response(response)
        correct = 0
        for category, expected_value in EXPECTED_PERFORMANCE.items():
            actual_value = result.get(category, "NOT FOUND")
            if actual_value == expected_value:
                correct += 1
                print(f"  [OK] {category}: {actual_value}")
            else:
                print(f"  [FAIL] {category}: {actual_value} (expected {expected_value})")

        print(f"\n  Result: {correct}/7 correct ({performance_time:.2f}s)")
    else:
        print("  [FAIL] No response from model")
        correct = 0

    performance_score = correct

    # Summary
    print(f"\n{'='*80}")
    print(f"  SUMMARY: {model_name}")
    print(f"{'='*80}")
    print(f"  Strategic: {strategic_score}/5 ({strategic_time:.2f}s)")
    print(f"  Performance: {performance_score}/7 ({performance_time:.2f}s)")

    total_accuracy = ((strategic_score + performance_score) / 12) * 100
    total_time = strategic_time + performance_time

    print(f"  Overall: {total_accuracy:.1f}% accuracy in {total_time:.2f}s")

    if strategic_score == 5 and performance_score == 7:
        print(f"  [SUCCESS] 100% accurate!")
    else:
        print(f"  [WARNING] Incomplete extraction")

    return {
        'strategic': strategic_score,
        'performance': performance_score,
        'accuracy': total_accuracy,
        'time': total_time
    }


if __name__ == "__main__":
    print("\n" + "*"*80)
    print("  GEMINI API TEST SUITE")
    print("*"*80)

    # Test multiple Gemini models
    models_to_test = [
        'gemini-2.0-flash-exp',           # Current default in llm_fallback.py
        'gemini-exp-1206',                # Latest experimental
        'gemini-2.0-flash-thinking-exp',  # With thinking
        'gemini-1.5-pro',                 # Stable pro model
        'gemini-1.5-flash',               # Stable flash model
    ]

    results = {}
    for model in models_to_test:
        results[model] = test_model(model)

    # Final ranking
    print("\n\n" + "="*80)
    print("  FINAL RANKING")
    print("="*80)

    sorted_results = sorted(results.items(), key=lambda x: (x[1]['accuracy'], -x[1]['time']), reverse=True)

    for i, (model, result) in enumerate(sorted_results, 1):
        print(f"{i}. {model}")
        print(f"   Accuracy: {result['accuracy']:.1f}% | Time: {result['time']:.2f}s")

    print("\n" + "="*80)
