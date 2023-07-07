import sys
import os

sys.path.append(os.getcwd())
sys.path.append(f"{os.getcwd()}/src/pyno_logger")

from pyno_logger import Pyno

logger = Pyno(
    {
        "level": "DEBUG",
    }
)

logger.debug("debug log")
logger.trace("trace log")
logger.info("info log")
logger.error("error log")
logger.warn("warning log")

logger.info({"foo": "bar"}, "dict log")
logger.info(["foo", "bar"], "list log")
logger.info(("foo", "bar"), "tuple log")
logger.info(Exception("foo"), "exception log")


def test_mixin():
    return {
        "mixin": "foo",
    }


mixin_logger = Pyno(mixin=test_mixin)

mixin_logger.info("mixin log")
