# api.py
import requests
from config import API_KEY, API_ENDPOINT
from logging_config import setup_logger

logger = setup_logger(__name__)

def get_lighthouse_scores(url, strategy='mobile'):
    params = {
        'url': url,
        'key': API_KEY,
        'strategy': strategy
    }
    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = requests.get(API_ENDPOINT, params=params)
            response.raise_for_status()
            result = response.json()
            lighthouse_result = result.get('lighthouseResult', {})
            performance_category = lighthouse_result.get('categories', {}).get('performance', {})
            performance_score = performance_category.get('score', 0) * 100 if performance_category.get('score') is not None else 0

            metrics = lighthouse_result.get('audits', {})
            cwv_metrics = {
                'performance_score': performance_score,
                'first_contentful_paint': metrics.get('first-contentful-paint', {}).get('numericValue', 0),
                'speed_index': metrics.get('speed-index', {}).get('numericValue', 0),
                'largest_contentful_paint': metrics.get('largest-contentful-paint', {}).get('numericValue', 0),
                'interactive': metrics.get('interactive', {}).get('numericValue', 0),
                'total_blocking_time': metrics.get('total-blocking-time', {}).get('numericValue', 0),
                'cumulative_layout_shift': metrics.get('cumulative-layout-shift', {}).get('numericValue', 0)
            }
            return cwv_metrics
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch data for {url} on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                return None  # Return None if all retries fail
