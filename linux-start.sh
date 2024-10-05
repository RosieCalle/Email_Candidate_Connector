#!/bin/bash

# expected environment name
env_name=$(basename "$PWD")

# mamba env create --name $env_name --file conf/conda_config.yaml -y

# Get the name of the current conda environment
current_env=$(micromamba env list | grep '*' | awk '{print $1}')

if [ "$current_env" != "$env_name" ]; then
    echo "Activating conda environment: $env_name"
    micromamba activate $env_name
fi

# clean old logs
rm logs/*.log > /dev/null 2>&1

# # Start the main app
python src/main.py