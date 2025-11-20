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

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Chrome WebDriver
- Download ChromeDriver matching your Chrome version
- Add to system PATH

### 3. Configure API Keys (Optional - for LLM fallback)
```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add at least one API key
# Recommended: GroqCloud (fastest, most reliable)
```

Get free API keys:
- **GroqCloud** (recommended): https://console.groq.com/keys
- **OpenRouter**: https://openrouter.ai/keys
- **Gemini**: https://aistudio.google.com/app/apikey

### 4. Test Your Setup
```bash
# Test the scraper
python scraper.py

# Test LLM fallback (optional)
python bin/test_llm_fallback.py
```

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

### Strategic Allocation (from text using hybrid extraction)
- Foreign currency bonds %
- Equities %
- Bonds in CHF %
- Real estate %
- Precious metals %

**Extraction Strategy:** Multi-tier fallback approach
- **Tier 1:** Specific regex patterns (highest accuracy)
- **Tier 2:** Sentence-based extraction with 15-word proximity check
- **Tier 3:** LLM-based extraction (GroqCloud, OpenRouter, Gemini)
- Features: Supports decimal percentages, 0% values, adaptable to text changes
- Validation: Tested by 4 AI models (avg confidence: 8/10)

**LLM Fallback:** Automatic fallback to AI models when regex fails
- GroqCloud API (llama-3.3-70b, mixtral-8x7b, gemma2-9b) - Free tier
- OpenRouter API (qwen, deepseek, llama models) - Free models available
- Gemini API (gemini-2.0-flash-exp) - Free tier
- Configure in `.env` file - see [LLM Configuration](#llm-fallback-configuration)

## Configuration

All settings are in `config.py`:
- URLs
- CSV column mappings
- Table category mappings
- Selenium timeouts

## Project Structure

```
CHEF – COMPENSWISS/
├── scraper.py              # Main production scraper
├── llm_fallback.py         # LLM fallback extraction module
├── config.py               # Configuration and strategic allocation patterns
├── requirements.txt        # Python dependencies
├── .env.example            # Environment configuration template
├── .env                    # Your API keys (create from .env.example)
├── README.md              # This file
├── bin/                   # Test files and development tools
│   ├── test_hybrid_strategy.py
│   ├── test_edge_cases.py
│   ├── test_llm_fallback.py
│   ├── test_all_providers.py
│   └── README.md
├── reports/               # Generated data files
│   ├── YYYYMMDD/         # Timestamped folders
│   └── latest/           # Latest run
└── Project-information/   # Project documentation
    └── Zen-Models-Updated.csv
```

## Key Files

- **scraper.py** - Main production scraper with hybrid extraction strategy
- **config.py** - Configuration including STRATEGIC_ALLOCATION_CONFIG
- **requirements.txt** - Python dependencies
- **bin/** - Test files and development tools (see bin/README.md)

## Requirements

- Python 3.8+
- Chrome browser
- ChromeDriver
- Internet connection (to access live site)

## LLM Fallback Configuration

The scraper includes automatic LLM fallback when standard extraction fails.

**Quick Setup:**
```bash
# 1. Copy the example environment file
cp .env.example .env

# 2. Edit .env and add your API keys
# (Get free keys from the links below)
```

**Configuration Options:**

See [.env.example](.env.example) for full configuration with detailed comments.

Key settings:
```bash
# API Keys (get at least one, GroqCloud recommended)
GROQ_CLOUD_API_KEY=your_key_here        # Free: 30 RPM, 14.4K RPD
OPENROUTER_API_KEY=your_key_here        # Free models available
GEMINI_API_KEY=your_key_here            # Free: 15 RPM, 1.5K RPD

# Enable/disable LLM fallback
ENABLE_LLM_FALLBACK=true

# Provider priority (which to try first)
LLM_PROVIDER_PRIORITY=groq,openrouter,gemini
```

**Free API Keys:**
- GroqCloud: https://console.groq.com/keys
- OpenRouter: https://openrouter.ai/keys
- Gemini: https://aistudio.google.com/app/apikey

**Provider Performance (Based on Test Results):**
- **GroqCloud** (llama-3.3-70b-versatile): 100% accuracy, 2.5s (FASTEST)
- **OpenRouter** (meta-llama/llama-3.3-70b-instruct:free): 100% accuracy, 14s
- **Gemini** (gemini-2.0-flash-exp): May hit quota limits

**Test LLM Fallback:**
```bash
python bin/test_llm_fallback.py
```

**Change Provider Priority:**

To use OpenRouter first, edit `.env`:
```bash
LLM_PROVIDER_PRIORITY=openrouter,groq,gemini
```

To use only Gemini (skip others):
```bash
LLM_PROVIDER_PRIORITY=gemini
```

## Notes

- The scraper accesses the live website at `https://ar.compenswiss.ch`
- Data is extracted directly from the loaded web pages
- All column headers match the exact format from the sample data
- Reports are saved in both timestamped and "latest" folders
- LLM fallback activates automatically when regex extraction is incomplete
- Multiple API providers ensure high reliability (GroqCloud → OpenRouter → Gemini)
