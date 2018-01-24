import logging

_formatter = logging.Formatter('%(message)s')
_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)
_logger = logging.getLogger('logger')
_logger.setLevel(logging.WARNING)
_logger.addHandler(_handler)


def set_verbose():
    _logger.setLevel(logging.INFO)


def log(msg):
    _logger.info(msg)


def error(msg):
    _logger.error(msg)
