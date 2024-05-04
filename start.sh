#!/bin/bash

echo "Logs cleaned up."
rm logs\*.log

echo "Starting the program..."
cd src
python recruiter_email_connector.py
cd ..