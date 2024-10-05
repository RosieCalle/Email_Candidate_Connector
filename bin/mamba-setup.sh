#!/bin/bash
# This script sets up the Mamba environment for the project.
#
APP_PATH=$(dirname "$0")
enviro=$(basename "$PWD")

# Check if the environment exists
if ! mamba env list | grep -q "$enviro"; then
    echo "Creating a new mamba environment named $enviro..."
    # Create a new mamba environment named "$enviro"
    #   -- using the c-requierments.txt file if it exists
    #   -- otherwise, create initial environment
    if [ -f ../conf/c-requirements.txt ]; then
        mamba create --name $enviro --file ../conf/c-requirements.txt -y
    else
        mamba create --name $enviro -y
    fi
fi

echo " ------------------------------------- "
echo "mamba activate "$enviro
echo " temp: mamba install --file conf/c-requirements.txt -y "
echo " ------------------------------------- "
echo " if conf/p-requirements.txt exists"
echo "pip install -r conf/p-requirements.txt"
echo " ------------------------------------- "
