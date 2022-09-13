"""Log configuration and initialization module."""
import sys
from datetime import datetime

from loguru import logger

from complex_epidemic_simulator import config
from complex_epidemic_simulator.config.core import ROOT_DIR


def setup_logging() -> tuple:
    """Execute logging setup."""
    log_filename_prefix = config.app_config.package_name
    log_filename_suffix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"{log_filename_prefix}_{log_filename_suffix}"
    log_dir = ROOT_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file_path = log_dir / f"{log_filename}.log"

    log_file, log_console = logger.configure(
        handlers=[
            dict(
                sink=log_file_path,
                level="DEBUG",
                format="{time} | {level} | {name}:{module}:{function} - {message}",
                rotation="250 MB",
                backtrace=True,
                diagnose=True,
                enqueue=True,
            ),
            dict(
                sink=sys.stderr,
                level="INFO",
                format="{level} | {name}:{module}:{function} - {message}",
                backtrace=True,
                diagnose=True,
                enqueue=True,
            ),
        ]
    )
    return log_file, log_file_path, log_console


if __name__ == "__main__":
    print(setup_logging())
