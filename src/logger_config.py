import os 
import json
import logging


# def setup_logger(name, log_level=logging.DEBUG, log_file=None):
def setup_logger(name):

    """
    Set up a logger with the specified name and log level.
    
    :param name: Name of the logger.
    :param log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    :param log_file: Optional path to a log file.
    :return: Logger instance.
    """

    # get paramters from config file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    relative_config_path = os.path.join(script_dir, '..', 'conf', 'config.json')
    config_path = os.path.abspath(relative_config_path)
    with open(config_path, 'r') as file:
        config = json.load(file)

    # get log parameters
    if os.name == 'nt': # 'nt' stands for Windows
        LOG_FILE = config['win_log_file']
        LOG_LEVEL = config['log_level']
    elif os.name == 'posix': # 'posix' stands for Linux/Unix
        LOG_FILE = config['lin_log_file']
        LOG_LEVEL = config['log_level']
    else:
        raise OSError("Unsupported operating system")

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)

    # If a log file is specified, also add a file handler
    if LOG_FILE:
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(LOG_LEVEL)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

#### Log messages at different levels ####
# logger.debug('This is a debug message.')
# logger.info('This is an informational message.')
# logger.warning('This is a warning message.')
# logger.error('This is an error message.')
# logger.critical('This is a critical message.')

########### log LEVEL meaning ###########
# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# INFO: Confirmation that things are working as expected.
# WARNING: An indication that something unexpected happened, or there may 
# be some problem in the near future (e.g., ‘disk space low’). 
# The software is still working as expected.
# ERROR: Due to a more serious problem, the software has not 
# been able to perform some function.
# CRITICAL: A very serious error, indicating that the program
#  itself may be unable to continue running.
# When you set a logging level, all the events at this level
#  and above will be tracked. For example, if the level is 
# set to INFO, the logger will handle both INFO, WARNING, ERROR, 
# and CRITICAL messages.