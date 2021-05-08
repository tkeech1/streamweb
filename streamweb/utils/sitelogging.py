import streamlit as st
import yaml
import logging

logger = logging.getLogger(__name__)


@st.cache
def load_logging_config(filename: str) -> None:
    logging.info(f"loading perf_logging config")
    with open(filename, "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
