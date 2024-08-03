#!/bin/bash
#

#https://stackoverflow.com/questions/4332478/read-the-current-text-color-in-a-xterm/4332530#4332530
NORMAL=$(tput sgr0)
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)

# expected environment name
env_name=$(basename "$PWD")

# Get the name of the current conda environment
current_env=$(conda env list | grep '*' | awk '{print $1}')

# Check if the environments match
if [ "$env_name" != "$current_env" ]; then
    printf "\n *** ERROR ***\n"
    printf "\nThe current conda environment is not the expected environment."
    printf "\n\n%40s" "Activate the enviroment running: ${RED}conda activate $env_name ${NORMAL}"
    printf "\n\n%40s\n" "If you don't have the environment, create it by running: ${RED}source bin/setup.sh ${NORMAL}"
  exit 1
fi

# clean old logs
rm logs/*.log > /dev/null 2>&1

# # Start the main app
python src/main.py