from functools import wraps
import time
import logging
from utils.sitelogging import load_logging_config
import logging.config


load_logging_config("perf_logging.yaml")

perf_logger = logging.getLogger("perf_logger")
# propagate doesn't work in the yaml file
perf_logger.propagate = False

# perf_logger = logging.getLogger(__name__)
# perf_logger.setLevel(logging.INFO)
# prevent propagation to root logger

# formatter = logging.Formatter("%(asctime)s,%(message)s")
# perf_file_handler = logging.FileHandler(
#    "/home/python/perf_metrics.log",
# )
# perf_file_handler.setFormatter(formatter)
# perf_logger.addHandler(perf_file_handler)

from streamlit.server.server import Server


def get_request():
    # Hack to get the session object from Streamlit.
    session_infos = Server.get_current()._session_info_by_id.values()
    for session_info in session_infos:
        return session_info.ws.request


# https://www.tornadoweb.org/en/stable/httputil.html#tornado.httputil.HTTPServerRequest
"""request = get_request()
st.write(f"Headers: {request.headers}")
st.write(f'User Agent: {request.headers["User-Agent"]}')
st.write(f'Origin: {request.headers["Origin"]}')
st.write(f"RemoteIP: {request.remote_ip}")
st.write(f"URI: {request.uri}")
st.write(f"Path: {request.path}")
st.write(f"Query: {request.query}")
st.write(f"Body: {request.body}")
st.write(f"Host: {request.host}")
st.write(f"Arguments: {request.arguments}")
st.write(f"Full URL: {request.full_url()}")
st.write(f"Request Time: {request.request_time()}")"""


def log_runtime(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        req = get_request()
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        # time is logged in seconds
        perf_logger.info(
            f"{fn.__module__},{round(t2 - t1,4)},{req.headers['User-Agent'].replace(',','')},{req.headers['Origin'].replace(',','')},{req.remote_ip.replace(',','')},{req.uri.replace(',','')},{req.path.replace(',','')},{req.query.replace(',','')},{req.host.replace(',','')},{req.full_url().replace(',','')},{str(req.request_time()).replace(',','')}"
        )
        return result

    return measure_time
