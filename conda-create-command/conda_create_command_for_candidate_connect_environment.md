# Conda create command for conda environment named "candidate_connect"

## Create a new environment

conda create --name candidate_connect -c conda-forge google-api-python-client google-auth-oauthlib google-auth python-dateutil jinja2 python-dateutil streamlit pandas matplotlib streamlit itables 

## Activate the environment
conda activate candidate_connect

## Install additional packages in the environment for generating diagrams
conda install -c conda-forge ipydrawio ipydrawio-export ipydrawio-mathjax ipydrawio-widgets jupyterlab-drawio 

