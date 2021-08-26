FROM python:3.9-buster

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

RUN pip3 install black flake8 mypy pytest

USER $USERNAME

RUN mkdir /home/$USERNAME/streamweb-logs

RUN pip3 install -r requirements.txt --user

ENV PATH="${PATH}:/home/${USERNAME}/.local/bin"