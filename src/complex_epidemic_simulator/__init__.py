"""The Complex Epidemic Simulator project."""
import logging

from loguru import logger

from complex_epidemic_simulator.config.core import config
from complex_epidemic_simulator.config.log import setup_logging

try:
    from importlib.metadata import PackageNotFoundError, version  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

# Disable logging if package is used as a library.
logging.getLogger(config.app_config.package_name).addHandler(logging.NullHandler())

# # Update version from file.
# with open(PACKAGE_ROOT_DIR / "VERSION") as version_file:
#     __version__ = version_file.read().strip()

LOG_FILE, LOG_FILE_PATH, LOG_CONSOLE = setup_logging()
logger.info("Initializing package.")
logger.info(f"Log file created at: {LOG_FILE_PATH} .")
