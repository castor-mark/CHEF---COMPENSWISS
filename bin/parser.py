# -*- coding: utf-8 -*-
"""
HTML Parser for CHEF COMPENSWISS data extraction
Extracts data from performance tables and strategic allocation text
"""

from bs4 import BeautifulSoup
import re
import config


class PerformanceTableParser:
    """Parser for extracting data from the performance table"""

    def __init__(self, html_content):
        """Initialize parser with HTML content"""
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_performance_data(self):
        """
        Extract Amount (in CHF million) from performance table
        Returns: Dictionary mapping category names to amounts
        """
        try:
            print("\n[->] Parsing performance table...")

            # Find the table
            table = self.soup.find('table', class_='table--chart')
            if not table:
                raise ValueError("Performance table not found")

            # Get rows
            tbody = table.find('tbody')
            if not tbody:
                raise ValueError("Table body not found")

            rows = tbody.find_all('tr')
            print("[OK] Found {} rows in table".format(len(rows)))

            # Store extracted data
            data = {}

            # Process each row
            for row in rows:
                cells = row.find_all('td')

                if len(cells) < 2:
                    continue

                # Extract category (first column)
                category = cells[0].get_text(strip=True)
                if not category:
                    continue

                # Extract amount (second column)
                amount_text = cells[1].get_text(strip=True)
                if not amount_text:
                    continue

                # Clean amount: remove spaces and non-breaking spaces
                amount_clean = amount_text.replace('\xa0', '').replace(' ', '').replace(',', '')

                # Handle negative numbers
                if amount_clean.startswith('-'):
                    amount_clean = '-' + amount_clean[1:].replace('-', '')

                data[category] = amount_clean
                print("  {} = {}".format(category, amount_clean))

            print("[OK] Extracted {} data points".format(len(data)))
            return data

        except Exception as e:
            print("[ERROR] Error parsing performance table: {}".format(e))
            raise

    def map_to_csv(self, performance_data):
        """
        Map extracted performance data to CSV columns
        Returns: List of values for CSV columns 0-32
        """
        try:
            print("\n[->] Mapping data to CSV format...")

            # Initialize with NA
            csv_data = ["NA"] * 33
            csv_data[0] = ""  # Year column

            # Map using config
            for category, col_index in config.PERFORMANCE_TABLE_MAPPING.items():
                if category in performance_data:
                    csv_data[col_index] = performance_data[category]
                    print("  Col {} = {}".format(col_index, performance_data[category]))

            print("[OK] Performance data mapped")
            return csv_data

        except Exception as e:
            print("[ERROR] Error mapping to CSV: {}".format(e))
            raise


class StrategicAllocationParser:
    """Parser for extracting strategic allocation percentages from text"""

    def __init__(self, html_content):
        """Initialize parser with HTML content"""
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_strategic_allocation(self):
        """
        Extract percentages from 'Structure of the strategic allocation' section
        Returns: Dictionary with asset class -> percentage
        """
        try:
            print("\n[->] Extracting strategic allocation text...")

            # Find heading
            heading = self.soup.find('h3', string=re.compile(r'Structure of the strategic allocation', re.IGNORECASE))
            if not heading:
                heading = self.soup.find('a', id='a4')
                if heading:
                    heading = heading.find_parent('h3')

            if not heading:
                raise ValueError("Strategic allocation heading not found")

            # Get paragraphs after heading
            paragraphs = []
            current = heading.find_next_sibling()

            while current:
                if current.name == 'p':
                    text = current.get_text(strip=True)
                    if text:
                        paragraphs.append(text)
                elif current.name in ['h2', 'h3', 'h4']:
                    break
                current = current.find_next_sibling()

            full_text = " ".join(paragraphs)
            print("[OK] Extracted text ({} chars)".format(len(full_text)))

            # Extract percentages using regex
            data = self.extract_percentages(full_text)
            return data

        except Exception as e:
            print("[ERROR] Error extracting strategic allocation: {}".format(e))
            raise

    def extract_percentages(self, text):
        """Extract percentage values using regex"""
        print("\n[->] Extracting percentages...")

        data = {}

        # Patterns for each asset class
        patterns = {
            "Foreign currency bonds": r"Foreign currency bonds account for (\d+)%",
            "Equities": r"Equities account for (\d+)%",
            "Bonds in CHF": r"denominated in CHF account for (\d+)%",
            "Real estate": r"Real estate.*?accounts for (\d+)%",
            "Precious metals": r"invests (\d+)% in precious metals",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                percentage = match.group(1)
                data[key] = percentage
                print("  {} = {}%".format(key, percentage))
            else:
                data[key] = "NA"
                print("  {} = NOT FOUND".format(key))

        return data

    def map_to_csv(self, strategic_data, csv_data):
        """
        Map strategic allocation to CSV columns 28-32
        Updates the csv_data array in place
        """
        try:
            print("\n[->] Mapping strategic allocation to CSV...")

            mapping = {
                "Foreign currency bonds": 28,
                "Equities": 29,
                "Bonds in CHF": 30,
                "Real estate": 31,
                "Precious metals": 32,
            }

            for key, col_index in mapping.items():
                value = strategic_data.get(key, "NA")
                csv_data[col_index] = value
                print("  Col {} = {}".format(col_index, value))

            print("[OK] Strategic allocation mapped")

        except Exception as e:
            print("[ERROR] Error mapping strategic allocation: {}".format(e))
            raise


if __name__ == "__main__":
    import os

    # Test performance parser
    perf_file = r"C:\Users\Mark Castro\Documents\CHEF – COMPENSWISS\Project-information\performance_page.html"
    if os.path.exists(perf_file):
        print("=== Testing Performance Parser ===")
        with open(perf_file, 'r', encoding='utf-8') as f:
            html = f.read()

        parser = PerformanceTableParser(html)
        data = parser.extract_performance_data()
        csv_data = parser.map_to_csv(data)

    # Test strategic parser
    strategic_file = r"C:\Users\Mark Castro\Documents\CHEF – COMPENSWISS\Project-information\strategic_allocation_page.html"
    if os.path.exists(strategic_file):
        print("\n=== Testing Strategic Parser ===")
        with open(strategic_file, 'r', encoding='utf-8') as f:
            html = f.read()

        parser = StrategicAllocationParser(html)
        data = parser.extract_strategic_allocation()
        parser.map_to_csv(data, csv_data)

        # Show sample results
        print("\n=== Sample CSV Data ===")
        print("Year: {}".format(csv_data[0]))
        print("Money market: {}".format(csv_data[1]))
        print("Foreign bonds: {}".format(csv_data[4]))
        print("Equities: {}".format(csv_data[11]))
        print("Strategic - Foreign bonds %: {}".format(csv_data[28]))
        print("Strategic - Equities %: {}".format(csv_data[29]))
