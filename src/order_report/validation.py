import pandas as pd
import logging
from order_report.config import REQUIRED_COLUMNS

logger = logging.getLogger(__name__)


def validate_columns(df: pd.DataFrame) -> None:
    """Ensures all required columns are present in the DataFrame"""
    logger.debug("Validating dataframe columns against required set")
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)

    if missing_columns:
        logger.error("Column validation failed. Midding columns: %s", missing_columns)
        raise ValueError(f"Missing columns in input data: {missing_columns}")

    logger.info("Column validation successful. All required columns present")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans and standardizes data types in the DataFrame"""
    logger.info("Starting data cleaning and standardization process")
    df = df.copy()

    for col in ["region", "product_category"]:
        if col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                logger.warning("Found %d missing values in '%s'. Imputing with 'Unknown'", missing_count, col)
            df[col] = df[col].fillna("Unknown").astype(str).str.strip().str.title()

    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
        nat_count = df["order_date"].isna().sum()
        if nat_count > 0:
            logger.warning("Found %d invalid or missing date values in 'order_date'", nat_count)

    if "quantity" in df.columns:    
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1)

    if "unit_price" in df.columns:    
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
        median_price = df["unit_price"].median()
        missing_prices = df["unit_price"].isna().sum()
        if missing_prices > 0:
            logger.warning("Imputing %d missing 'unit_price' values with median (%.2f)", missing_prices, median_price)
        df["unit_price"] = df["unit_price"].fillna(median_price)

    if "discount" in df.columns:
        df["discount"] = pd.to_numeric(df["discount"], errors="coerce").fillna(0)

    if "returned" in df.columns:
        df["returned"] = (
            df["returned"]
            .fillna("false")
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["true", "yes", "1", "ja"])
        )

    logger.info("Data cleaning completed successfully")
    return df
   