# Create and configure logging
import logging

def setup_log_file():
    """
    Checks if the logs folder and log file exist. If they don't, it creates them.
    """
    # Define the path to the logs folder
    logs_folder_path = os.path.join(os.getcwd(), '../logs')
    # Define the path to the log file
    log_file_path = os.path.join(logs_folder_path, 'app.log')

    # Check if the logs folder exists, if not, create it
    if not os.path.exists(logs_folder_path):
        os.makedirs(logs_folder_path)

    # Check if the log file exists, if not, create it
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as log_file:
            log_file.write("Log file created.\n")

    return log_file_path

# Configure logging using the paths provided by setup_log_file() function.
def configure_logging(log_file_path):
    global logger
    # print(f"global logger object added in the first line of configure_loggin() function.")
    logging.basicConfig(filename=log_file_path, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Create a logger
    logger = logging.getLogger('email_candidate_connector')
    logger.setLevel(logging.INFO)

    # Create a file handler
    handler = logging.FileHandler(log_file_path)
    handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger

# global logger
# print(f"global logger object added.")
