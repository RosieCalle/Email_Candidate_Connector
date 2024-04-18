# Email_Candidate_Connector
Automated Email Agent to Help Recruiter and Candidate Connect. 

#TODO: how can I setup the enviroment and how I can run the app

- conda env create -f conda_config.yaml
- conda activate eamilagent

#TODO: explain how to setup the email authentication


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

# issues connecting with google account
Access blocked: This app’s request is invalid
rafael.testeador.68@gmail.com

---> enable api in the googlecloud project
https://console.cloud.google.com/flows/enableapi?apiid=gmail.googleapis.com

At the end it needs in the google app, make the publish step, even it is nothing on the app. 
In this way not only 'tester' can execute it.

