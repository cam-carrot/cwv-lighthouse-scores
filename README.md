# cwv-lighthouse-scores

This project processes URLs to fetch Lighthouse scores using the Google PageSpeed Insights API.

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/my_project.git
    cd my_project
    ```

2. **Create a virtual environment and activate it:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Add your Google API key:**
    Update the `API_KEY` in `config.py` with your Google PageSpeed Insights API key.

5. **Place your input data:**
    Ensure that your `cwv.csv` file is in the `data` directory.

## URL Format Requirements

- All URLs in the `cwv.csv` file must be in the format `https://www.example.com`.
- Ensure that each URL starts with `https://` and includes `www.` to avoid any issues with API requests.

## Platform Column

- The `cwv.csv` file should include a `platform` column, which differentiates between "Carrot" and "Non-Carrot" sites.
- This data is directly gleaned from the script output at [carrot-serp-compare](https://github.com/jondcoleman/carrot-serp-compare). The `TRUE` and `FALSE` values from this script need to be turned into "Carrot" and "Non-Carrot" respectively.
- The reason for this differentiation is to provide mean CWV (Core Web Vitals) scores for Carrot vs Non-Carrot sites in the comparison file at the end of the processing.

## Running the Script

1. **Run the main script:**
    ```sh
    python main.py
    ```

## Output

- The processed Lighthouse scores will be saved in `data/lighthouse_scores.csv`.
- The comparison results will be saved in `data/comparison_results.csv`.
- Errors and logs will be saved in `logs/errors.log`.

## Parallel Processing

- The current setup uses parallel processing to speed up the fetching of Lighthouse scores.
- URLs are processed concurrently using Python's `concurrent.futures.ThreadPoolExecutor`, which significantly reduces the total processing time.
- By default, the script uses 10 threads to handle multiple requests in parallel. This can be adjusted by modifying the `max_workers` parameter in the `main.py` script.


