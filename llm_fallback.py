# -*- coding: utf-8 -*-
"""
LLM Fallback Module for Table Data Extraction
Uses GroqCloud, OpenRouter, and Gemini APIs as fallback when table parsing fails
"""

import os
import re
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMFallbackExtractor:
    """
    LLM-based fallback extractor for performance and strategic allocation data

    Uses multiple API providers with automatic fallback:
    1. GroqCloud (free, fast models)
    2. OpenRouter (free models available)
    3. Gemini (free tier available)
    """

    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_CLOUD_API_KEY')
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.enabled = os.getenv('ENABLE_LLM_FALLBACK', 'true').lower() == 'true'

        # Provider priority configuration
        priority_str = os.getenv('LLM_PROVIDER_PRIORITY', 'groq,openrouter,gemini')
        self.provider_priority = [p.strip().lower() for p in priority_str.split(',')]

        # Validate provider names
        valid_providers = {'groq', 'openrouter', 'gemini'}
        self.provider_priority = [p for p in self.provider_priority if p in valid_providers]

        # If no valid providers, use default order
        if not self.provider_priority:
            self.provider_priority = ['groq', 'openrouter', 'gemini']

        # Model configuration
        self.primary_model = os.getenv('LLM_MODEL', 'qwen/qwen-2.5-coder-32b-instruct:free')
        self.fallback_models = [
            os.getenv('LLM_MODEL_FALLBACK_1', 'qwen/qwen-2.5-72b-instruct:free'),
            os.getenv('LLM_MODEL_FALLBACK_2', 'deepseek/deepseek-r1:free'),
            os.getenv('LLM_MODEL_FALLBACK_3', 'meta-llama/llama-3.3-70b-instruct:free'),
            os.getenv('LLM_MODEL_FALLBACK_4', 'qwen/qwen3-coder:free'),
        ]

        # GroqCloud models (fast, free) - only use working model based on test results
        self.groq_models = [
            'llama-3.3-70b-versatile',  # Only this one works, others return 400 errors
        ]

    def extract_performance_data(self, html_text, expected_categories):
        """
        Extract performance data from HTML using LLM

        Args:
            html_text: HTML content containing the table
            expected_categories: List of category names to extract

        Returns:
            dict: {category_name: amount_value}
        """
        if not self.enabled:
            print("[LLM] Fallback disabled in .env")
            return {}

        print(f"\n[LLM] Attempting extraction with LLM fallback (priority: {' -> '.join(self.provider_priority)})...")

        prompt = self._create_performance_prompt(html_text, expected_categories)

        # Try providers in configured priority order
        result = None

        for provider in self.provider_priority:
            if result:
                break

            if provider == 'groq' and self.groq_api_key:
                for model in self.groq_models:
                    print(f"[LLM] Trying GroqCloud: {model}")
                    result = self._call_groq(prompt, model)
                    if result:
                        break

            elif provider == 'openrouter' and self.openrouter_api_key:
                models_to_try = [self.primary_model] + self.fallback_models
                for model in models_to_try:
                    print(f"[LLM] Trying OpenRouter: {model}")
                    result = self._call_openrouter(prompt, model)
                    if result:
                        break

            elif provider == 'gemini' and self.gemini_api_key:
                print("[LLM] Trying Gemini API")
                result = self._call_gemini(prompt)

        if result:
            return self._parse_performance_response(result, expected_categories)

        print("[LLM] All fallback attempts failed")
        return {}

    def extract_strategic_allocation(self, text):
        """
        Extract strategic allocation percentages from text using LLM

        Args:
            text: Text content containing strategic allocation info

        Returns:
            dict: {asset_name: percentage}
        """
        if not self.enabled:
            print("[LLM] Fallback disabled in .env")
            return {}

        print(f"\n[LLM] Extracting strategic allocation with LLM fallback (priority: {' -> '.join(self.provider_priority)})...")

        prompt = self._create_strategic_prompt(text)

        # Try providers in configured priority order
        result = None

        for provider in self.provider_priority:
            if result:
                break

            if provider == 'groq' and self.groq_api_key:
                for model in self.groq_models:
                    print(f"[LLM] Trying GroqCloud: {model}")
                    result = self._call_groq(prompt, model)
                    if result:
                        break

            elif provider == 'openrouter' and self.openrouter_api_key:
                models_to_try = [self.primary_model] + self.fallback_models
                for model in models_to_try:
                    print(f"[LLM] Trying OpenRouter: {model}")
                    result = self._call_openrouter(prompt, model)
                    if result:
                        break

            elif provider == 'gemini' and self.gemini_api_key:
                print("[LLM] Trying Gemini API")
                result = self._call_gemini(prompt)

        if result:
            return self._parse_strategic_response(result)

        print("[LLM] All fallback attempts failed")
        return {}

    def _create_performance_prompt(self, html_text, expected_categories):
        """Create prompt for performance data extraction"""
        categories_list = "\n".join([f"- {cat}" for cat in expected_categories])

        return f"""You are a data extraction expert. Extract investment performance data from the HTML table below.

EXPECTED CATEGORIES:
{categories_list}

INSTRUCTIONS:
1. Find each category in the table
2. Extract the corresponding amount (in CHF millions)
3. Return ONLY a JSON object with category names as keys and amounts as values
4. If a category is not found, omit it from the JSON
5. Remove all formatting (commas, spaces) from numbers
6. Handle negative numbers correctly (e.g., -582)

HTML CONTENT:
{html_text[:5000]}

Return format:
{{
  "Money market investments": "452",
  "Foreign currency bonds:": "15829",
  ...
}}

JSON OUTPUT:"""

    def _create_strategic_prompt(self, text):
        """Create prompt for strategic allocation extraction"""
        return f"""You are a data extraction expert. Extract strategic allocation percentages from the text below.

EXPECTED ASSETS:
- Foreign currency bonds
- Equities
- Bonds in CHF
- Real estate
- Precious metals

INSTRUCTIONS:
1. Find percentage allocations for each asset class
2. Return ONLY a JSON object with asset names as keys and percentages as values
3. Include ONLY the numeric value (e.g., "43" not "43%")
4. Support decimal percentages (e.g., "23.5")
5. If an asset is not mentioned, omit it from the JSON

TEXT CONTENT:
{text}

Return format:
{{
  "Foreign currency bonds": "37",
  "Equities": "28",
  "Bonds in CHF": "17",
  "Real estate": "15",
  "Precious metals": "3"
}}

JSON OUTPUT:"""

    def _call_groq(self, prompt, model):
        """Call GroqCloud API"""
        try:
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.groq_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': model,
                    'messages': [
                        {'role': 'system', 'content': 'You are a precise data extraction assistant. Always return valid JSON.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.1,
                    'max_tokens': 2000
                },
                timeout=30
            )

            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                print(f"[LLM] GroqCloud {model} succeeded")
                return content
            else:
                print(f"[LLM] GroqCloud {model} error: {response.status_code}")
                return None

        except Exception as e:
            print(f"[LLM] GroqCloud {model} exception: {str(e)}")
            return None

    def _call_openrouter(self, prompt, model):
        """Call OpenRouter API"""
        try:
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.openrouter_api_key}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'https://github.com/compenswiss-scraper',
                    'X-Title': 'COMPENSWISS Data Scraper'
                },
                json={
                    'model': model,
                    'messages': [
                        {'role': 'system', 'content': 'You are a precise data extraction assistant. Always return valid JSON.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.1,
                    'max_tokens': 2000
                },
                timeout=30
            )

            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                print(f"[LLM] OpenRouter {model} succeeded")
                return content
            else:
                print(f"[LLM] OpenRouter {model} error: {response.status_code}")
                return None

        except Exception as e:
            print(f"[LLM] OpenRouter {model} exception: {str(e)}")
            return None

    def _call_gemini(self, prompt):
        """Call Gemini API"""
        try:
            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={self.gemini_api_key}',
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
                print("[LLM] Gemini succeeded")
                return content
            else:
                print(f"[LLM] Gemini error: {response.status_code}")
                return None

        except Exception as e:
            print(f"[LLM] Gemini exception: {str(e)}")
            return None

    def _parse_performance_response(self, response, expected_categories):
        """Parse LLM response for performance data"""
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
            if not json_match:
                print("[LLM] No JSON found in response")
                return {}

            data = json.loads(json_match.group())

            # Validate and clean
            cleaned_data = {}
            for category in expected_categories:
                if category in data:
                    # Clean the value
                    value = str(data[category]).replace(',', '').replace(' ', '').strip()
                    cleaned_data[category] = value

            print(f"[LLM] Successfully extracted {len(cleaned_data)} categories")
            return cleaned_data

        except Exception as e:
            print(f"[LLM] Parse error: {str(e)}")
            return {}

    def _parse_strategic_response(self, response):
        """Parse LLM response for strategic allocation"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
            if not json_match:
                print("[LLM] No JSON found in response")
                return {}

            data = json.loads(json_match.group())

            # Validate percentages are in reasonable range (0-50%)
            cleaned_data = {}
            for asset, percentage in data.items():
                try:
                    pct_value = float(percentage)
                    if 0 <= pct_value <= 50:
                        cleaned_data[asset] = str(percentage)
                    else:
                        print(f"[LLM] Invalid percentage for {asset}: {percentage}%")
                except:
                    print(f"[LLM] Could not parse percentage for {asset}: {percentage}")

            print(f"[LLM] Successfully extracted {len(cleaned_data)} allocations")
            return cleaned_data

        except Exception as e:
            print(f"[LLM] Parse error: {str(e)}")
            return {}
