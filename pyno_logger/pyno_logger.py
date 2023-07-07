import time
import json
from os import getenv, getpid
from socket import gethostname
from decimal import Decimal

LogLevel = {
    "ERROR": 50,
    "WARNING": 40,
    "INFO": 30,
    "DEBUG": 20,
    "TRACE": 10,
    "SILENT": 0,
}


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class Pyno:
    name = None
    base_ctx = {
        "hostname": gethostname(),
        "pid": getpid(),
    }
    log_level = getenv("LOG_LEVEL") or "INFO"

    omitted_keys = []
    newlines = False

    mixin = None

    def __init__(self, config={}, mixin=None, name=None):
        if self.log_level not in LogLevel.keys():
            raise Exception(f"Invalid log level: {self.log_level}")

        if isinstance(name, str):
            self.name = name

        if isinstance(name, dict):
            self.base_ctx = {**self.base_ctx, **name}

        self.set_config(config, mixin)

    def child(self, name):
        child_logger = Pyno(mixin=self.mixin, name=name)
        child_logger.omitted_keys = self.omitted_keys
        child_logger.newlines = self.newlines
        child_logger.log_level = self.log_level
        return child_logger

    def set_config(self, config={}, mixin=None):
        if config.get("omitted_keys"):
            omitted_keys = config["omitted_keys"]
            if isinstance(omitted_keys, list):
                self.omitted_keys = omitted_keys
            elif isinstance(omitted_keys, tuple):
                self.omitted_keys = list(omitted_keys)
            elif isinstance(omitted_keys, str):
                self.omitted_keys = omitted_keys.split(",")
            else:
                raise Exception("Invalid omitted_keys config")

        if config.get("newlines") and isinstance(config["newlines"], bool):
            self.newlines = config["newlines"]

        if (
            config.get("level")
            and isinstance(config["level"], str)
            and config["level"] in LogLevel.keys()
        ):
            self.log_level = config["level"]

        if mixin and callable(mixin):
            self.mixin = mixin

    def log(self, level, data, message=None):
        level_num = LogLevel.get(level)

        if not level_num or not isinstance(level_num, int):
            raise Exception(f"Invalid log level: {level}")

        if self.log_level == "SILENT" or level_num == 0:
            return

        base_data = {"time": int(time.time())}

        if self.name:
            base_data["name"] = self.name

        if len(self.base_ctx.keys()):
            for key, val in self.base_ctx.items():
                base_data[key] = val

        if level_num >= LogLevel.get(self.log_level):
            ctx = {}
            msg = message

            if isinstance(data, list) or isinstance(data, tuple):
                for index, item in enumerate(data):
                    ctx[f"{index}"] = item
            elif isinstance(data, dict):
                ctx = data
            elif isinstance(data, str):
                msg = data
            elif isinstance(data, Exception):
                ctx = {"error": str(data)}

            # TODO: Add support for custom log formats and serializers

            to_log = {
                **base_data,
                "level": level_num,
                "msg": msg,
            }

            if len(ctx.keys()):
                for key, val in ctx.items():
                    to_log[key] = val

            if self.mixin:
                mixin_dict = self.mixin()
                if isinstance(mixin_dict, dict):
                    for key, val in mixin_dict.items():
                        to_log[key] = val

            if len(self.omitted_keys):
                for key in self.omitted_keys:
                    if key in to_log:
                        del to_log[key]

            try:
                json_to_log = json.dumps(to_log, cls=DecimalEncoder)
                if self.newlines:
                    json_to_log += "\n"
                print(json_to_log)
            except Exception as e:
                print(f"Error logging: {e}")

    def info(self, data={}, message=None):
        self.log("INFO", data, message)

    def warning(self, data={}, message=None):
        self.log("WARNING", data, message)

    def warn(self, data={}, message=None):
        self.warning(data, message)

    def debug(self, data={}, message=None):
        self.log("DEBUG", data, message)

    def trace(self, data={}, message=None):
        self.log("TRACE", data, message)

    def error(self, data={}, message=None):
        self.log("ERROR", data, message)
