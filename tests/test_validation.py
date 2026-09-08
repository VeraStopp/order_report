import pytest
import pandas as pd

from order_report.validation import validate_columns, clean_data

def test_validate_columns_success():
    """Tests that no errors are raised when all required columns are present"""
    data = {
        "order_id": [1],
        "order_date": ["2026-01-01"],
        "customer_id": [101],
        "region": ["North"],
        "product_category": ["Electronics"],
        "quantity": [2],
        "unit_price": [100.0],
        "discount": [0.1],
        "returned": ["false"]
    }

    df = pd.DataFrame(data)

    validate_columns(df)

def test_validate_columns_missing_column_raise_error():
    """Tests that ValueError is raised if a required column is missing"""
    df = pd.DataFrame({
        "order_id": [1],
        "customer_id": [101]
    })

    with pytest.raises(ValueError, match="Missing columns"):
        validate_columns(df)

def test_clean_data_text_formatting():
    """Tests that text columns are trimmed of whitespace and converted to title case"""
    df = pd.DataFrame({
        "region": ["  europe ", None],
        "product_category": ["home appliances", "BOOKS"]
    })

    result = clean_data(df)

    assert result["region"].tolist() == ["Europe", "Unknown"]
    assert result["product_category"].tolist() == ["Home Appliances", "Books"]

def test_clean_data_numeric_imputation():
    """Tests that invalid or missing numbers are replaced with the specified value"""
    df = pd.DataFrame({
        "quantity": ["fel_text", None],
        "unit_price": [100.0, None],
        "discount": ["invalid", 0.2]
    })

    result = clean_data(df)

    assert result["quantity"].tolist() == [1, 1]
    assert result["unit_price"].tolist() == [100.0, 100.0]
    assert result["discount"].tolist() == [0.0, 0.2]

def test_clean_data_date_parsing():
    """Test that invalid order dates ceonverts to datetime"""
    df = pd.DataFrame({
        "order_date": ["2026-01-15", "invalid_date"]
    })

    result = clean_data(df)

    assert pd.api.types.is_datetime64_any_dtype(result["order_date"])

@pytest.mark.parametrize(
        "input_val, expected",
        [
            ("Ja", True),
            ("ja", True),
            ("TRUE", True),
            ("true", True),
            ("1", True),
            ("yes", True),
            ("no", False),
            ("false", False),
            ("0", False),
            (None, False),
            ("felaktigt_värde", False),
        ],
)
def test_clean_data_boolean_conversion(input_val, expected):
    """Tests that various text variants of returns are correctly converted to booleans."""
    df = pd.DataFrame({"returned": [input_val]})

    result = clean_data(df)

    assert result["returned"].iloc[0] == expected