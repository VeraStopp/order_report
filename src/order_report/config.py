
import logging
from pathlib import Path

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "customer_id",
    "region",
    "product_category",
    "quantity",
    "unit_price",
    "discount",
    "returned",
}

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_FILE_PATH = BASE_DIR / "data" / "orders.csv"
OUTPUT_DIR = BASE_DIR / "output"
LOG_FILE = BASE_DIR / "order_report.log"

LOGGER_NAME = "order_report"

def configure_logging() -> None:
    """Configures package specific logging for order_report"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    package_logger = logging.getLogger(LOGGER_NAME)

    if package_logger.handlers:
        return

    package_logger.setLevel(logging.DEBUG)
    package_logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    package_logger.addHandler(console_handler)
    package_logger.addHandler(file_handler)