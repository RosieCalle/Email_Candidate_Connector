# Email_Candidate_Connector
Automated Email Agent to Help Recruiter and Candidate Connect. 
# TODO - more details

# TODO: how can to setup the enviroment 
- conda env create -f conda_config.yaml
- conda activate eamilagent

# TODO how to setup configuration

- create a file: config.json at 'conf' folder
- {
    "db_name": "emailcandidate",
    "db_user": "postgres",
    "db_password": "abc",
    "db_host": "localhost",
    "db_port": "5432",
    "pg_user": "postgres",
    "pg_pass": "abc",
    "win_data_folder": "..\\data\\",
    "win_token_path": "C:\\webservices\\gmail_credentials\\token.pickle",
    "win_credentials_path": "C:\\webservices\\gmail_credentials\\credentials.json",
    "win_log_file": "..\\app.log",
    "lin_data_folder": "/home/rafael/dev/projects/email-candidate-connector/data/",
    "lin_token_path": "/home/rafael/dev/projects/token.pickle",
    "lin_credentials_path": "/home/rafael/dev/projects/client_secret_desktop-app.json",
    "lin_log_file": "/home/rafael/dev/projects/email-candidate-connector/logs/app.log"
} 



# TODO how to run the app
...

# folder structure

├── conf
│   └── config.json
│   └── conda_config.yaml
├── data
├── docs
│   └── TODO.md
├── LICENSE
├── logs
│   └── app.log
├── README.md
├── src
│   ├── db_create.py
│   ├── db_functions.py
│   └── recruiter_email_connector.py
│   └── setup-conda.bat
├── start-windows.bat
├── start-linux.sh



We did use for filtering
https://www.nltk.org/install.html