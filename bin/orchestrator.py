# -*- coding: utf-8 -*-
"""
Main Orchestrator for CHEF COMPENSWISS Data Scraper
Coordinates scraping, parsing, and CSV output
"""

import csv
import datetime
import os
from scraper import CompensswissScraper
from parser import PerformanceTableParser, StrategicAllocationParser
import config


class CompensswissOrchestrator:
    """Orchestrates the complete data extraction workflow"""

    def __init__(self, headless=True):
        """Initialize orchestrator"""
        self.scraper = CompensswissScraper(headless=headless)
        self.csv_row = None

    def run_workflow(self, year=None):
        """
        Run the complete data extraction workflow
        Args:
            year: Year for the data (default: current year)
        Returns: CSV row data
        """
        try:
            if year is None:
                year = datetime.datetime.now().year

            print("\n" + "="*70)
            print("  CHEF COMPENSWISS Data Extraction - Year {}".format(year))
            print("="*70)

            # Step 1: Setup browser
            print("\n[1/4] Setting up browser...")
            self.scraper.setup_driver()

            # Step 2: Get performance data
            print("\n[2/4] Extracting performance data...")
            perf_html = self.scraper.get_performance_page()
            perf_parser = PerformanceTableParser(perf_html)
            perf_data = perf_parser.extract_performance_data()
            self.csv_row = perf_parser.map_to_csv(perf_data)

            # Step 3: Get strategic allocation data
            print("\n[3/4] Extracting strategic allocation...")
            strategic_html = self.scraper.get_strategic_allocation_page()
            strategic_parser = StrategicAllocationParser(strategic_html)
            strategic_data = strategic_parser.extract_strategic_allocation()
            strategic_parser.map_to_csv(strategic_data, self.csv_row)

            # Step 4: Set year
            self.csv_row[0] = str(year)
            print("\n[4/4] Data extraction complete!")

            # Close browser
            self.scraper.close()

            print("\n" + "="*70)
            print("  EXTRACTION COMPLETE")
            print("="*70)

            return self.csv_row

        except Exception as e:
            print("\n[ERROR] Workflow failed: {}".format(e))
            self.scraper.close()
            raise

    def save_to_csv(self, output_file, year=None, append=True):
        """
        Save extracted data to CSV file
        Args:
            output_file: Path to output CSV file
            year: Year for the data
            append: If True, append to existing file
        """
        try:
            # Run extraction if needed
            if self.csv_row is None:
                self.run_workflow(year)

            print("\n[->] Saving to CSV: {}".format(output_file))

            # Check if file exists
            file_exists = os.path.exists(output_file)

            # Determine mode
            if append and file_exists:
                mode = 'a'
                write_headers = False
                print("[->] Appending to existing file")
            else:
                mode = 'w'
                write_headers = True
                print("[->] Creating new file")

            # Write CSV
            with open(output_file, mode, newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                if write_headers:
                    writer.writerow(config.CSV_HEADERS)
                    writer.writerow(config.CSV_ROW2_HEADERS)
                    print("[OK] Headers written")

                writer.writerow(self.csv_row)
                print("[OK] Data row written for year {}".format(self.csv_row[0]))

            print("[OK] CSV saved: {}".format(output_file))

        except Exception as e:
            print("[ERROR] Failed to save CSV: {}".format(e))
            raise

    def display_summary(self):
        """Display summary of extracted data"""
        if self.csv_row is None:
            print("No data extracted yet")
            return

        print("\n" + "="*70)
        print("  DATA SUMMARY")
        print("="*70)

        print("\nYear: {}".format(self.csv_row[0]))

        print("\n--- Performance Data ---")
        print("Money market investments: {}".format(self.csv_row[1]))
        print("Swiss francs bonds: {}".format(self.csv_row[3]))
        print("Foreign currency bonds: {}".format(self.csv_row[4]))
        print("Equities: {}".format(self.csv_row[11]))
        print("Real estate: {}".format(self.csv_row[15]))
        print("Gold: {}".format(self.csv_row[20]))
        print("Market portfolio: {}".format(self.csv_row[22]))
        print("Market portfolio after hedging: {}".format(self.csv_row[26]))

        print("\n--- Strategic Allocation ---")
        print("Foreign currency bonds: {}%".format(self.csv_row[28]))
        print("Equities: {}%".format(self.csv_row[29]))
        print("Bonds in CHF: {}%".format(self.csv_row[30]))
        print("Real estate: {}%".format(self.csv_row[31]))
        print("Precious metals: {}%".format(self.csv_row[32]))

        print("\n" + "="*70)


if __name__ == "__main__":
    import sys

    # Get year from command line or use current year
    year = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.datetime.now().year

    # Create orchestrator (headless=False to see browser)
    orchestrator = CompensswissOrchestrator(headless=True)

    # Run workflow
    csv_data = orchestrator.run_workflow(year=year)

    # Display summary
    orchestrator.display_summary()

    # Save to CSV
    output_dir = r"C:\Users\Mark Castro\Documents\CHEF – COMPENSWISS\output"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "COMPENSWISS_DATA_{}.csv".format(year))
    orchestrator.save_to_csv(output_file, year=year, append=False)

    print("\n[OK] Complete! Data saved to: {}".format(output_file))
