import logging
import pandas as pd

logger = logging.getLogger(__name__)

def calculate_order_value(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates total price and discounted price for each order record"""
    logger.info("Calculating total order values and applying discount")
    df = df.copy()

    df["total_price"] = df["quantity"] * df["unit_price"]
    df["discounted_price"] = df["total_price"] * (1 - df["discount"])