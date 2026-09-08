from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def load_df(path: Path) -> pd.DataFrame:
    """Reads a CSV file into a pandas DataFrame with error handling and logging"""
    logger.info("Attempting to load data from: %s", path)

    try:
        df = pd.read_csv(path)
        logger.info("Successfully loaded DataFrame with %d rows and %d columns", len(df), len(df.columns))
        return df

    except FileNotFoundError as error:
        logger.error("File not found at path: %s", path)
        raise FileNotFoundError(f"Could not find the data file: {path}") from error

    except pd.errors.EmptyDataError as error:
        logger.error("File at path %s is empty", path)
        raise ValueError(f"the file is empty: {path}") from error

    except Exception as error:
        logger.error("Unexpected error occured while reading %s: %s", path, error)
        raise