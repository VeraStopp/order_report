import logging
import pandas as pd

logger = logging.getLogger(__name__)

def calculate_order_values(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates total price and discounted price for each order record"""
    logger.info("Calculating total order values and applying discount")
    df = df.copy()

    df["total_price"] = df["quantity"] * df["unit_price"]
    df["discounted_price"] = df["total_price"] * (1 - df["discount"])

    return df

def summarize_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize sales performance and return statistics grouped by product category"""
    logger.info("Generating sales summary by product category")

    summary = (
        df.groupby("product_category")
        .agg(
            total_orders=("order_id", "count"),
            total_sales=("discounted_price", "sum"),
            returned_orders=("returned", "sum"),
        )
        .reset_index()
    )

    return summary

def summarize_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Summarizes sales performance and return statistics grouped by geographic region"""
    logger.info("Generating sales summary by region")

    summary = (
            df.groupby("region")
            .agg(
                total_orders=("order_id", "count"),
                total_sales=("discounted_price", "sum"),
                returned_orders=("returned", "sum"),
            )
            .reset_index()
    )

    return summary

def generate_kpi_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Computes high-level Key Performance Indicators (KPIs) across all orders"""
    logger.info("Computing overall KPI metrics")

    total_orders = len(df)
    total_revenue = df["discounted_price"].sum()
    returned_count = df["returned"].sum()
    return_rate = (returned_count / total_orders * 100) if total_orders > 0 else 0.0

    kpi_df = pd.DataFrame(
        [
            {
                "total_orders": total_orders,
                "total_revenue": round(total_revenue, 2),
                "returned_orders": returned_count,
                "returned_rate_pct": round(return_rate, 2)
            }
        ]
    )

    return kpi_df