# Python Logging Module - Comprehensive Guide

The Python `logging` module provides a flexible framework for tracking events within your application, enabling easy debugging and diagnosis. This README covers the essentials of logging, including log levels, configurations, handlers, formatters, rotation techniques, and examples for various use cases.

## Table of Contents
- [Basics of Logging](#basics-of-logging)
- [Log Levels](#log-levels)
- [Configuring Loggers](#configuring-loggers)
- [Handlers](#handlers)
  - [FileHandler](#filehandler)
  - [RotatingFileHandler](#rotatingfilehandler)
  - [TimedRotatingFileHandler](#timedrotatingfilehandler)
  - [StreamHandler](#streamhandler)
- [Formatters and Formatting Variables](#formatters-and-formatting-variables)
- [Exception Handling with Logging](#exception-handling-with-logging)
- [Complete Example with File, Stream, and Rotation Handlers](#complete-example-with-file-stream-and-rotation-handlers)

---

## Basics of Logging

The `logging` module uses a hierarchy of loggers to manage logging across your application. Key components include:
- **Logger**: Manages and routes log messages.
- **Handlers**: Define where log messages go (e.g., files, console).
- **Formatter**: Controls the layout of log messages.

### Simple Example

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.info("This is an info log.")
```

## Log Levels

Python’s logging has five standard levels:
- **DEBUG**: Detailed information for diagnosing issues.
- **INFO**: Confirmation that things are working as expected.
- **WARNING**: Indication of something unexpected or potential issues.
- **ERROR**: Serious issues that prevent parts of the application from functioning.
- **CRITICAL**: Severe errors indicating the application might not be able to continue.

## Configuring Loggers

To control logging behavior across modules, configure a logger with a minimum **level** and attach **handlers**. 

```python
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)  # Set minimum logging level
```

## Handlers

Handlers direct log output to different destinations, like files or the console. 

### FileHandler

The `FileHandler` writes log records to a file.

```python
file_handler = logging.FileHandler("my_log.log")
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
```

### RotatingFileHandler

The `RotatingFileHandler` rotates files when they reach a specific size, preventing the log file from growing indefinitely.

```python
from logging.handlers import RotatingFileHandler

rotating_handler = RotatingFileHandler("my_rotating_log.log", maxBytes=1024, backupCount=5)
rotating_handler.setLevel(logging.INFO)
logger.addHandler(rotating_handler)
```

- **`maxBytes`**: Maximum file size in bytes before rotation.
- **`backupCount`**: Number of backup files to retain.

### TimedRotatingFileHandler

The `TimedRotatingFileHandler` rotates files at regular intervals (e.g., every minute, day).

```python
from logging.handlers import TimedRotatingFileHandler

timed_handler = TimedRotatingFileHandler("timed_log.log", when="s", interval=5, backupCount=5)
logger.addHandler(timed_handler)
```

- **`when`**: Time interval (e.g., "s" for seconds, "m" for minutes).
- **`interval`**: Frequency of rotation.
- **`backupCount`**: Number of backup files to retain.

### StreamHandler

The `StreamHandler` sends log output to the console or any other stream, such as `sys.stdout`.

```python
import sys

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.WARNING)
logger.addHandler(stream_handler)
```

## Formatters and Formatting Variables

Formatters define the layout of log messages. You can specify variables that display information like timestamps, log levels, and module names.

### Common Formatting Variables

- **`%(asctime)s`**: Timestamp of the log record.
- **`%(levelname)s`**: Level of the log (e.g., INFO, ERROR).
- **`%(name)s`**: Name of the logger (usually the module).
- **`%(message)s`**: Log message.
- **`%(filename)s`**: Name of the file containing the log.
- **`%(lineno)d`**: Line number where the log call was made.
- **`%(funcName)s`**: Name of the function that issued the log call.
- **`%(threadName)s`**: Thread name from which the log was issued.
- **`%(process)d`**: Process ID (useful for multi-processing).

### Setting Up a Formatter

```python
formatter = logging.Formatter("[%(levelname)s] %(name)s - %(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
```

## Exception Handling with Logging

Use `logging` with `traceback` to log detailed error messages during exceptions.

```python
try:
    my_list = [1, 2]
    print(my_list[2])  # Will raise an IndexError
except IndexError:
    logging.error("An error occurred: %s", traceback.format_exc())
```

## Complete Example with File, Stream, and Rotation Handlers

The example below sets up a comprehensive logging system with `FileHandler`, `StreamHandler`, and rotating handlers.

```python
import logging
import sys
import traceback
import time
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# Basic logging setup
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%m/%d/%Y %H:%M:%S")

logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")

# Non-propagating logger setup
logger = logging.getLogger(__name__)
logger.propagate = False
logger.info("This is an info message from a non-propagating logger")

# Stream and File handlers with levels and formatter
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('file.log')
stream_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.warning("This is a warning")
logger.error("This is an error")

# Handling exceptions with logging
try:
    sample_list = [1, 2]
    print(sample_list[2])  # Raises IndexError
except IndexError:
    logging.error("An error occurred: %s", traceback.format_exc())

# Advanced log rotation with rotating and timed handlers
rotating_handler = RotatingFileHandler('rotating_file.log', maxBytes=2000, backupCount=5)
timed_rotating_handler = TimedRotatingFileHandler('timed_file.log', when="s", interval=5, backupCount=5)
logger.addHandler(rotating_handler)
logger.addHandler(timed_rotating_handler)

# Log entries to trigger rotation
for i in range(6):
    logger.info("Rotating handler log message #%d", i + 1)
    time.sleep(1)

print("Logging setup complete.")
```

### Explanation of Each Component

1. **Basic Logging Configuration**: Configures logging with `basicConfig` to output to the console.
2. **Logger with Propagation Control**: Demonstrates disabling propagation for more precise log control.
3. **Stream and File Handlers**: Demonstrates separate log levels and formats for console and file outputs.
4. **Exception Logging**: Uses `traceback` for detailed error logging.
5. **Rotating Handlers**: Demonstrates both file size-based and time-based log rotation.

---

### Summary

This guide covers Python’s `logging` module and demonstrates configurations, formats, log rotation, and exception handling. With proper configuration, logging can provide insightful information about program behavior and improve error diagnosis and debugging, particularly in production environments.
