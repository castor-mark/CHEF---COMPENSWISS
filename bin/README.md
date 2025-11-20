# Test Files and Development Tools

This directory contains test files and development tools used during the scraper development process.

## Test Files

### Strategic Allocation Extraction Tests

These files were used to develop and validate the hybrid extraction strategy for strategic allocation percentages:

- **test_hybrid_strategy.py** - Final validated hybrid extraction strategy test
  - Tests the production implementation across 4 text variation scenarios
  - Validates all 3 critical fixes: decimal percentages, 0% support, proximity checks
  - Achieves 100% accuracy on all test scenarios
  - Used to validate the strategy before production deployment

- **test_edge_cases.py** - Edge case validation tests
  - Tests decimal percentages (23.5%, 0.2%, etc.)
  - Tests zero percent (0%) acceptance
  - Tests proximity validation to prevent false positives
  - Confirms all AI model recommendations work correctly

- **test_strategic_extraction.py** - Multi-pattern fallback strategy test
  - Early development version testing multiple fallback patterns
  - Helped identify the need for sentence-based extraction

- **test_strategic_v2.py** - Proximity-based extraction test
  - Tests simple proximity matching without patterns
  - Led to the hybrid approach combining both strategies

### Metadata Tests

- **test_metadata.py** - Metadata generation validation
  - Ensures metadata structure matches AfricaAI runbook specification
  - Validates 32 rows with correct DATA_TYPE, UNIT_TYPE, etc.

### Legacy Development Files

- **parser.py** - Old HTML parsing utilities (replaced by scraper.py)
- **orchestrator.py** - Old orchestration logic (replaced by scraper.py)
- **compare_results.py** - Result comparison utilities
- **test_parsers.py** - Parser unit tests

## Production Files

The actual production scraper uses:
- **../scraper.py** - Main scraper with validated hybrid strategy
- **../config.py** - Configuration including STRATEGIC_ALLOCATION_CONFIG

## Running Tests

To run the validated tests:

```bash
# Test hybrid strategy (recommended)
python bin/test_hybrid_strategy.py

# Test edge cases
python bin/test_edge_cases.py
```

## AI Model Validation

The hybrid strategy was validated by 4 AI models via Zen MCP:
- qwen/qwen3-235b-a22b:free (confidence: 8/10)
- qwen/qwen-2.5-72b-instruct:free (confidence: 7/10)
- deepseek/deepseek-r1:free (confidence: 8/10)
- gemini-2.5-pro via clink (confidence: 9/10)

**Average confidence: 8/10**

All models unanimously recommended the hybrid approach with proximity checks.
