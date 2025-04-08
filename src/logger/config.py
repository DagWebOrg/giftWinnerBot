import logging


config = {
    "filename": "logger/logs/main.log",
    "level": logging.INFO,
    "format": "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s"
}
logging.basicConfig(**config)
LOGGER = logging.getLogger(__name__)
