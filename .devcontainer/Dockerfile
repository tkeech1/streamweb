FROM python:3.11.1-buster

ARG USERNAME=python
# On Linux, replace with your actual UID, GID if not the default 1000
ARG USER_UID=1000
ARG USER_GID=$USER_UID
# Docker GID on the host machine
ARG DOCKER_GID=999

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir -p /home/$USERNAME/.vscode-server /home/$USERNAME/.vscode-server-insiders \
    && chown ${USER_UID}:${USER_GID} /home/$USERNAME/.vscode-server*

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# get rid of pip warnings
RUN python3 -m pip install --upgrade pip 

RUN pip3 install black flake8 mypy pytest

USER $USERNAME

RUN mkdir /home/$USERNAME/streamweb-logs

ENV PATH="${PATH}:/home/${USERNAME}/.local/bin"

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt --user