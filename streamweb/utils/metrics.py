from functools import wraps
import time
import logging
import logging.config
from utils.siteutils import get_request
import yaml

logger = logging.getLogger(__name__)

with open("perf_logging.yaml", "r") as f:
    logger.info("loading perf_logging config")
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

perf_logger = logging.getLogger("perf_logger")
# propagate=false not working in the yaml file
perf_logger.propagate = False


def log_runtime(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        # https://www.tornadoweb.org/en/stable/httputil.html#tornado.httputil.HTTPServerRequest
        req = get_request()
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        # time is logged in seconds
        perf_logger.info(
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
        return result

    return measure_time
