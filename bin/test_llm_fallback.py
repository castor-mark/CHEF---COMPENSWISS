# -*- coding: utf-8 -*-
"""
Test LLM Fallback Extraction
Tests GroqCloud, OpenRouter, and Gemini APIs
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_fallback import LLMFallbackExtractor

# Test data
TEST_STRATEGIC_TEXT = """
Foreign currency bonds account for 37% of the allocations, making them the most important asset class.
Equities account for 28%. They offer attractive returns in the long term, but are subject to higher short-
term risks. Bonds and other fixed-income instruments denominated in CHF account for 17%, which is
lower than the other two asset classes due to their low return potential. Real estate, which accounts for
15% of the allocations, is particularly interesting in terms of long-term growth. To further diversify the
portfolio and protect against inflation, compenswiss also invests 3% in precious metals. Since 2019, this
asset class known as "commodities", has been limited to gold.
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

EXPECTED_CATEGORIES = [
    "Money market investments",
    "Loans to public entities in Switzerland",
    "Swiss francs bonds",
    "Foreign currency bonds:",
    "Equities:",
    "Real estate:",
    "Gold"
]


def test_strategic_allocation():
    """Test strategic allocation extraction"""
    print("="*80)
    print("  TEST: Strategic Allocation Extraction with LLM Fallback")
    print("="*80)

    extractor = LLMFallbackExtractor()

    print("\nTest Text:")
    print("-"*80)
    print(TEST_STRATEGIC_TEXT[:200] + "...")

    print("\n" + "-"*80)
    result = extractor.extract_strategic_allocation(TEST_STRATEGIC_TEXT)

    print("\n" + "="*80)
    print("  RESULTS")
    print("="*80)

    expected = {
        "Foreign currency bonds": "37",
        "Equities": "28",
        "Bonds in CHF": "17",
        "Real estate": "15",
        "Precious metals": "3"
    }

    for asset, expected_value in expected.items():
        actual_value = result.get(asset, "NOT FOUND")
        status = "[OK]" if actual_value == expected_value else "[FAIL]"
        print(f"  {status} {asset}: {actual_value}% (expected {expected_value}%)")

    if result:
        print(f"\n[SUCCESS] Extracted {len(result)}/5 assets")
    else:
        print("\n[FAIL] No data extracted")

    return result


def test_performance_data():
    """Test performance data extraction"""
    print("\n\n" + "="*80)
    print("  TEST: Performance Data Extraction with LLM Fallback")
    print("="*80)

    extractor = LLMFallbackExtractor()

    print("\nTest HTML (sample):")
    print("-"*80)
    print(TEST_PERFORMANCE_HTML[:300] + "...")

    print("\n" + "-"*80)
    result = extractor.extract_performance_data(TEST_PERFORMANCE_HTML, EXPECTED_CATEGORIES)

    print("\n" + "="*80)
    print("  RESULTS")
    print("="*80)

    expected = {
        "Money market investments": "452",
        "Loans to public entities in Switzerland": "1295",
        "Swiss francs bonds": "5624",
        "Foreign currency bonds:": "15829",
        "Equities:": "12278",
        "Real estate:": "6049",
        "Gold": "1447"
    }

    for category, expected_value in expected.items():
        actual_value = result.get(category, "NOT FOUND")
        status = "[OK]" if actual_value == expected_value else "[FAIL]"
        print(f"  {status} {category}: {actual_value} (expected {expected_value})")

    if result:
        print(f"\n[SUCCESS] Extracted {len(result)}/7 categories")
    else:
        print("\n[FAIL] No data extracted")

    return result


if __name__ == "__main__":
    print("\n")
    print("*"*80)
    print("  LLM FALLBACK EXTRACTION TEST SUITE")
    print("  Testing: GroqCloud, OpenRouter, and Gemini APIs")
    print("*"*80)

    # Test strategic allocation
    strategic_result = test_strategic_allocation()

    # Test performance data
    performance_result = test_performance_data()

    # Summary
    print("\n\n" + "="*80)
    print("  TEST SUMMARY")
    print("="*80)

    if strategic_result:
        print(f"[OK] Strategic Allocation: {len(strategic_result)}/5 assets")
    else:
        print("[FAIL] Strategic Allocation: 0/5 assets")

    if performance_result:
        print(f"[OK] Performance Data: {len(performance_result)}/7 categories")
    else:
        print("[FAIL] Performance Data: 0/7 categories")

    if strategic_result and performance_result:
        print("\n[SUCCESS] LLM fallback is working correctly!")
    else:
        print("\n[WARNING] Some tests failed - check API keys in .env")

    print("="*80)
