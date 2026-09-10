from pathlib import Path
import pandas as pd
import pytest
from order_report.reporting import save_all_reports, save_dataframe_to_csv

@pytest.fixture
def sample_summary_df() -> pd.DataFrame:
    """Provides a small DataFrame fixture for file export testing"""
    return pd.DataFrame({"category": ["Electronics"], "total_sales": [150.0]})

def test_save_dataframe_to_csv(sample_summary_df: pd.DataFrame, tmp_path: Path) -> None:
    """Tests saving a single DataFrame to a CSV file in a temporary directory"""
    target_file = tmp_path / "test_report.csv"

    save_dataframe_to_csv(sample_summary_df, target_file)

    assert target_file.exists()
    loaded_df = pd.read_csv(target_file)
    assert len(loaded_df) == 1
    assert loaded_df.loc[0, "category"] == "Electronics"

def test_save_all_reports(sample_summary_df: pd.DataFrame, tmp_path: Path) -> None:
    """Tests exporting a dictionary of report DataFrames"""
    reports = {
        "category_summary": sample_summary_df,
        "region_summary": sample_summary_df,
    }
    output_dir = tmp_path / "outpus_reports"

    save_all_reports(reports, output_dir)

    assert output_dir.exists()
    assert (output_dir / "category_summary.csv").exists()
    assert (output_dir / "region_summary.csv").exists()

def test_save_dataframe_to_csv_io_error(sample_summary_df: pd.DataFrame, tmp_path: Path) -> None:
    """Tests that an invalid path properly raises an IOError"""
    invalid_path = tmp_path

    with pytest.raises(IOError):
        save_dataframe_to_csv(sample_summary_df, invalid_path)

