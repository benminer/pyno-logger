# Pyno Logger 🔥

Pyno is a Python logging package inspired by [Pino](https://www.npmjs.com/package/pino) for NodeJS. It provides a simple and customizable way to log messages with different log levels to the console in JSON format with optional log message customization.

## Installation

To install Pyno, use the following command:

```bash
pip install pyno_logger
```

## Usage

To use Pyno, you need to import the package and create an instance of the `Pyno` class. Here's an example:

```python
from pyno_logger import Pyno

logger = Pyno(config={"level": "INFO"}, mixin=SomeFunction)
```

The `Pyno` class takes am optional configuration dictionary as an argument. The configuration options are as follows:

- `level` (optional): Specifies the log level. Valid log levels are "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", and "SILENT". The default log level is "INFO". By default, Pyno uses the `LOG_LEVEL` environment variable if nothing is passed via the `config` dict.

- `omitted_keys` (optional): Specifies a list of keys to omit from the logged data. It can be a list, tuple, or comma-separated string.
- `newlines` (optional): Specifies whether to append a newline character to the end of each log message. It should be a boolean value.

The second param, `mixin`, allows for injecting a function that returns additional contextual data. Useful for any global state or dynamic data.

- `mixin` (optional): Specifies a mixin function that returns a dictionary of additional data to include in log messages.

### Logging Methods

Pyno provides several logging methods that correspond to different log levels:

- `info(data={}, message=None)`: Logs an informational message with the provided data and an optional message.
- `warning(data={}, message=None)`: Logs a warning message with the provided data and an optional message.
- `warn(data={}, message=None)`: Logs a warning message (alias for `warning`).
- `debug(data={}, message=None)`: Logs a debug message with the provided data and an optional message.
- `trace(data={}, message=None)`: Logs a trace message with the provided data and an optional message.
- `error(data={}, message=None)`: Logs an error message with the provided data and an optional message.

Each logging method takes two optional arguments: `data` and `message`. The `data` argument can be a dictionary, list, tuple, string, or Exception object containing additional contextual data. The `message` argument is a string that represents the log message. If not provided, the log message will be automatically generated based on the log level and data.

By default, Pyno includes the fields `time`, `pid`, `hostname` and `level`. These can be omitted via the `omitted_keys` config param, if desired.

### Log Levels

Pyno uses the following log levels:

- `ERROR`: 50
- `WARNING`: 40
- `INFO`: 30
- `DEBUG`: 20
- `TRACE`: 10
- `SILENT`: 0

The log level determines which log messages will be displayed based on the configured log level. Messages with a log level equal to or higher than the configured log level will be logged.

### Child Loggers

The Pyno instance can be cloned with additional data, or name, to be included in all of the child's logs:

- `child(name: str | dict)`: Creates a child logger with the specified name. The child logger inherits the configuration options and mixin (if any) from the parent logger.

### Examples

Here are some examples of how to use Pyno:

```python
# Create a logger with default configuration
logger = Pyno(config={"level": "INFO"})

logger.info("This is an informational message.")
logger.warning({"user_id": 123}, "This is a warning message.")
logger.error({"error_code": 500}, "An error occurred.")
# or log an Exception instance
logger.error(Exception('something went wrong!'), "An error occured")

# Create a child logger with additional configuration
child_logger = logger.child("child_logger")
child_logger.debug("Debug message from child logger.")
# Will output `{ "name": "child_logger", "msg": "Debug message from child logger."}

# Create a child logger with a dictionary
child_logger = logger.child({ "module": "SubModule" })
child_logger.debug("Debug message from child logger.")
# Will output `{ "module": "SubModule", "msg": "Debug message from child logger."}

# Create a logger with a mixin
def get_user_id():
    return {
        "user": user_id
    }
mixin_logger = Pyno(mixin=get_user_id)
mixin_logger.info("got a user")
# Will output `{ "msg": "got a user", "user": user_id }`
```

In the above example, the log messages will be printed to the console in JSON format.

## TODOS

- Customizable Log Levels
- Configurable Serializers for logging class instances
