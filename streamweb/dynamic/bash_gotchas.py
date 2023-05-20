import streamlit as st
import datetime
import pytz
from datetime import date
from utils.metrics import log_runtime
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

short_title = "A Few Bash Things"
long_title = "A Few Bash Things I Can Never Remember"
key = 10
content_date = datetime.datetime(2021, 9, 15).astimezone(pytz.timezone("US/Eastern"))
assets_dir = "./assets/" + str(key) + '/'

@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    #location.write(f"*{content_date.strftime('%m.%d.%Y')}*")

    location.markdown("""
### Waiting for a Specific Condition

Instead of using `sleep 100` (which may end up wasting time), try the following one-liner to repeatedly check if a condition is met:

```
until curl -o /dev/null -s -w "%{http_code}" -X GET "http://localhost:8000/hello?name=todd" > /dev/null 2>&1; do echo "sleeping - waiting for container to be ready..."; sleep 1; done
```
    """)

    location.markdown("""
### Downloading and Installing Via curl/wget

These are very useful in a Dockerfile.

```
curl -L https://releases.hashicorp.com/terraform/0.15.0/terraform_0.15.0_linux_amd64.zip -o /tmp/tf.zip; unzip /tmp/tf.zip -d /usr/local/bin/; rm /tmp/tf.zip
wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh -O ~/miniconda.sh && /bin/bash ~/miniconda.sh -b -p /opt/conda
```

    """)

    location.markdown("""
### Recursively Search for Specific Text in a Specific Filename 

This is particularly useful for finding things buried in a Dockerfile somewhere on your system.

```
grep --include=Dockerfile -rnw '../' -e "wget"
```

    """)

    

    

    
    



