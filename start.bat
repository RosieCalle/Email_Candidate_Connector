@echo off

echo Logs cleaned up.
del /Q /F logs\*

echo Starting the program...
cd src
python recruiter_email_connector.py
