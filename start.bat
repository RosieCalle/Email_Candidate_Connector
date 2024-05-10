@echo off

:: Check if the current environment is 'candidate_connect'
for /f "delims=" %%i in ('conda info --envs ^| findstr /R /C:"candidate_connect"') do set "ENV_ACTIVE=%%i"

:: If 'candidate_connect' is not active, activate it
if not "%ENV_ACTIVE%"=="candidate_connect" (
    echo Activating 'candidate_connect' environment...
    call conda activate candidate_connect
) else (
    echo 'candidate_connect' environment is already active.
)

echo Logs cleaned up.
del /Q /F logs\*.log

echo Starting the program...
cd src
python retrieve_emails.py
cd ..
