# Python core
FROM python:3.9-bullseye

# Arguments as mentioned in the task bonus
## ENV NOTEBOOKS_FROM=/notebook
ENV HUB_PATH=/hub

# just a work dir
WORKDIR ${HUB_PATH}

# Installing useful things
RUN apt install curl
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -

# Installing nodejs so its requred for jupyter
RUN apt-get install nodejs-legacy
 
# Also some requirements
RUN npm install -g configurable-http-proxy

# The jupyter
RUN pip install jupyterhub
RUN pip install --upgrade notebook

# Better sign in
RUN pip install jupyterhub-nativeauthenticator

# Exposing port as required in the task
EXPOSE 8000

# Mentioning volume as required in the task
VOLUME /home

# Config
COPY jupyterhub_config.py jupyterhub_config.py

# Starting the Jupyter!
CMD jupyterhub
