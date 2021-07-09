import streamlit as st
import datetime
import pytz
from utils.metrics import log_runtime

short_title = "GPUs in VS Code Dev Containers"
long_title = "Using GPUs in VS Code Dev Containers"
key = 2
content_date = datetime.datetime(2021, 7, 5).astimezone(pytz.timezone("US/Eastern"))
output_dir = "./tmp/1/"


@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    location.write(content_date)

    location.markdown(
        "I recently started reading [Practical Deep Learning for Coders](https://course.fast.ai/) "
        "by Jeremy Howard and Sylvain Gugger. The book gives a great overview of deep learning and transfer learning "
        "based on fastai and PyTorch. If you're new to deep learning and want to understand the detailed workings of neural networks, "
        "it's definitely worth the time. "
    )

    location.markdown(
        "The authors caution against spending a lot of time setting up a local development environment with GPU support. Instead, they "
        "recommend using Google Colab or another option that provides an out-of-the-box, GPU-enabled Jupyter notebook environment. "
        "While I think this is good advice for those who want to focus on deep learning, I always learn a lot configuring "
        "the environment from scratch so I decided to create a local setup. "
    )

    location.markdown(
        "In this post, I'll cover how to set up a local GPU-enabled Jupyter notebook environment using a VS Code development container. "
        "I have a GPU (GEForce GTX 1050 Ti) on my "
        "laptop but never used it for ML so this was a good opportunity to give it a try. Luckily, it's surprisingly easy to do in "
        "Docker. In this example, I'm running Docker 20.10.2 on Ubuntu 20.04.2 LTS."
    )

    location.markdown(
        "I use VS Code and I do most of my development using the [Remote Development extension](https://code.visualstudio.com/docs/remote/remote-overview) "
        "and [Docker development containers](https://code.visualstudio.com/docs/remote/create-dev-container). Dev containers allow me "
        "to install (and document in code) every dependency while keeping my base system neat and tidy. Unfortunately, using a GPU inside a Docker "
        "container requires some minimal setup on the host system. "
    )

    location.markdown("### Configure the Host System")

    location.markdown(
        "To start off, install the nvidia-docker2 package and its dependencies on the host system. This is "
        "[NVIDIA's container toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html). "
        "It includes a container runtime library and utilities to configure container support for GPUs. "
        "You'll need to restart Docker after installing it."
    )

    location.code(
        """
    sudo apt-get update
    sudo apt-get install nvidia-docker2
    sudo systemctl restart docker
    """
    )

    location.markdown(
        "NVIDIA provides a set of Docker images with GPU support. The command below executes `nvidia-smi`, "
        "an NVIDIA utility that allows you to query and manage GPU device state, inside a Docker container. "
        "Note that I'm using the Ubuntu 20.04 image but there are other images available. "
    )

    location.code(
        """
    docker run --rm --gpus all nvidia/cuda:11.0-base-ubuntu20.04 nvidia-smi
    """
    )

    location.markdown(
        "The output of the `nvidia-smi` command should be similar to what's shown below. If your host system is configured properly, you should see the "
        "CUDA version in the upper right-hand corner as well as the GPU memory in the bottom middle cell. "
    )

    location.code(
        """
Status: Downloaded newer image for nvidia/cuda:11.0-base
Wed Jul  7 00:34:05 2021       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 460.80       Driver Version: 460.80       CUDA Version: 11.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  GeForce GTX 105...  Off  | 00000000:01:00.0  On |                  N/A |
| N/A   55C    P0    N/A /  N/A |    186MiB /  4040MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
+-----------------------------------------------------------------------------+
    """
    )

    location.markdown("### Create a VS Code Dev Container")

    location.markdown(
        "Now that the host system has the necessary dependencies, you'll need to create a VS Code dev container. First, create a Dockerfile in the .devcontainer folder "
        "at the root of your VS Code project. The Dockerfile shown below contains the typical setup for mapping the container "
        "user to a local user so that files created inside the container have the appropriate ownership and permissions "
        "on the host system. "
    )

    location.code(
        """
FROM nvidia/cuda:11.0-base-ubuntu20.04

ARG USERNAME=python
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt update && apt install sudo time docker.io gpustat python3 python3-pip -y && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && echo $USERNAME":"$USERNAME | chpasswd && adduser $USERNAME sudo \
    && mkdir -p /home/$USERNAME/.vscode-server /home/$USERNAME/.vscode-server-insiders \
    && chown ${USER_UID}:${USER_GID} /home/$USERNAME/.vscode-server*

RUN python3 -m pip install --upgrade pip

USER $USERNAME
ENV PATH="${PATH}:/home/${USERNAME}/.local/bin"

RUN pip3 install --user torch jupyterlab fastai ipywidgets
"""
    )

    location.markdown(
        "`gpustat` is utility for monitoring GPU status and can be useful for monitoring the GPU during model training. "
        "I also included jupyterlab, fastai and ipywidgets as part of the image. These packages allow you to run the code in the [Practical Deep Learning for Coders](https://course.fast.ai/) book "
        "(you may need other dependencies but this should be enough to get started)."
    )

    location.markdown(
        "Next, you'll need to create a .devcontainer.json file in the .devcontainer directory. This file tells VS Code how "
        "to run your dev container and allows you to configure Docker options for forwarding ports and other runtime settings. "
    )

    location.code(
        """
{
    "name": "python",
    "context": "..",
    "dockerFile": "Dockerfile",
    "runArgs": [
        "--gpus",
        "all",
        "--shm-size",
        "2G"
    ],
    "forwardPorts": [
        8888
    ],
    "appPort": [],
    "settings": {
        "terminal.integrated.profiles.linux": {
            "bash": {
                "path": "/bin/bash"
            }
        },
        "terminal.integrated.defaultProfile.linux": "bash"
    },
    "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
    ]
}
    """
    )

    location.markdown(
        "There are two items to note. First, the `--gpus all` option enables Docker to use all available GPUs "
        "on the host machine. Second, `--shm-size 2G` increases the shared memory size to 2GB. The default amount "
        "of shared memory may not be enough depending on your application. If you encounter errors similar to the "
        "those shown below, try increasing the `--shm-size`."
    )

    location.code(
        """ERROR: Unexpected bus error encountered in worker. This might be caused by insufficient shared memory (shm)."""
    )

    location.markdown("### Run and Test the Dev Container")

    location.markdown(
        "Launch the dev container through VS Code. If all is well, you'll end up at a bash prompt inside the container. "
        "Start Jupyter Lab with `jupyter-lab` command and you should see Jupyter Lab startup normally as shown below. "
    )

    location.code(
        """
python@83279f51bc5c:/workspaces/gpu_docker$ jupyter-lab
[I 2021-07-07 14:01:08.369 ServerApp] jupyterlab | extension was successfully linked.
[I 2021-07-07 14:01:08.403 LabApp] JupyterLab extension loaded from /home/python/.local/lib/python3.8/site-packages/jupyterlab
[I 2021-07-07 14:01:08.403 LabApp] JupyterLab application directory is /home/python/.local/share/jupyter/lab
[I 2021-07-07 14:01:08.406 ServerApp] jupyterlab | extension was successfully loaded.
[I 2021-07-07 14:01:08.407 ServerApp] Serving notebooks from local directory: /workspaces/gpu_docker
[I 2021-07-07 14:01:08.407 ServerApp] Jupyter Server 1.9.0 is running at:
[I 2021-07-07 14:01:08.407 ServerApp] http://localhost:8888/lab?token=TOKEN
[I 2021-07-07 14:01:08.407 ServerApp]  or http://127.0.0.1:8888/lab?token=TOKEN
[I 2021-07-07 14:01:08.407 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 2021-07-07 14:01:08.412 ServerApp] 
    
    To access the server, open this file in a browser:
        file:///home/python/.local/share/jupyter/runtime/jpserver-12565-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/lab?token=TOKEN
     or http://127.0.0.1:8888/lab?token=TOKEN

    """
    )

    location.markdown(
        "From here, you can browse to Jupyter Lab at the URL noted above. Create a new notebook file and execute the following in "
        "the first cell."
    )

    location.code(
        """
import torch
torch.cuda.is_available()
    """
    )

    location.markdown(
        "The cell output will display `True` if everything is working properly. You now have a local GPU-enabled "
        "Jupyter notebook environment."
    )

    location.markdown("### GPU Status")

    location.markdown(
        "As you're working on code that uses the GPU, it can helpful to monitor the GPU status. "
        "The `nvidia-smi` utility mentioned earlier allows you to see which processes are using the GPU. Running `nvidia-smi` "
        "on the **host** machine should allow you to see your Jupyter notebook process on the GPU."
    )

    location.code(
        """
Wed Jul  7 10:14:31 2021       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 460.80       Driver Version: 460.80       CUDA Version: 11.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  GeForce GTX 105...  Off  | 00000000:01:00.0  On |                  N/A |
| N/A   54C    P3    N/A /  N/A |   1585MiB /  4040MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A   1340913      G   /usr/lib/xorg/Xorg                249MiB |
|    0   N/A  N/A   1341673      G   xfwm4                               1MiB |
|    0   N/A  N/A   1716644      C   /usr/bin/python3                 1329MiB |
+-----------------------------------------------------------------------------+
    """
    )

    location.markdown(
        "In the above output, PID 1716644 (/usr/bin/python3) is the Jupyter notebook process. "
        "You can confirm that by running `ps`. "
    )

    location.code(
        """
~/projects/gpu_docker$ ps -ef | grep 1716644
1716644 1715961  0 08:47 ?        00:00:27 /usr/bin/python3 -m ipykernel_launcher -f /home/python/.local/share/jupyter/runtime/kernel-0e5ccd1e-e1f6-43a3-8e6a-36bbbbb6c272.json
    """
    )

    location.markdown(
        "Although less verbose, `gpustat` might also be helpful in understanding GPU utilization. "
    )

    location.code(
        """
python@83279f51bc5c:/workspaces/gpu_docker$ gpustat

83279f51bc5c            Wed Jul  7 14:11:48 2021  460.80
[0] GeForce GTX 1050 Ti | 56'C,   1 % |  1577 /  4040 MB |    """
    )

    location.markdown(
        "Thanks for reading. I hope this was helpful and  you're ready to start running code on the GPU. "
    )

    location.markdown("### Helfpul Links")

    location.write(
        """
    * [nvidia-docker](https://github.com/NVIDIA/nvidia-docker)
    * [NVIDIA NVML](https://developer.nvidia.com/nvidia-management-library-nvml)
    * [Docker Run Reference](https://docs.docker.com/engine/reference/run/)
    * [Monitoring GPUs](https://www.andrey-melentyev.com/monitoring-gpus.html)
"""
    )
