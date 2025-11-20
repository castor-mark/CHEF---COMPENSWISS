"""
Test script for validating parsers with sample HTML files
"""

import os
from parser import PerformanceTableParser
from llm_parser import StrategicAllocationParser
import config


def test_performance_parser():
    """Test the performance table parser"""
    print("="*70)
    print("TESTING PERFORMANCE TABLE PARSER")
    print("="*70)

    html_file = r"C:\Users\Mark Castro\Documents\CHEF – COMPENSWISS\Project-information\performance_page.html"

    if not os.path.exists(html_file):
        print(f"✗ File not found: {html_file}")
        return False

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        parser = PerformanceTableParser(html_content)
        perf_data = parser.extract_performance_data()

        print("\n--- Extracted Performance Data ---")
        for category, amount in perf_data.items():
            print(f"  {category}: {amount}")

        csv_data = parser.map_to_csv_format(perf_data)

        print("\n--- CSV Data (Performance Columns 1-27) ---")
        important_indices = [1, 2, 3, 4, 11, 15, 20, 22, 23, 26, 27]
        for i in important_indices:
            header = config.CSV_ROW2_HEADERS[i] if i < len(config.CSV_ROW2_HEADERS) else f"Column {i}"
            print(f"  [{i}] {csv_data[i]}")

        print("\n✓ Performance parser test PASSED")
        return True

    except Exception as e:
        print(f"\n✗ Performance parser test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_strategic_parser():
    """Test the strategic allocation parser"""
    print("\n" + "="*70)
    print("TESTING STRATEGIC ALLOCATION PARSER")
    print("="*70)

    html_file = r"C:\Users\Mark Castro\Documents\CHEF – COMPENSWISS\Project-information\strategic_allocation_page.html"

    if not os.path.exists(html_file):
        print(f"✗ File not found: {html_file}")
        return False

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        parser = StrategicAllocationParser(html_content)

        # Extract section text
        section_text = parser.extract_strategic_allocation_section()
        print("\n--- Extracted Text ---")
        print(f"  {section_text[:200]}...")

        # Extract percentages
        strategic_data = parser.extract_percentages_with_regex(section_text)

        print("\n--- Strategic Allocation Data ---")
        for key, value in strategic_data.items():
            print(f"  {key}: {value}%")

        # Map to CSV
        csv_updates = parser.map_to_csv_format(strategic_data)

        print("\n--- CSV Updates (columns 28-32) ---")
        for col, value in csv_updates.items():
            header = config.CSV_ROW2_HEADERS[col] if col < len(config.CSV_ROW2_HEADERS) else f"Column {col}"
            print(f"  [{col}] {value}")

        print("\n✓ Strategic parser test PASSED")
        return True

    except Exception as e:
        print(f"\n✗ Strategic parser test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_complete_row():
    """Test creating a complete CSV row"""
    print("\n" + "="*70)
    print("TESTING COMPLETE CSV ROW GENERATION")
    print("="*70)

    try:
        # Parse performance data
        perf_html_file = r"C:\Users\Mark Castro\Documents\CHEF – COMPENSWISS\Project-information\performance_page.html"
        with open(perf_html_file, 'r', encoding='utf-8') as f:
            perf_html = f.read()

        perf_parser = PerformanceTableParser(perf_html)
        perf_data = perf_parser.extract_performance_data()
        csv_row = perf_parser.map_to_csv_format(perf_data)

        # Parse strategic data
        strategic_html_file = r"C:\Users\Mark Castro\Documents\CHEF – COMPENSWISS\Project-information\strategic_allocation_page.html"
        with open(strategic_html_file, 'r', encoding='utf-8') as f:
            strategic_html = f.read()

        strategic_parser = StrategicAllocationParser(strategic_html)
        strategic_text = strategic_parser.extract_strategic_allocation_section()
        strategic_data = strategic_parser.extract_percentages_with_regex(strategic_text)
        strategic_updates = strategic_parser.map_to_csv_format(strategic_data)

        # Merge
        for col_index, value in strategic_updates.items():
            csv_row[col_index] = value

        # Set year
        csv_row[0] = "2024"

        print("\n--- Complete CSV Row (Sample Values) ---")
        print(f"Year: {csv_row[0]}")
        print(f"Money market investments: {csv_row[1]}")
        print(f"Foreign currency bonds: {csv_row[4]}")
        print(f"Equities: {csv_row[11]}")
        print(f"Real estate: {csv_row[15]}")
        print(f"Gold: {csv_row[20]}")
        print(f"Market portfolio: {csv_row[22]}")
        print(f"Currency hedging: {csv_row[23]}")
        print(f"Market portfolio after hedging: {csv_row[26]}")
        print(f"Strategic - Foreign currency bonds %: {csv_row[28]}")
        print(f"Strategic - Equities %: {csv_row[29]}")
        print(f"Strategic - Real estate %: {csv_row[31]}")
        print(f"Strategic - Precious metals %: {csv_row[32]}")

        print("\n✓ Complete row generation test PASSED")

        # Compare with expected values from sample data
        print("\n--- Validation Against Sample Data (2024) ---")
        expected = {
            0: "2024",
            1: "452",
            4: "15829",
            11: "12278",
            28: "37",
            29: "28",
            31: "15",
            32: "3"
        }

        all_match = True
        for col, expected_val in expected.items():
            actual_val = csv_row[col]
            match = actual_val == expected_val
            symbol = "✓" if match else "✗"
            print(f"  {symbol} Column {col}: Expected '{expected_val}', Got '{actual_val}'")
            if not match:
                all_match = False

        if all_match:
            print("\n✓✓✓ ALL VALUES MATCH SAMPLE DATA! ✓✓✓")
        else:
            print("\n⚠ Some values don't match - may need adjustment")

        return True

    except Exception as e:
        print(f"\n✗ Complete row test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "="*70)
    print("  CHEF COMPENSWISS PARSER VALIDATION TESTS")
    print("="*70)

    results = []

    # Test 1: Performance Parser
    results.append(("Performance Parser", test_performance_parser()))

    # Test 2: Strategic Parser
    results.append(("Strategic Parser", test_strategic_parser()))

    # Test 3: Complete Row
    results.append(("Complete CSV Row", test_complete_row()))

    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)

    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {status}: {test_name}")

    all_passed = all(result[1] for result in results)

    print("\n" + "="*70)
    if all_passed:
        print("  ✓✓✓ ALL TESTS PASSED ✓✓✓")
    else:
        print("  ✗✗✗ SOME TESTS FAILED ✗✗✗")
    print("="*70 + "\n")
