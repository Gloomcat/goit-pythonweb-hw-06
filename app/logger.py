import logging

LOGGER = logging.getLogger("AppLogger")
LOGGER.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

LOGGER.addHandler(ch)
