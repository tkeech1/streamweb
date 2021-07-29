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

RUN pip3 install --user streamlit==0.80.0 bokeh==2.2 feedgen==0.9.0 pandas==1.2.3 numpy==1.20.1 pyyaml==5.4.1 torch fastai bing_image_downloader --user

ENV PATH="${PATH}:/home/${USERNAME}/.local/bin"