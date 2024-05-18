#!/bin/bash -x


# get enviroment name from the conda_config.yaml file
yaml_file_path="conf/conda_config.yaml"
# enviro=$(grep 'name:' "$yaml_file_path" | awk '{print $2}')
enviro="emailagent"

if [[ "$CONDA_DEFAULT_ENV" == "$enviro" ]]; then
  echo "The conda environment $enviro is already activated."
else
  echo "Activating the conda environment $enviro..."
#   conda activate $enviro
    # conda activate emailagent
    source activate emailagent
fi

echo "Logs cleaned up."
rm logs\*.log

echo "Starting the program..."
cd src
python main.py
