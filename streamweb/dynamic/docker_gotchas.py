import streamlit as st
import datetime
import pytz
from datetime import date
from utils.metrics import log_runtime

short_title = "A Few Docker Things..."
long_title = "A Few Docker Things I Can Never Remember"
key = 5
content_date = datetime.datetime(2021, 9, 1).astimezone(pytz.timezone("US/Eastern"))
assets_dir = "./assets/" + str(key) + '/'

@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    #location.write(f"*{content_date.strftime('%m.%d.%Y')}*")

    location.markdown("### Upgrading Packages That Prompt For Installation Options")

    location.markdown("It's often a good idea to update Docker images with the latest security patches and software versions. ")

    location.code("""
FROM nvidia/cuda:11.0-base-ubuntu20.04
RUN apt update && apt dist-upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*
""")

    location.markdown("Upgrading certain packages, however, may prompt for user input and halt the container build - not ideal in an automated process. "
    "Below is a snippet from `apt dist-upgrade` in which the tzdata package prompts for the user's time zone."
    )

    location.code("""
Setting up tzdata (2021a-0ubuntu0.20.04) ...
debconf: unable to initialize frontend: Dialog
debconf: (TERM is not set, so the dialog frontend is not usable.)
debconf: falling back to frontend: Readline
Configuring tzdata
------------------

Please select the geographic area in which you live. Subsequent configuration
questions will narrow this down by presenting a list of cities, representing
the time zones in which they are located.

  1. Africa      4. Australia  7. Atlantic  10. Pacific  13. Etc
  2. America     5. Arctic     8. Europe    11. SystemV
  3. Antarctica  6. Asia       9. Indian    12. US
Geographic area: 
    """)

    location.markdown("To avoid the user prompt for specific packages, set the `DEBIAN_FRONTEND=noninteractive` environment variable. "
    "Setting `--no-install-recommends` is also a good idea to help reduce the size of your Docker image. It instructs apt not install recommended packages."
    )

    location.code("""
RUN apt update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata && apt dist-upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*
    """)

    location.markdown("### Entrypoints and CMD")

    location.markdown("Entrypoints allow a container to be run as an executable. There are two forms for an entrypoint, *shell* form and *exec* form. In a "
    "Dockerfile, the *exec* form looks like this:"
    )

    location.code("""
ENTRYPOINT ["myscript.sh", "option1", "option2"]
    """)

    location.markdown("And *shell* form looks like this:"
    )

    location.code("""
ENTRYPOINT myscript.sh option1 option2
    """)

    location.markdown("*Exec* form runs the entrypoint with PID 1 and allows the process to recieve UNIX signals from the docker daemon. "
    "If the process handles UNIX signals (`SIGTERM`, `SIGINT`, etc.), use *exec* form. "
    )
    
    location.markdown(
    "Docker runs the entrypoint command on container startup and appends any command line arguments passed through `docker run`. For example: "
    )

    location.code("""
docker run image option1 option2""")
    
    location.markdown("`option1` and `option2` are appended to the entrypoint as additional arguments and override any elements passed via CMD."
    "")

    location.markdown("*Shell* form entrypoints cannot handle UNIX signals since the entrypoint is started as a subcommand of `/bin/sh -c`. "
    "*Shell* form entrypoint arguments also cannot be overridden by CMD or additional command line arguments."
    )

    location.markdown("CMD can also be used to specify the command to execute when a container starts but it's more commonly used as a way of "
    "defining default arguments for an entrypoint as shown below. ")

    location.code("""
ENTRYPOINT ["program.sh"]
CMD [“option1”, “option2”]
    """)

    location.markdown("The above code will execute `program.sh option1 option2` when the container starts. ")

        
    location.markdown("### Starting Services with a Script in a Container")
    
    location.markdown("Sometimes, a wrapper script is necessary to perform setup and configuration prior to starting the process that runs inside a container. "
    "When starting a process from a script, use `exec` to run the process (not the wrapper script) as PID 1. This allows the process to recieve UNIX signals. "
    "`gosu` is also useful for running the process as a non-root user."
    )

    location.markdown("The following Dockerfile runs from `ps aux` inside an entrypoint bash script without using `exec`.")
    
    location.code("""
FROM ubuntu:focal
COPY docker-entrypoint.sh .
RUN chmod 755 docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
    """)

    location.code("""
#!/bin/sh
# docker-entrypoint.sh
ps aux
    """)

    location.markdown("This entrypoint script is PID 1 which isn't what we want. It's also running as root which is not ideal. ")

    location.code("""
docker run -it --rm dockertest
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  8.0  0.0   2608   548 pts/0    Ss+  00:29   0:00 /bin/sh /dock
root           8  0.0  0.0   5896  2900 pts/0    R+   00:29   0:00 ps aux

    """)

    location.markdown("If we use `exec`, the process runs as PID 1. "
    "`gosu` allows you to run the process as a non-root user."
    )

    location.code("""
#!/bin/sh
# docker-entrypoint.sh
exec gosu nobody ps aux
    """)

    location.code("""
docker run -it --rm dockertest
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
nobody         1  0.0  0.0   5816  1160 pts/0    Rs+  00:34   0:00 ps aux
    """)

    location.markdown("Now we have a process running as PID 1 under a non-root user. Exactly what we wanted."
    )
    
    location.markdown("Thanks for reading."
    )

    location.markdown("### Resources")

    location.write(
        """
    * [Docker Documentation](https://docs.docker.com/engine/reference/builder/)
    * [gosu](https://github.com/tianon/gosu)
    * [Debian: debian_frontend=noninteractive](https://linuxhint.com/debian_frontend_noninteractive/)
    * [Docker using gosu vs USER](https://stackoverflow.com/questions/36781372/docker-using-gosu-vs-user)
"""
    )
    