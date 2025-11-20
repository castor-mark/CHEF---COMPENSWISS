# -*- coding: utf-8 -*-
"""
Compare scraper results with sample data
Validates accuracy of extracted data
"""

import pandas as pd
import os


def compare_results():
    """Compare latest scraper output with sample data"""

    print("\n" + "="*70)
    print("  COMPARING SCRAPER RESULTS WITH SAMPLE DATA")
    print("="*70)

    # Paths
    sample_file = r"C:\Users\Mark Castro\Documents\CHEF – COMPENSWISS\Project-information\CHEF_COMPENSWISS_DATA_20240617.xlsx - DATA.csv"
    latest_file = r"C:\Users\Mark Castro\Documents\CHEF – COMPENSWISS\reports\latest\COMPENSWISS_DATA_2024.xlsx"

    # Check if files exist
    if not os.path.exists(sample_file):
        print("\n[ERROR] Sample file not found: {}".format(sample_file))
        return

    if not os.path.exists(latest_file):
        print("\n[ERROR] Latest scraper output not found: {}".format(latest_file))
        print("        Run the scraper first: python scraper.py 2024")
        return

    print("\n[1] Loading files...")

    # Load sample data (CSV)
    sample_df = pd.read_csv(sample_file)
    print("[OK] Sample data loaded: {} rows, {} columns".format(len(sample_df), len(sample_df.columns)))

    # Load scraper output (Excel)
    scraper_df = pd.read_excel(latest_file, header=None)
    print("[OK] Scraper data loaded: {} rows, {} columns".format(len(scraper_df), len(scraper_df.columns)))

    # Get 2024 data from sample
    sample_2024 = sample_df[sample_df.iloc[:, 0] == 2024]
    if len(sample_2024) == 0:
        print("\n[ERROR] No 2024 data found in sample file")
        return

    sample_2024_values = sample_2024.iloc[0].values

    # Get 2024 data from scraper (row 3, index 2)
    if len(scraper_df) < 3:
        print("\n[ERROR] Scraper output has fewer than 3 rows")
        return

    scraper_2024_values = scraper_df.iloc[2].values

    print("\n[2] Comparing 2024 data...")
    print("\n{:<50} {:>15} {:>15} {:>10}".format("Field", "Sample", "Scraper", "Match?"))
    print("-" * 90)

    # Important columns to compare
    comparisons = {
        0: "Year",
        1: "Money market investments",
        2: "Loans",
        3: "Swiss francs bonds",
        4: "Foreign currency bonds",
        5: "Government bonds",
        6: "Inflation-protected bonds",
        7: "Emerging market bonds",
        8: "Corporate bonds",
        9: "High yield bonds",
        10: "Securitised bonds",
        11: "Equities",
        12: "Large caps",
        13: "Emerging markets",
        14: "Small and mid caps",
        15: "Real estate",
        16: "Switzerland direct",
        17: "Switzerland listed",
        18: "Global listed",
        19: "Global not listed",
        20: "Gold",
        21: "Multi-Asset portfolio",
        22: "Market portfolio",
        23: "Currency hedging",
        26: "Market portfolio after hedging",
        27: "Basic portfolio - Treasury",
        28: "Strategic: Foreign bonds %",
        29: "Strategic: Equities %",
        30: "Strategic: Bonds CHF %",
        31: "Strategic: Real estate %",
        32: "Strategic: Precious metals %",
    }

    matches = 0
    mismatches = 0

    for col, name in comparisons.items():
        if col >= len(sample_2024_values) or col >= len(scraper_2024_values):
            continue

        sample_val = str(sample_2024_values[col])
        scraper_val = str(scraper_2024_values[col])

        # Normalize values for comparison
        sample_clean = sample_val.strip().upper()
        scraper_clean = scraper_val.strip().upper()

        match = sample_clean == scraper_clean
        match_symbol = "✓" if match else "✗"

        print("{:<50} {:>15} {:>15} {:>10}".format(
            name[:50],
            sample_val[:15],
            scraper_val[:15],
            match_symbol
        ))

        if match:
            matches += 1
        else:
            mismatches += 1

    print("-" * 90)
    print("\n[3] Summary:")
    print("    Total fields compared: {}".format(matches + mismatches))
    print("    Matches: {}".format(matches))
    print("    Mismatches: {}".format(mismatches))

    if mismatches == 0:
        print("\n" + "="*70)
        print("  ✓✓✓ PERFECT MATCH! All data matches sample ✓✓✓")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("  ⚠ {} mismatches found - review above".format(mismatches))
        print("="*70)

    # Show detailed differences
    if mismatches > 0:
        print("\n[4] Detailed Mismatches:")
        for col, name in comparisons.items():
            if col >= len(sample_2024_values) or col >= len(scraper_2024_values):
                continue

            sample_val = str(sample_2024_values[col])
            scraper_val = str(scraper_2024_values[col])

            if sample_val.strip().upper() != scraper_val.strip().upper():
                print("\n  Column {}: {}".format(col, name))
                print("    Expected: '{}'".format(sample_val))
                print("    Got:      '{}'".format(scraper_val))


if __name__ == "__main__":
    compare_results()
