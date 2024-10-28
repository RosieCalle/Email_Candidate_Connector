- change process_email for something like save_email_body
- change save_to_file for save_attachment 
- add the attachment the email_id
- make 2 folders in data 1-body 2-attachments

- add checking database connection before at main function
2










# Email_Candidate_Connector
Automated Email Agent to Help Recruiter and Candidate Connect. 

# Functionalities
1. Gmail Authentication:
    - Checks for existing credentials and refreshes them if necessary.
    - Initiates the OAuth2 flow to obtain new credentials if none are found.
    - Saves new credentials for future use.
    - Builds and returns a Gmail service object for API interactions.
2. Message Retrieval:
    - Retrieves messages from the user's mailbox matching a specified query.
    - Removes the 'UNREAD' label from downloaded messages.
    - Continues to fetch messages until a specified maximum number of messages is reached or there are no more messages to fetch.
3. Message Processing:
    - Processes each retrieved message using a specified function.
4. Storing:
    - Saves messages to a postgres database.

# How to setup the conda enviroment 
- conda env create -f conda_config.yaml
- conda activate eamilagent

# How to setup configuration
- configuation file: conf/config.json (for the application) and conf/config (for dockers)

- create a file: config.json at 'conf' folder
{
    "db_name": "emailcandidate",
    "db_user": "postgres",
    "db_password": "abc...",
    "db_host": "localhost",
    "db_port": "25432",
    "pg_user": "postgres",
    "pg_pass": "abc...",
    "win_data_folder": "..\\data\\",
    "win_token_path": "C:\\webservices\\gmail_credentials\\token.pickle",
    "win_credentials_path": "C:\\webservices\\gmail_credentials\\credentials.json",
    "win_log_file": "..\\app.log",
    "lin_data_folder": "_your_full_path_to_app_folder/email-candidate/data/",
    "lin_token_path": "_your_full_path_to_app_folder/key/token.pickle",
    "lin_credentials_path": "_your_full_path_to_app_folder/key/client_secret_desktop-app.json",
    "lin_log_file": "_your_full_path_to_app_folder/logs/app.log",
    "schema": "gmailemails"
}

- create a file: conf/config (for dockers)
```
    export POSTGRES_DB="emailcandidate"
    export POSTGRES_USER="postgres"
    export POSTGRES_PASSWORD="your_pass"
    export PGADMIN_DEFAULT_EMAIL="admin@example.com"
    export PGADMIN_DEFAULT_PASSWORD="admin_pass_"
    export POSTGRES_HOST="your_host"
    export POSTGRES_PORT="your_port"
```

- for docker the port should be different than 5432 in case that there is a postgres already running in local machine

# How to setup database with dockers
    - run bin/build-docker-images.sh
        - this script will build the docker images for postgres and pgadmin4.
    - go to 'add new server' and connect with postgres instance
         (pgvectordb1, is the hostname defined in docker-compose.yml)
            - use the user and password defined in config (or config.json)
    - run python utils/db_utils.py 
        - this script will create the database and tables
            the schema is gmailemils, and tables are 'attachments', 'emails', and 'bademails'


# TODO how to run the app
- In Linux: source start-linux.sh
- In Windows: 
...

# folder structure

# Project Structure

This project is organized into several directories and files, each serving a specific purpose:

- **bin/**: Contains shell scripts for various setup and startup tasks.
    - `build-docker-images.sh`: Script to build Docker images.
    - `mamba-setup.sh`: Script to set up Mamba.
    - `setup-conda.sh`: Script to set up Conda.
    - `start-docker-postgres.sh`: Script to start PostgreSQL in Docker.
    - `start.sh`: General startup script.

- **conf/**: Configuration files for the project.
    - `conda_config.yaml`: Conda configuration file.
    - `config`: General configuration file.
    - `config.json`: JSON configuration file.
    - `c-requirements.txt`: Conda requirements.
    - `p-requirements.txt`: Python requirements.
    - `setup-conda.bat`: Batch script to set up Conda on Windows.

- **data/**: Directory for data storage.
    - `attach/`: Directory for attachments.
    - `body/`: Directory for email bodies.

- **docs/**: Documentation files.
    - `architecture.md`: Architecture documentation.
    - `calls_graph.dot`: Graph of calls in DOT format.
    - `calls_graph.drawio`: Graph of calls in Draw.io format.
    - `calls_graph.drawio.xml`: XML file for Draw.io graph.
    - `calls_graph.mermaid`: Graph of calls in Mermaid format.
    - `candiate_connect_conda_env_list.txt`: List of Conda environments for candidate connect.
    - `conda_create_command_for_candidate_connect_environment.md`: Instructions to create Conda environment.
    - `DB_text_diagram.md`: Database text diagram.
    - `dot2drawio.py`: Script to convert DOT files to Draw.io format.
    - `google-authentication.md`: Documentation for Google authentication.
    - `notas.txt`: Miscellaneous notes.
    - `postgresql_setup.md`: PostgreSQL setup instructions.

- **logs/**: Directory for log files.
    - `app.log`: Application log file.

- **src/**: Source code for the project.
    - `db_functions.py`: Database functions.
    - `files.py`: File handling functions.
    - `filter.py`: Filtering functions.
    - `generate_mimetype_examples.py`: Script to generate MIME type examples.
    - `logger_config.py`: Logger configuration.
    - `main.py`: Main application script.
    - `parser_messages.py`: Message parsing functions.
    - `process_emails.py`: Email processing functions.
    - `send_emails.py`: Email sending functions.

- **utils/**: Utility scripts.
    - `db_utils.py`: Database utility functions.

- **docker-compose.yml**: Docker Compose configuration file.
- **LICENSE**: License file.
- **linux-start.sh**: Startup script for Linux.
- **README.md**: Project README file.
- **start.sh**: General startup script.
- **TODO.md**: To-do list.
- **windows-start.bat**: Startup script for Windows.