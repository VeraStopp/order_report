import logging
from pathlib import Path
import sys
from . import config, loading, validation, processing, reporting

logger = logging.getLogger("order_report")

def run_pipeline(input_path: Path, output_dir: Path) -> None:
    df = loading.load_df(input_path)
    validation.validate_columns(df)
    clean_df = validation.clean_data(df)

    processed_df = processing.calculate_order_values(clean_df)

    reports = {
        "summary_by_category": processing.summarize_by_category(processed_df),
        "summary_by_region": processing.summarize_by_region(processed_df),
        "kpi_overview": processing.generate_kpi_summary(processed_df)
    }

    reporting.save_all_reports(reports, output_dir)

def main() -> None:
    """Main entry point for the order report application"""
    config.configure_logging()
    logger.info("Starting order processing pipeline")

    try:
        run_pipeline(config.INPUT_FILE_PATH, config.OUTPUT_DIR)
        logger.info("Pipeline executed successfulley. All task completed")

    except FileNotFoundError as error:
        logger.error("Data file missing: %s", error)
        sys.exit(1)

    except ValueError as error:
        logger.error("Validation error: %s", error)
        sys.exit(1)

    except IOError as error:
        logger.error("Report output error: %s", error)
        sys.exit(1)

    except Exception as error:
        logger.critical("Unexpected system failure: %s", error, exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()