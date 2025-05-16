Lesson 6

Python Context Managers: TimerContext and Configuration
This repository contains two Python context managers that simplify common tasks: measuring execution time (TimerContext) and managing temporary configuration changes (Configuration). These tools are designed to be reusable, robust, and easy to integrate into any Python project.

1. TimerContext: Measure Execution Time
The TimerContext context manager measures and logs the execution time of a block of code. It uses Python's time module to calculate the elapsed time and logs it using the logging module.

Features:
Automatically measures the time taken for a block of code.
Logs the elapsed time in seconds with two decimal places.
Integrates seamlessly with Python's logging system.
Example Usage:
python


1
2
3
4
5
6
7
⌄
import time
import logging

logging.basicConfig(level=logging.INFO)

with TimerContext():
    time.sleep(2)  # Simulate a task that takes 2 seconds
Output:


1
INFO:root:Elapsed: 2.00 seconds
Use Cases:
Benchmarking code performance.
Logging execution times for debugging or monitoring purposes.
2. Configuration: Temporary Configuration Changes
The Configuration context manager applies temporary updates to a global configuration dictionary and ensures the original configuration is restored after the context exits, even if an error occurs. It optionally supports validation of the updated configuration.

Features:
Temporarily updates a global configuration (GLOBAL_CONFIG) with a dictionary of changes.
Restores the original configuration when exiting the context, regardless of errors.
Supports optional validation of the updated configuration using a custom validator function.
Example Usage:
GLOBAL_CONFIG = {"feature_a": True, "max_retries": 3}

def validate_config(config):
    return config.get("max_retries", 0) >= 0

# Test with valid updates
print("Original Configuration:", GLOBAL_CONFIG)
with Configuration({"feature_a": False, "max_retries": 5}, validator=validate_config):
    print("Inside Context (Valid Updates):", GLOBAL_CONFIG)
print("Restored Configuration:", GLOBAL_CONFIG)

# Test with invalid updates
try:
    with Configuration({"max_retries": -1}, validator=validate_config):
        print("Inside Context (Invalid Updates):", GLOBAL_CONFIG)
except ValueError as e:
    print("Validation Error:", e)
print("Restored Configuration:", GLOBAL_CONFIG)

# Test with an error inside the context
try:
    with Configuration({"feature_a": False}, validator=validate_config):
        print("Inside Context (Before Error):", GLOBAL_CONFIG)
        raise RuntimeError("An error occurred!")
except RuntimeError as e:
    print("Caught Exception:", e)
print("Restored Configuration:", GLOBAL_CONFIG)


Output:
Original Configuration: {'feature_a': True, 'max_retries': 3}
Inside Context (Valid Updates): {'feature_a': False, 'max_retries': 5}
Restored Configuration: {'feature_a': True, 'max_retries': 3}
Validation Error: Invalid configuration after applying updates.
Restored Configuration: {'feature_a': True, 'max_retries': 3}
Inside Context (Before Error): {'feature_a': False, 'max_retries': 3}
Caught Exception: An error occurred!
Restored Configuration: {'feature_a': True, 'max_retries': 3}