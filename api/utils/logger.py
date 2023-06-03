"""Logger module."""
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s : %(filename)s(%(lineno)d) : %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

log = logging.getLogger("reachdata")
