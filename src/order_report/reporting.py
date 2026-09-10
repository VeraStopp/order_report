import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)

def save_dataframe_to_csv(df: pd.DataFrame, output_path: Path) -> None:
    """Saves a single DataFrame to a CSV file at the specified output path"""
    try: 
        output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_path, index=False)
        logger.info("Successfully saved report to: %s", output_path)

    except Exception as error:
        logger.error("Failed to save report to %s. Error: %s", output_path, error)
        raise IOError(f"Could not save report file to {output_path}") from error

def save_all_reports(reports: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Iterates over a dictionary of report DataFrames and saves each to the output directory"""
    logger.info("Exporting all generated reports to directory: %s", output_dir)

    if not reports: 
        logger.warning("No reports provided for export")
        return

    for report_name, df in reports.items():
        file_path = output_dir / f"{report_name}.csv"
        save_dataframe_to_csv(df, file_path)

    logger.info("All reports saved successfully")
