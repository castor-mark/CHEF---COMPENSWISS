# -*- coding: utf-8 -*-
"""
Comprehensive LLM Provider Test Suite
Tests each provider individually and compares accuracy
"""

import sys
import os
import time
from dotenv import load_dotenv

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Load .env from parent directory
env_path = os.path.join(parent_dir, '.env')
load_dotenv(env_path)

from llm_fallback import LLMFallbackExtractor

# Test data
TEST_STRATEGIC_TEXT = """
Foreign currency bonds account for 37% of the allocations, making them the most important asset class.
Equities account for 28%. They offer attractive returns in the long term, but are subject to higher short-
term risks. Bonds and other fixed-income instruments denominated in CHF account for 17%, which is
lower than the other two asset classes due to their low return potential. Real estate, which accounts for
15% of the allocations, is particularly interesting in terms of long-term growth. To further diversify the
portfolio and protect against inflation, compenswiss also invests 3% in precious metals. Since 2019, this
asset class known as "commodities", has been limited to gold.
"""

TEST_PERFORMANCE_HTML = """
<table class="table--chart">
<tbody>
<tr><td>Money market investments</td><td>452</td></tr>
<tr><td>Loans to public entities in Switzerland</td><td>1,295</td></tr>
<tr><td>Swiss francs bonds</td><td>5,624</td></tr>
<tr><td>Foreign currency bonds:</td><td>15,829</td></tr>
<tr><td>Equities:</td><td>12,278</td></tr>
<tr><td>Real estate:</td><td>6,049</td></tr>
<tr><td>Gold</td><td>1,447</td></tr>
</tbody>
</table>
"""

EXPECTED_CATEGORIES = [
    "Money market investments",
    "Loans to public entities in Switzerland",
    "Swiss francs bonds",
    "Foreign currency bonds:",
    "Equities:",
    "Real estate:",
    "Gold"
]

EXPECTED_STRATEGIC = {
    "Foreign currency bonds": "37",
    "Equities": "28",
    "Bonds in CHF": "17",
    "Real estate": "15",
    "Precious metals": "3"
}

EXPECTED_PERFORMANCE = {
    "Money market investments": "452",
    "Loans to public entities in Switzerland": "1295",
    "Swiss francs bonds": "5624",
    "Foreign currency bonds:": "15829",
    "Equities:": "12278",
    "Real estate:": "6049",
    "Gold": "1447"
}


class ProviderTester:
    """Test individual LLM providers"""

    def __init__(self):
        self.extractor = LLMFallbackExtractor()
        self.results = {}

    def test_openrouter_models(self):
        """Test all OpenRouter models"""
        print("\n" + "="*80)
        print("  TESTING OPENROUTER MODELS")
        print("="*80)

        if not self.extractor.openrouter_api_key:
            print("[SKIP] No OpenRouter API key found")
            return {}

        models_to_test = [self.extractor.primary_model] + self.extractor.fallback_models
        results = {}

        for model in models_to_test:
            print(f"\n[TEST] Model: {model}")
            print("-"*80)

            # Test strategic allocation
            start_time = time.time()
            strategic_result = self._test_single_model_strategic(model, 'openrouter')
            strategic_time = time.time() - start_time

            # Test performance data
            start_time = time.time()
            performance_result = self._test_single_model_performance(model, 'openrouter')
            performance_time = time.time() - start_time

            results[model] = {
                'strategic': strategic_result,
                'performance': performance_result,
                'strategic_time': strategic_time,
                'performance_time': performance_time
            }

            # Summary
            strategic_score = f"{strategic_result['correct']}/{strategic_result['total']}"
            performance_score = f"{performance_result['correct']}/{performance_result['total']}"

            print(f"\n  Strategic: {strategic_score} ({strategic_time:.2f}s)")
            print(f"  Performance: {performance_score} ({performance_time:.2f}s)")

            if strategic_result['correct'] == 5 and performance_result['correct'] == 7:
                print(f"  [SUCCESS] 100% accuracy")
            else:
                print(f"  [WARNING] Incomplete extraction")

        return results

    def test_gemini(self):
        """Test Gemini models"""
        print("\n" + "="*80)
        print("  TESTING GEMINI MODELS")
        print("="*80)

        if not self.extractor.gemini_api_key:
            print("[SKIP] No Gemini API key found")
            return {}

        # Test multiple Gemini models
        gemini_models = [
            'gemini-2.0-flash-exp',
            'gemini-2.5-pro-exp-0827',
            'gemini-exp-1206'
        ]

        results = {}

        for model_name in gemini_models:
            print(f"\n[TEST] Model: {model_name}")
            print("-"*80)

            # Test strategic allocation
            start_time = time.time()
            strategic_result = self._test_single_model_strategic(model_name, 'gemini')
            strategic_time = time.time() - start_time

            # Test performance data
            start_time = time.time()
            performance_result = self._test_single_model_performance(model_name, 'gemini')
            performance_time = time.time() - start_time

            results[model_name] = {
                'strategic': strategic_result,
                'performance': performance_result,
                'strategic_time': strategic_time,
                'performance_time': performance_time
            }

            # Summary
            strategic_score = f"{strategic_result['correct']}/{strategic_result['total']}"
            performance_score = f"{performance_result['correct']}/{performance_result['total']}"

            print(f"\n  Strategic: {strategic_score} ({strategic_time:.2f}s)")
            print(f"  Performance: {performance_score} ({performance_time:.2f}s)")

            if strategic_result['correct'] == 5 and performance_result['correct'] == 7:
                print(f"  [SUCCESS] 100% accuracy")
            else:
                print(f"  [WARNING] Incomplete extraction")

        return results

    def test_groq_models(self):
        """Test all GroqCloud models"""
        print("\n" + "="*80)
        print("  TESTING GROQCLOUD MODELS")
        print("="*80)

        if not self.extractor.groq_api_key:
            print("[SKIP] No GroqCloud API key found")
            return {}

        results = {}

        for model in self.extractor.groq_models:
            print(f"\n[TEST] Model: {model}")
            print("-"*80)

            # Test strategic allocation
            start_time = time.time()
            strategic_result = self._test_single_model_strategic(model, 'groq')
            strategic_time = time.time() - start_time

            # Test performance data
            start_time = time.time()
            performance_result = self._test_single_model_performance(model, 'groq')
            performance_time = time.time() - start_time

            results[model] = {
                'strategic': strategic_result,
                'performance': performance_result,
                'strategic_time': strategic_time,
                'performance_time': performance_time
            }

            # Summary
            strategic_score = f"{strategic_result['correct']}/{strategic_result['total']}"
            performance_score = f"{performance_result['correct']}/{performance_result['total']}"

            print(f"\n  Strategic: {strategic_score} ({strategic_time:.2f}s)")
            print(f"  Performance: {performance_score} ({performance_time:.2f}s)")

            if strategic_result['correct'] == 5 and performance_result['correct'] == 7:
                print(f"  [SUCCESS] 100% accuracy")
            else:
                print(f"  [WARNING] Incomplete extraction")

        return results

    def _test_single_model_strategic(self, model, provider):
        """Test strategic allocation extraction for a single model"""
        prompt = self.extractor._create_strategic_prompt(TEST_STRATEGIC_TEXT)

        # Call appropriate provider
        if provider == 'openrouter':
            response = self.extractor._call_openrouter(prompt, model)
        elif provider == 'gemini':
            response = self._call_gemini_with_model(prompt, model)
        elif provider == 'groq':
            response = self.extractor._call_groq(prompt, model)
        else:
            return {'correct': 0, 'total': 5, 'errors': ['Unknown provider']}

        if not response:
            return {'correct': 0, 'total': 5, 'errors': ['No response from model']}

        # Parse response
        result = self.extractor._parse_strategic_response(response)

        # Check accuracy
        correct = 0
        errors = []

        for asset, expected_value in EXPECTED_STRATEGIC.items():
            actual_value = result.get(asset, "NOT FOUND")
            if actual_value == expected_value:
                correct += 1
                print(f"    [OK] {asset}: {actual_value}%")
            else:
                errors.append(f"{asset}: got {actual_value}, expected {expected_value}")
                print(f"    [FAIL] {asset}: {actual_value}% (expected {expected_value}%)")

        return {'correct': correct, 'total': 5, 'errors': errors}

    def _test_single_model_performance(self, model, provider):
        """Test performance data extraction for a single model"""
        prompt = self.extractor._create_performance_prompt(TEST_PERFORMANCE_HTML, EXPECTED_CATEGORIES)

        # Call appropriate provider
        if provider == 'openrouter':
            response = self.extractor._call_openrouter(prompt, model)
        elif provider == 'gemini':
            response = self._call_gemini_with_model(prompt, model)
        elif provider == 'groq':
            response = self.extractor._call_groq(prompt, model)
        else:
            return {'correct': 0, 'total': 7, 'errors': ['Unknown provider']}

        if not response:
            return {'correct': 0, 'total': 7, 'errors': ['No response from model']}

        # Parse response
        result = self.extractor._parse_performance_response(response, EXPECTED_CATEGORIES)

        # Check accuracy
        correct = 0
        errors = []

        for category, expected_value in EXPECTED_PERFORMANCE.items():
            actual_value = result.get(category, "NOT FOUND")
            if actual_value == expected_value:
                correct += 1
                print(f"    [OK] {category}: {actual_value}")
            else:
                errors.append(f"{category}: got {actual_value}, expected {expected_value}")
                print(f"    [FAIL] {category}: {actual_value} (expected {expected_value})")

        return {'correct': correct, 'total': 7, 'errors': errors}

    def _call_gemini_with_model(self, prompt, model_name):
        """Call Gemini API with specific model"""
        import requests

        try:
            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.extractor.gemini_api_key}',
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [{
                        'parts': [{'text': prompt}]
                    }],
                    'generationConfig': {
                        'temperature': 0.1,
                        'maxOutputTokens': 2000
                    }
                },
                timeout=30
            )

            if response.status_code == 200:
                content = response.json()['candidates'][0]['content']['parts'][0]['text']
                print(f"[LLM] Gemini {model_name} succeeded")
                return content
            else:
                print(f"[LLM] Gemini {model_name} error: {response.status_code}")
                if response.status_code == 400:
                    try:
                        error_detail = response.json()
                        print(f"[LLM] Error detail: {error_detail}")
                    except:
                        pass
                return None

        except Exception as e:
            print(f"[LLM] Gemini {model_name} exception: {str(e)}")
            return None

    def print_summary(self, openrouter_results, gemini_results, groq_results):
        """Print comprehensive summary"""
        print("\n\n" + "="*80)
        print("  COMPREHENSIVE TEST SUMMARY")
        print("="*80)

        all_results = []

        # OpenRouter
        if openrouter_results:
            print("\n[OPENROUTER MODELS]")
            for model, result in openrouter_results.items():
                strategic_pct = (result['strategic']['correct'] / 5) * 100
                performance_pct = (result['performance']['correct'] / 7) * 100
                overall_pct = (strategic_pct + performance_pct) / 2
                total_time = result['strategic_time'] + result['performance_time']

                print(f"  {model}")
                print(f"    Accuracy: {overall_pct:.1f}% (Strategic: {strategic_pct:.1f}%, Performance: {performance_pct:.1f}%)")
                print(f"    Speed: {total_time:.2f}s total")

                all_results.append({
                    'provider': 'OpenRouter',
                    'model': model,
                    'accuracy': overall_pct,
                    'speed': total_time
                })

        # Gemini
        if gemini_results:
            print("\n[GEMINI]")
            for model, result in gemini_results.items():
                strategic_pct = (result['strategic']['correct'] / 5) * 100
                performance_pct = (result['performance']['correct'] / 7) * 100
                overall_pct = (strategic_pct + performance_pct) / 2
                total_time = result['strategic_time'] + result['performance_time']

                print(f"  {model}")
                print(f"    Accuracy: {overall_pct:.1f}% (Strategic: {strategic_pct:.1f}%, Performance: {performance_pct:.1f}%)")
                print(f"    Speed: {total_time:.2f}s total")

                all_results.append({
                    'provider': 'Gemini',
                    'model': model,
                    'accuracy': overall_pct,
                    'speed': total_time
                })

        # GroqCloud
        if groq_results:
            print("\n[GROQCLOUD MODELS]")
            for model, result in groq_results.items():
                strategic_pct = (result['strategic']['correct'] / 5) * 100
                performance_pct = (result['performance']['correct'] / 7) * 100
                overall_pct = (strategic_pct + performance_pct) / 2
                total_time = result['strategic_time'] + result['performance_time']

                print(f"  {model}")
                print(f"    Accuracy: {overall_pct:.1f}% (Strategic: {strategic_pct:.1f}%, Performance: {performance_pct:.1f}%)")
                print(f"    Speed: {total_time:.2f}s total")

                all_results.append({
                    'provider': 'GroqCloud',
                    'model': model,
                    'accuracy': overall_pct,
                    'speed': total_time
                })

        # Ranking
        print("\n" + "="*80)
        print("  RANKING BY ACCURACY")
        print("="*80)

        sorted_by_accuracy = sorted(all_results, key=lambda x: x['accuracy'], reverse=True)
        for i, result in enumerate(sorted_by_accuracy, 1):
            print(f"{i}. [{result['provider']}] {result['model']}: {result['accuracy']:.1f}% ({result['speed']:.2f}s)")

        print("\n" + "="*80)
        print("  RANKING BY SPEED")
        print("="*80)

        sorted_by_speed = sorted(all_results, key=lambda x: x['speed'])
        for i, result in enumerate(sorted_by_speed, 1):
            print(f"{i}. [{result['provider']}] {result['model']}: {result['speed']:.2f}s ({result['accuracy']:.1f}%)")


if __name__ == "__main__":
    print("\n")
    print("*"*80)
    print("  COMPREHENSIVE LLM PROVIDER TEST SUITE")
    print("  Testing all providers: OpenRouter, Gemini 2.5 Pro, GroqCloud")
    print("*"*80)

    tester = ProviderTester()

    # Test all providers
    openrouter_results = tester.test_openrouter_models()
    gemini_results = tester.test_gemini()
    groq_results = tester.test_groq_models()

    # Print comprehensive summary
    tester.print_summary(openrouter_results, gemini_results, groq_results)

    print("\n" + "="*80)
    print("  RECOMMENDED FALLBACK ORDER (based on test results)")
    print("="*80)
    print("  Will be displayed above based on accuracy and speed rankings")
    print("="*80)
