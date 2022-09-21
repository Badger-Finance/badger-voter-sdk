import logging
import traceback

from pythonjsonlogger import jsonlogger

logger = logging.getLogger()

log_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)


def exception_logging(exctype, value, tb) -> None:
    logger.error(f"{str(exctype)} Exception", extra={
        'exctype': str(exctype),
        'error': ''.join(traceback.format_exception(exctype, value, tb))
    })
