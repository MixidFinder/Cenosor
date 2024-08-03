import logging
import os


def setup_logger(log_file_name, log_dir="log"):
    log_file_path = os.path.join(log_dir, log_file_name)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()],
    )
    return logging.getLogger(__name__)
