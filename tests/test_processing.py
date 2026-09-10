import pandas as pd
import pytest
from order_report.processing import (
    calculate_order_value,
    generate_kpi_summary,
    summarize_by_category,
    summarize_by_region
)

@pytest.fixture
def sample_orders_df() -> pd.DataFrame:
    """Provides a standardized DataFrame fixture for testing processing functions"""
    return pd.DataFrame(
        {
            "order_id": [101, 102, 103, 104],
            "region": ["North", "North", "South", "South"],
            "product_category": ["Electronics", "Clothing", "Electronics", "Clothing"],
            "quantity": [2, 1, 5, 3],
            "unit_price": [100.0, 50.0, 20.0, 10.0],
            "discount": [0.10, 0.00, 0.20, 0.00],
            "returned": [False, True, False, False], 
        }
    )

def test_calculate_order_values(sample_orders_df: pd.DataFrame) -> None:
    """Test correct calculation of total_price and discounted_price"""
    result = calculate_order_value(sample_orders_df)

    assert result.loc[0, "total_price"] == pytest.approx(200.0)
    assert result.loc[0, "discounted_price"] == pytest.approx(180.0)

    assert result.loc[2, "total_price"] == pytest.approx(100.0)
    assert result.loc[2, "discounted_price"] == pytest.approx(80.0)

def test_summarize_by_category(sample_orders_df: pd.DataFrame) -> None:
    """Tests category aggregation logic for order counts, sales, and returns"""
    processed_df = calculate_order_value(sample_orders_df)
    summary = summarize_by_category(processed_df)

    assert len(summary) == 2
    assert "product_category" in summary.columns

    electronics_row = summary[summary["product_category"] == "Electronics"].iloc[0]
    assert electronics_row["total_orders"] == 2
    assert electronics_row["total_sales"] == pytest.approx(260.0)
    assert electronics_row["returned_orders"] == 0

def test_summarize_by_region(sample_orders_df: pd.DataFrame) -> None:
    """Tests regional aggregation logic for order counts, sales, and returns"""
    processed_df = calculate_order_value(sample_orders_df)
    summary = summarize_by_region(processed_df)

    assert len(summary) == 2

    north_row = summary[summary["region"] == "North"].iloc[0]
    assert north_row["total_orders"] == 2
    assert north_row["total_sales"] == pytest.approx(230.0)
    assert north_row["returned_orders"] == 1

def test_generate_kpi_summary(sample_orders_df: pd.DataFrame) -> None:
    """Tests high-level KPI metric calculations including return rate percentage"""
    processed_df = calculate_order_value(sample_orders_df)
    kpis = generate_kpi_summary(processed_df)

    assert kpis.loc[0, "total_orders"] == 4
    assert kpis.loc[0, "total_revenue"] == pytest.approx(340.0)
    assert kpis.loc[0, "returned_orders"] == 1
    assert kpis.loc[0, "returned_rate_pct"] == pytest.approx(25.0)

def test_generate_kpi_summary_empty_df() -> None:
    """Tests KPI generation with an empty DataFrame to prevent division by zero errors"""
    empty_df = pd.DataFrame(columns=["discounted_price", "returned"])
    kpis = generate_kpi_summary(empty_df)

    assert kpis.loc[0, "total_orders"] == 0
    assert kpis.loc[0, "total_revenue"] == 0.0
    assert kpis.loc[0, "returned_rate_pct"] == 0