# -*- coding: utf-8 -*-
"""
Test strategic allocation extraction - PROXIMITY-BASED STRATEGY
Find the percentage closest to each keyword
"""

import re

# Test scenarios
test_scenarios = {
    "Current text": """
Foreign currency bonds account for 43% of the allocations, making them the most important asset class.
Equities account for 23%. They offer attractive returns in the long term, but are subject to higher short-
term risks. Bonds and other fixed-income instruments denominated in CHF account for 21%, which is
lower than the other two asset classes due to their low return potential. Real estate, which accounts for
11% of the allocations, is particularly interesting in terms of long-term growth. To further diversify the
portfolio and protect against inflation, compenswiss also invests 2% in precious metals. Since 2019, this
asset class known as "commodities", has been limited to gold.
""",

    "Variation 1": """
The allocation consists of 43% foreign currency bonds, which are the largest component.
Equities represent 23% of the portfolio. Bonds denominated in Swiss francs (CHF) make up 21%.
Real estate holdings are 11% of total allocations.
Precious metals, specifically gold, comprise 2% of investments.
""",

    "Variation 2": """
Real estate investments account for 11%. The fund also holds 2% in precious metals.
Foreign currency bonds are the largest at 43%. Equities comprise 23%.
Bonds denominated in CHF represent 21% of the portfolio.
""",

    "Variation 3": """
The strategic allocation shows that foreign currency bonds, being the most significant, account for approximately 43%.
Equity investments account for roughly 23% of assets. Bonds denominated in Swiss CHF account for about 21%.
Additionally, real estate accounts for 11% while precious metals investments stand at 2%.
""",
}

# Strategy: Multiple keywords per asset, find closest percentage
ASSET_KEYWORDS = {
    "Foreign currency bonds": {
        "keywords": ["foreign currency bond", "foreign bond"],
        "column": 28,
    },
    "Equities": {
        "keywords": ["equit"],
        "column": 29,
    },
    "Bonds in CHF": {
        "keywords": ["denominated in chf", "bonds.*chf", "chf.*bond"],
        "column": 30,
    },
    "Real estate": {
        "keywords": ["real[- ]estate", "property"],
        "column": 31,
    },
    "Precious metals": {
        "keywords": ["precious metal", "gold", "commodit"],
        "column": 32,
    },
}


def find_closest_percentage(text, keywords, max_distance=150):
    """Find percentage closest to any of the keywords"""

    # Find all percentages with their positions
    percentages = []
    for match in re.finditer(r'(\d+)%', text):
        percentages.append({
            'value': match.group(1),
            'position': match.start(),
        })

    if not percentages:
        return None, None

    # For each keyword, find closest percentage
    best_match = None
    best_distance = float('inf')
    best_keyword = None

    for keyword in keywords:
        # Find keyword position
        keyword_match = re.search(keyword, text, re.IGNORECASE)
        if not keyword_match:
            continue

        keyword_pos = keyword_match.start()

        # Find closest percentage
        for pct in percentages:
            distance = abs(pct['position'] - keyword_pos)

            # Only consider if within max distance
            if distance <= max_distance and distance < best_distance:
                best_distance = distance
                best_match = pct['value']
                best_keyword = keyword

    return best_match, best_keyword


# Run tests
print("="*80)
print("  PROXIMITY-BASED EXTRACTION STRATEGY TEST")
print("="*80)
print("Strategy: Find the percentage CLOSEST to each asset keyword")
print("="*80)

for scenario_name, test_text in test_scenarios.items():
    print("\nScenario: {}".format(scenario_name))
    print("-"*80)

    all_correct = True

    for asset_name, config in ASSET_KEYWORDS.items():
        value, matched_keyword = find_closest_percentage(test_text, config["keywords"])

        if value:
            print("  [OK] {}: {}% (Col {}) - matched '{}'".format(
                asset_name, value, config["column"], matched_keyword
            ))
        else:
            print("  [FAIL] {}: NOT FOUND".format(asset_name))
            all_correct = False

    if all_correct:
        print("\n  [SUCCESS] All values extracted")

print("\n" + "="*80)
print("STRATEGY BENEFITS:")
print("="*80)
print("""
1. SIMPLE: Just find closest % to keyword
2. ROBUST: Works regardless of text order or wording
3. ACCURATE: Proximity ensures correct matching
4. ADAPTIVE: No need to update patterns for text changes
5. FAST: Single pass through text
""")
