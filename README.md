- change process_email for something like save_email_body
- change save_to_file for save_attachment 
- add the attachment the email_id
- make 2 folders in data 1-body 2-attachments

- add checking database connection before at main function
2










# Email_Candidate_Connector
Automated Email Agent to Help Recruiter and Candidate Connect. 

# TODO - more details

# TODO: how can to setup the enviroment 
- conda env create -f conda_config.yaml
- conda activate eamilagent

# TODO how to setup configuration

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
    "lin_data_folder": "/home/rafael/dev/projects/email-candidate/data/",
    "lin_token_path": "/home/rafael/dev/projects/token.pickle",
    "lin_credentials_path": "/home/rafael/dev/projects/client_secret_desktop-app.json",
    "lin_log_file": "/home/rafael/dev/projects/email-candidate/logs/app.log",
    "schema": "gmailemails"
}
- if there are more dockers, the db_host must be changed  to the docker host name
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

├── bin
│   ├── build-docker-images.sh
│   ├── mamba-setup.sh
│   ├── setup-conda.sh
│   ├── start-docker-postgres.sh
│   └── start.sh
├── conf
│   ├── conda_config.yaml
│   ├── config
│   ├── config.json
│   ├── c-requirements.txt
│   ├── p-requirements.txt
│   └── setup-conda.bat
├── data
│   ├── attach
│   └── body
├── docker-compose.yml
├── docs
│   ├── architecture.md
│   ├── calls_graph.dot
│   ├── calls_graph.drawio
│   ├── calls_graph.drawio.xml
│   ├── calls_graph.mermaid
│   ├── candiate_connect_conda_env_list.txt
│   ├── conda_create_command_for_candidate_connect_environment.md
│   ├── DB_text_diagram.md
│   ├── dot2drawio.py
│   ├── google-authentication.md
│   ├── notas.txt
│   └── postgresql_setup.md
├── LICENSE
├── linux-start.sh
├── logs
│   └── app.log
├── README.md
├── src
│   ├── db_functions.py
│   ├── files.py
│   ├── filter.py
│   ├── generate_mimetype_examples.py
│   ├── logger_config.py
│   ├── main.py
│   ├── parser_messages.py
│   ├── process_emails.py
│   └── send_emails.py
├── start.sh
├── TODO.md
├── utils
│   └── db_utils.py
└── windows-start.bat


We did use for filtering
https://www.nltk.org/install.html