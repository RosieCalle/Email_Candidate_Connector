
import os
import os.path
import re
from bs4 import BeautifulSoup
from db_functions import save_to_attachment_table

from logger_config import setup_logger
logger = setup_logger('DEBUG',__name__)

def convert_html_to_text(html_data):
    """
    Converts HTML data to plain text, removing images and HTML formatting.  
    """
    soup = BeautifulSoup(html_data, 'html.parser')
    
    # Remove images
    for img in soup.find_all('img'):
        img.decompose()
    
    # Remove HTML formatting
    text = soup.get_text(separator=' ')

    # Remove extra spaces 
    text = re.sub(r'\s+', ' ', text)
    
    # Remove extra newlines
    text = re.sub(r'\n+', '\n', text)
    
    return text

def save_body_to_file(body_text, folder, file_name, msg_id): 
    """
    Saves text data to a file. 
    The body must be converter to text before saving to a file.
    """
    file_path = os.path.join(folder, file_name)  # data/file
    try:
        # Save text to a separate file
        file_name_text = msg_id + "_" + file_name + ".txt"
        text_file_path = os.path.join(folder, file_name_text)
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(body_text)
        logger.info(f"Text data saved to {text_file_path}")   
        return True   
    except Exception as e:
        print(f"Failed to save data to {file_path}: {e}")
        return False

def save_attachment_to_file(data, folder, filename, message_id, mimeType):
    """
    Saves the given data to a file in the specified folder.
    # message id is added to the filename to make it unique
    # filename is the epoch time in nanoseconds + message id + file extension
    # filetype is determined by the mimeType
    # filepath is the folder 
    """
    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Save the data to the file
        file = message_id + "_" + filename
        with open(os.path.join(folder, file), 'wb') as f:
            f.write(data)
        logger.info(f"Data saved to {folder}/{file}")

        # try:
        # save_to_attachment_table(message_id, folder, filename, mimeType)
        # except Exception as e:
        #     logger.error(f"Failed to save data to database: {str(e)}")      
        #    
    except Exception as e:
        logger.error(f"Failed to save data to {folder}/{file}: {str(e)}")

