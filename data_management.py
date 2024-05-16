# data_management.py
import pandas as pd
from logging_config import setup_logger

logger = setup_logger(__name__)

def read_data(filepath):
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        logger.error(f"Failed to read {filepath}: {e}")
        return pd.DataFrame()

def write_data(data, filepath):
    try:
        data.to_csv(filepath, index=False)
    except Exception as e:
        logger.error(f"Failed to write {filepath}: {e}")

def perform_analysis(results_df, output_file_path_comparison):
    carrot_sites = results_df[results_df['platform'] == 'Carrot']
    non_carrot_sites = results_df[results_df['platform'] == 'Non-Carrot']
    
    metrics = ['performance_score', 'first_contentful_paint', 'speed_index', 'largest_contentful_paint', 'interactive', 'total_blocking_time', 'cumulative_layout_shift']
    
    comparison = {
        'metric': metrics,
        'carrot_mean': [carrot_sites[metric].mean() for metric in metrics],
        'non_carrot_mean': [non_carrot_sites[metric].mean() for metric in metrics]
    }
    
    comparison_df = pd.DataFrame(comparison)
    write_data(comparison_df, output_file_path_comparison)

