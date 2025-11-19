# CHEF COMPENSWISS Data Scraper

Automated web scraper for extracting investment performance data from the CHEF COMPENSWISS annual report website.

## Overview

This scraper:
- Navigates to the **live CHEF COMPENSWISS website**
- Extracts investment performance data from the performance table
- Extracts strategic allocation percentages from text
- Outputs data to Excel (.xlsx) format
- Creates timestamped reports and maintains a "latest" folder

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Chrome WebDriver:
- Download ChromeDriver matching your Chrome version
- Add to system PATH

## Configuration

Edit `config.py` to configure the scraper:

```python
# Runtime settings
HEADLESS = True  # Set to False to see the browser
YEAR = "latest"  # Set to specific year (e.g., 2024) or "latest" to use current year
```

## Usage

**Option 1: Use config settings**
```bash
python scraper.py
```
This uses `HEADLESS` and `YEAR` settings from config.py

**Option 2: Specify year via command line**
```bash
python scraper.py 2024
```
or
```bash
python scraper.py latest
```

The command line argument overrides the config setting.

## Output Structure

Per the AfricaAI runbook, the scraper creates:

```
reports/
├── 20250119/                           # Timestamped folder (YYYYMMDD)
│   ├── CHEF_COMPENSWISS_DATA_20250119.xls
│   ├── CHEF_COMPENSWISS_META_20250119.xls
│   └── CHEF_COMPENSWISS_20250119.zip  # ZIP archive containing both files
└── latest/                             # Always contains latest run
    ├── CHEF_COMPENSWISS_DATA_20250119.xls
    ├── CHEF_COMPENSWISS_META_20250119.xls
    └── CHEF_COMPENSWISS_20250119.zip
```

**File Naming Convention (per runbook):**
- DATA file: `CHEF_COMPENSWISS_DATA_YYYYMMDD.xls`
- METADATA file: `CHEF_COMPENSWISS_META_YYYYMMDD.xls`
- ZIP archive: `CHEF_COMPENSWISS_YYYYMMDD.zip`

where YYYYMMDD is the date the file was created.

## Data Extracted

### Performance Data (from table)
- Money market investments
- Loans to public entities
- Swiss franc bonds
- Foreign currency bonds (with subcategories)
- Equities (with subcategories)
- Real estate (with subcategories)
- Gold
- Multi-Asset portfolio
- Market portfolio totals

### Strategic Allocation (from text)
- Foreign currency bonds %
- Equities %
- Bonds in CHF %
- Real estate %
- Precious metals %

## Configuration

All settings are in `config.py`:
- URLs
- CSV column mappings
- Table category mappings
- Selenium timeouts

## Files

- `scraper.py` - Main scraper (navigates site, extracts data, saves Excel)
- `config.py` - Configuration and mappings
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Requirements

- Python 3.8+
- Chrome browser
- ChromeDriver
- Internet connection (to access live site)

## Notes

- The scraper accesses the live website at `https://ar.compenswiss.ch`
- Data is extracted directly from the loaded web pages
- All column headers match the exact format from the sample data
- Reports are saved in both timestamped and "latest" folders
