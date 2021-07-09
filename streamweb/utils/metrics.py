from functools import wraps
import streamlit as st
import time
import logging
import logging.config
from streamlit.server.server import Server
from tornado.httputil import HTTPServerRequest
import yaml

logger = logging.getLogger(__name__)


@st.cache()
def get_perf_logger():
    with open("perf_logging.yaml", "r") as f:
        logger.info("loading perf_logging config")
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    perf_logger = logging.getLogger("perf_logger")
    # propagate=false not working in the yaml file
    perf_logger.propagate = False
    return perf_logger


def get_request() -> HTTPServerRequest:
    try:
        return list(Server.get_current()._session_info_by_id.values())[0].ws.request
    except Exception as e:
        logger.error(f"unable to get request {e}")


def log_runtime(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):

        # https://www.tornadoweb.org/en/stable/httputil.html#tornado.httputil.HTTPServerRequest
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        # time is logged in seconds
        perf_logger = get_perf_logger()

        try:
            req = get_request()
            perf_logger.info(
                # f"{fn.__module__}.{fn.__name__},{round(t2 - t1,4)}"
                f"{fn.__module__},{round(t2 - t1,4)}"
                f",{req.headers['User-Agent'].replace(',','')}"
                f",{req.headers['Origin'].replace(',','')}"
                f",{req.remote_ip.replace(',','')}"
                f",{req.uri.replace(',','')}"
                f",{req.path.replace(',','')}"
                f",{req.query.replace(',','')}"
                f",{req.host.replace(',','')}"
                f",{req.full_url().replace(',','')}"
                f",{str(req.request_time()).replace(',','')}"
            )
        except Exception as e:
            logger.error(f"unable to log request {e}")
        return result

    return measure_time
