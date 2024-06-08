import logging

def setup_logger(name, log_level=logging.DEBUG, log_file=None):
    """
    Set up a logger with the specified name and log level.
    
    :param name: Name of the logger.
    :param log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    :param log_file: Optional path to a log file.
    :return: Logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)

    # If a log file is specified, also add a file handler
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


# from logger_config import setup_logger

# # Setup a logger with a custom name and log level
# logger = setup_logger('my_application', log_level=logging.INFO, log_file='../logs/application.log')

# # Log messages at different levels
# logger.debug('This is a debug message.')
# logger.info('This is an informational message.')
# logger.warning('This is a warning message.')
# logger.error('This is an error message.')
# logger.critical('This is a critical message.')