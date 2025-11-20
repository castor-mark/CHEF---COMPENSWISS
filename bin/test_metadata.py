# -*- coding: utf-8 -*-
"""
Test script to verify metadata generation matches sample file
"""

import pandas as pd
import config

def test_metadata():
    """Compare generated metadata structure with sample file"""

    print("="*70)
    print("  METADATA VERIFICATION TEST")
    print("="*70)

    # Load sample metadata
    sample_path = r"C:\Users\Mark Castro\Documents\CHEF – COMPENSWISS\Project-information\CHEF_COMPENSWISS_META_20240617.xlsx"
    df_sample = pd.read_excel(sample_path)

    print("\n[1] Sample metadata loaded")
    print("    Rows: {}".format(len(df_sample)))
    print("    Columns: {}".format(len(df_sample.columns)))
    print("    Column names: {}".format(list(df_sample.columns)))

    # Generate metadata using scraper logic
    metadata_rows = []

    for col_idx in range(1, 33):
        code = config.CSV_HEADERS[col_idx]
        description = config.CSV_ROW2_HEADERS[col_idx]
        code_mnemonic = code.split('@')[0] if '@' in code else code
        # Remove .A.1 suffix
        if code_mnemonic.endswith('.A.1'):
            code_mnemonic = code_mnemonic[:-4]

        if col_idx <= 27:
            metadata_type = config.METADATA_PERFORMANCE.copy()
        else:
            metadata_type = config.METADATA_STRATEGIC.copy()

        row = {
            "CODE": code,
            "CODE_MNEMONIC": code_mnemonic,
            "DESCRIPTION": description,
            "FREQUENCY": config.METADATA_COMMON["FREQUENCY"],
            "MULTIPLIER": metadata_type["MULTIPLIER"],
            "AGGREGATION_TYPE": config.METADATA_COMMON["AGGREGATION_TYPE"],
            "UNIT_TYPE": metadata_type["UNIT_TYPE"],
            "DATA_TYPE": metadata_type["DATA_TYPE"],
            "DATA_UNIT": metadata_type["DATA_UNIT"],
            "SEASONALLY_ADJUSTED": config.METADATA_COMMON["SEASONALLY_ADJUSTED"],
            "ANNUALIZED": config.METADATA_COMMON["ANNUALIZED"],
            "STATE": config.METADATA_COMMON["STATE"],
            "PROVIDER_MEASURE_URL": metadata_type["PROVIDER_MEASURE_URL"],
            "PROVIDER": config.METADATA_COMMON["PROVIDER"],
            "SOURCE": config.METADATA_COMMON["SOURCE"],
            "SOURCE_DESCRIPTION": config.METADATA_COMMON["SOURCE_DESCRIPTION"],
            "COUNTRY": config.METADATA_COMMON["COUNTRY"],
            "DATASET": config.METADATA_COMMON["DATASET"]
        }
        metadata_rows.append(row)

    df_generated = pd.DataFrame(metadata_rows)

    print("\n[2] Generated metadata")
    print("    Rows: {}".format(len(df_generated)))
    print("    Columns: {}".format(len(df_generated.columns)))

    # Compare structure
    print("\n[3] Comparing structure...")

    if len(df_sample) == len(df_generated):
        print("    [OK] Row count matches: {}".format(len(df_sample)))
    else:
        print("    [ERROR] Row count mismatch: {} vs {}".format(len(df_sample), len(df_generated)))

    if len(df_sample.columns) == len(df_generated.columns):
        print("    [OK] Column count matches: {}".format(len(df_sample.columns)))
    else:
        print("    [ERROR] Column count mismatch: {} vs {}".format(len(df_sample.columns), len(df_generated.columns)))

    # Compare column names
    sample_cols = set(df_sample.columns)
    generated_cols = set(df_generated.columns)

    if sample_cols == generated_cols:
        print("    [OK] All column names match")
    else:
        missing = sample_cols - generated_cols
        extra = generated_cols - sample_cols
        if missing:
            print("    [ERROR] Missing columns: {}".format(missing))
        if extra:
            print("    [ERROR] Extra columns: {}".format(extra))

    # Compare specific rows
    print("\n[4] Comparing specific rows...")

    test_rows = [0, 10, 20, 27, 28, 31]  # Sample rows across performance and strategic

    for idx in test_rows:
        if idx < len(df_sample) and idx < len(df_generated):
            sample_row = df_sample.iloc[idx]
            generated_row = df_generated.iloc[idx]

            matches = True
            mismatches = []

            for col in df_sample.columns:
                if col in df_generated.columns:
                    if str(sample_row[col]) != str(generated_row[col]):
                        matches = False
                        mismatches.append("{}('{}' vs '{}')".format(col, sample_row[col], generated_row[col]))

            if matches:
                print("    Row {}: [OK] {}".format(idx, sample_row['CODE']))
            else:
                print("    Row {}: [ERROR] Mismatches in: {}".format(idx, ", ".join(mismatches[:3])))

    # Compare key fields for all rows
    print("\n[5] Comparing key fields across all rows...")

    key_fields = ['CODE', 'CODE_MNEMONIC', 'DESCRIPTION', 'MULTIPLIER', 'UNIT_TYPE',
                  'DATA_TYPE', 'DATA_UNIT', 'PROVIDER', 'COUNTRY', 'DATASET']

    for field in key_fields:
        if field in df_sample.columns and field in df_generated.columns:
            matches = (df_sample[field].astype(str) == df_generated[field].astype(str)).sum()
            total = len(df_sample)
            if matches == total:
                print("    {}: [OK] {}/{} match".format(field, matches, total))
            else:
                print("    {}: [ERROR] {}/{} match".format(field, matches, total))
                # Show first mismatch
                for i in range(total):
                    if str(df_sample[field].iloc[i]) != str(df_generated[field].iloc[i]):
                        print("        First mismatch at row {}: '{}' vs '{}'".format(
                            i, df_sample[field].iloc[i], df_generated[field].iloc[i]))
                        break

    print("\n" + "="*70)
    print("  TEST COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_metadata()
