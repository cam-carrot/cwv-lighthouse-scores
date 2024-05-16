# main.py
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures  # Ensure concurrent is imported
from api import get_lighthouse_scores
from data_management import read_data, write_data, perform_analysis
from config import INPUT_FILE_PATH, OUTPUT_FILE_PATH_SCORES, OUTPUT_FILE_PATH_COMPARISON
from logging_config import setup_logger
import pandas as pd

logger = setup_logger(__name__)

def process_url(row, index, total_urls):
    url = row['url']
    platform = row['platform']
    logger.info(f"Processing URL {index+1}/{total_urls}: {url}")
    scores = get_lighthouse_scores(url)
    if scores:
        scores['url'] = url
        scores['platform'] = platform
    else:
        logger.error(f"Failed to fetch data for {url}")
        scores = {'url': url, 'platform': platform, 'performance_score': 0}  # Handling failed request with default values
    return scores

def main():
    df = read_data(INPUT_FILE_PATH)
    total_urls = len(df)
    results = []
    try:
        with ThreadPoolExecutor(max_workers=25) as executor:
            future_to_url = {executor.submit(process_url, row, index, total_urls): row for index, row in df.iterrows()}
            for future in concurrent.futures.as_completed(future_to_url):
                results.append(future.result())
    except KeyboardInterrupt:
        logger.info("Process interrupted. Shutting down gracefully.")
        executor.shutdown(wait=False)
        raise

    results_df = pd.DataFrame(results)

    # Explicitly convert numeric columns to float and round to 3 decimal places
    numeric_columns = ['performance_score', 'first_contentful_paint', 'speed_index', 'largest_contentful_paint', 'interactive', 'total_blocking_time', 'cumulative_layout_shift']
    for col in numeric_columns:
        results_df[col] = pd.to_numeric(results_df[col], errors='coerce').round(3)

    write_data(results_df, OUTPUT_FILE_PATH_SCORES)
    perform_analysis(results_df, OUTPUT_FILE_PATH_COMPARISON)

    logger.info("Processing completed. Results saved.")

if __name__ == "__main__":
    main()
