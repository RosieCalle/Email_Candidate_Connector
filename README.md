# Email_Candidate_Connector
Automated Email Agent to Help Recruiter and Candidate Connect. 

#TODO: how can I setup the enviroment and how I can run the app

- conda env create -f conda_config.yaml
- conda activate eamilagent

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

# Add configuration file

- create a file: config.json at conf folder
- {
    "db_name": "emailcandidate",
    "db_user": "postgres",
    "db_password": "xxx",
    "db_host": "localhost",
    "db_port": "5432",
    "pg_user": "postgres",
    "pg_pass": "xxx"
}


# TODO: explain how to setup the email authentication
# TODO move to a doc inside docs folder, and improve explanation with some samples
# To get the credentials for your application from Google, you need to create a project in the Google Cloud Console and then generate the credentials. Here are the steps:

https://developers.google.com/gmail/api/quickstart/python

Go to the Google Cloud Console: https://console.cloud.google.com/
Create a new project or select an existing one.
Once you're in your project, go to the navigation menu (three horizontal lines in the top left corner), and navigate to "APIs & Services" > "Credentials".
Click on "Create Credentials" and select "OAuth client ID".
If you haven't configured the OAuth consent screen yet, you'll be prompted to do so. Fill in the necessary information.
Once the OAuth consent screen is set up, you'll be able to create credentials. For the application type, select "Web application".
Enter a name for the credentials.
Under "Authorized JavaScript origins", add your application's origin (the URL where your app is hosted). For local testing, this can be http://localhost.
Under "Authorized redirect URIs", add the URI where you want the user to be redirected after they have authenticated with Google. For local testing, this can be http://localhost.
Click "Create". Your client ID and client secret will be generated.
After you've created your credentials, you can download them as a JSON file. This file will have the same structure as the one in your question. Be sure to keep this file secure and do not expose it publicly, as it contains sensitive information about your application.

---issues connecting with google account
Access blocked: This app’s request is invalid
your-email@gmail.com

--- enable api in the googlecloud project
https://cloud.google.com/apis/docs/getting-started?&_gl=1*4i3leb*_ga*ODQzMTE2MjE4LjE3MTA1MjgzMzA.*_ga_WH2QY8WWF5*MTcxNDA4MDMzNi43LjEuMTcxNDA4ODUzMC4wLjAuMA..&_ga=2.53326113.-843116218.1710528330#enabling_apis


