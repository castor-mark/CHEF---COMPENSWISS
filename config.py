# Configuration for CHEF COMPENSWISS Data Scraper

# Base URL
BASE_URL = "https://ar.compenswiss.ch"

# Page URLs
INVESTMENTS_PAGE = f"{BASE_URL}/en_GB/investments"
PERFORMANCE_PAGE = f"{BASE_URL}/en_GB/investments/performance"
STRATEGIC_ALLOCATION_PAGE = f"{BASE_URL}/en_GB/investments/strategic-asset-allocation"

# Selenium settings
SELENIUM_WAIT_TIME = 10
SELENIUM_PAGE_LOAD_TIMEOUT = 30

# Runtime settings
HEADLESS = True  # Set to False to see the browser
YEAR = "latest"  # Set to specific year (e.g., 2024) or "latest" to use current year

# Dataset settings
DATASET_NAME = "CHEF_COMPENSWISS"  # Used in file naming


# CSV Column Headers (exact order from sample data)
CSV_HEADERS = [
    "",
    "COMPENSWISS.MONEYMARKET.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.LOANS.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.DOMESTICBONDSLOCALFX.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.FOREIGNBONDS.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.GOVERNMENTBONDS.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.ILBONDS.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.EMBONDS.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.CORPORATEBONDS.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.HIGHYIELD.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.OTHERBONDS.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.EQUITIES.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.LARGECAPEQUITIES.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.EMEQUITIES.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.SMALLCAPEQUITIES.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.REALESTATE.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.DOMESTICREALESTATE.LEVEL.DIRECT.A.1@COMPENSWISS",
    "COMPENSWISS.DOMESTICREALESTATE.LEVEL.INDIRECT.A.1@COMPENSWISS",
    "COMPENSWISS.FOREIGNREALESTATE.LEVEL.INDIRECT.A.1@COMPENSWISS",
    "COMPENSWISS.FOREIGNREALESTATE.LEVEL.DIRECT.A.1@COMPENSWISS",
    "COMPENSWISS.GOLD.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.MULTIASSET.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.TOTAL.LEVEL.UNHEDGED.A.1@COMPENSWISS",
    "COMPENSWISS.CURRENCYHEDGING.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.INTERESTRATEHEDGING.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.EQUITYOVERLAY.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.TOTAL.LEVEL.HEDGED.A.1@COMPENSWISS",
    "COMPENSWISS.CASH.LEVEL.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.FOREIGNBONDS.TARGETALLOCATION.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.EQUITIES.TARGETALLOCATION.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.DOMESTICBONDSLOCALFX.TARGETALLOCATION.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.REALESTATE.TARGETALLOCATION.NONE.A.1@COMPENSWISS",
    "COMPENSWISS.PRECIOUSMETALS.TARGETALLOCATION.NONE.A.1@COMPENSWISS",
]

# CSV Row 2 Headers (descriptive names)
CSV_ROW2_HEADERS = [
    "",
    "Detailed investment perfomance, Money market investment, Amount",
    "Detailed investment perfomance, Loans, Amount",
    "Detailed investment perfomance, Swiss francs bonds, Amount",
    "Detailed investment perfomance, Foreign currency bonds, Amount",
    "Detailed investment perfomance, Government bonds, Amount",
    "Detailed investment perfomance, Inflation-protected Bonds, Amount",
    "Detailed investment perfomance, Emerging markets Bonds, Amount",
    "Detailed investment perfomance, Corporate bonds, Amount",
    "Detailed investment perfomance, Higher Yielding Bonds, Amount",
    "Detailed investment perfomance, Securitised Bonds, Amount",
    "Detailed investment perfomance, Equities, Amount",
    "Detailed investment perfomance, Large Caps, Amount",
    "Detailed investment perfomance, Emerging markets Bonds, Amount",
    "Detailed investment perfomance, Small and mid caps, Amount",
    "Detailed investment perfomance, Real Estate, Amount",
    "Detailed investment perfomance, Swiss Direct, Amount",
    "Detailed investment perfomance, Swiss Listed, Amount",
    "Detailed investment perfomance, Global Listed, Amount",
    "Detailed investment perfomance, Global not listed, Amount",
    "Detailed investment perfomance, Gold, Amount",
    "Detailed investment perfomance, Multi-Asset Portfolio, Amount",
    "Detailed investment perfomance, Market Portfolio, Amount",
    "Detailed investment perfomance, Currency Hedging, Amount",
    "Detailed investment perfomance, Interest Rate Hedging, Amount",
    "Detailed investment perfomance, Equity Overlay, Amount",
    "Detailed investment perfomance, Market Portfolio After Hedging, Amount",
    "Detailed investment perfomance, Basic Portfolio - Treasury, Amount",
    "Structure of the strategic allocation, Foreign Currency Bonds",
    "Structure of the strategic allocation, Equities",
    "Structure of the strategic allocation, Bonds in CHF",
    "Structure of the strategic allocation, Real Estate",
    "Structure of the strategic allocation, Precious Metals",
]

# Mapping table categories to CSV column indices
PERFORMANCE_TABLE_MAPPING = {
    "Money market investments": 1,
    "Loans to public entities in Switzerland": 2,
    "Swiss francs bonds": 3,
    "Foreign currency bonds:": 4,
    "Government bonds": 5,
    "Inflation-protected bonds": 6,
    "Emerging market bonds": 7,
    "Corporate bonds": 8,
    "High yield bonds": 9,
    "Securitised bonds": 10,
    "Equities:": 11,
    "Large caps": 12,
    "Emerging markets": 13,
    "Small and mid caps": 14,
    "Real estate:": 15,
    "Switzerland direct": 16,
    "Switzerland listed": 17,
    "Global listed": 18,
    "Global not listed": 19,
    "Gold": 20,
    "Multi-Asset portfolio": 21,
    "Market portfolio": 22,
    "Hedging of currency risk": 23,
    "Market portfolio after hedging": 26,
    "Basic portfolio - Treasury": 27,
}

# Metadata template - common fields for all rows
METADATA_COMMON = {
    "FREQUENCY": "A",
    "AGGREGATION_TYPE": "UNDEFINED",
    "SEASONALLY_ADJUSTED": "NSA",
    "ANNUALIZED": False,
    "STATE": "ACTIVE",
    "PROVIDER": "AfricaAI",
    "SOURCE": "COMPENSWISS",
    "SOURCE_DESCRIPTION": "Compenswiss - Fonds de compensation AVS",
    "COUNTRY": "CHE",
    "DATASET": "CHEF"
}

# Metadata for performance data (columns 1-27)
METADATA_PERFORMANCE = {
    "MULTIPLIER": 6,
    "UNIT_TYPE": "FLOW",
    "DATA_TYPE": "CURRENCY",
    "DATA_UNIT": "CHF",
    "PROVIDER_MEASURE_URL": f"{BASE_URL}/en_GB/investments"
}

# Metadata for strategic allocation data (columns 28-32)
METADATA_STRATEGIC = {
    "MULTIPLIER": 0,
    "UNIT_TYPE": "LEVEL",
    "DATA_TYPE": "PERCENT",
    "DATA_UNIT": "PERCENT",
    "PROVIDER_MEASURE_URL": f"{BASE_URL}/en_GB/investments/strategic-asset-allocation-sva"
}


