#!/bin/bash

# get enviroment name from the conda_config.yaml file
yaml_file_path="conf/conda_config.yaml"
# enviro=$(grep 'name:' "$yaml_file_path" | awk '{print $2}')
enviro="emailagent"

if [[ "$CONDA_DEFAULT_ENV" == "$enviro" ]]; then
    echo "The conda environment $enviro is already activated."
else
    echo "#### please change the conda enviroment to $enviro ####"
    echo ""
    echo "conda activate "$enviro
    echo ""
    exit 1
fi

echo "Logs cleaned up."
rm logs/*.log

echo "Starting the program..."
cd src
python main.py
