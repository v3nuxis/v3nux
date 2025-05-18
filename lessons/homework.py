# import json
# import time
# import logging
#
# logging.basicConfig(level=logging.INFO)
#
# class TimerContext:
#     def __enter__(self):
#         self.start = time.monotonic()
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         elapsed = time.monotonic() - self.start
# try:
#     with open('students.json', 'r', encoding='utf-8') as file:
#         students = json.load(file)
# except FileNotFoundError:
#     logging.error("File 'students.json' not found.")
#     students = []
# except json.JSONDecodeError:
#     logging.error("Failed to decode JSON from 'students.json'.")
#     students = []
#
# with TimerContext():
#     logging.info(f"All students: {students}")
#     time.sleep(2)



GLOBAL_CONFIG = {"feature_a": True, "max_retries": 3}

class Configuration:
    def __init__(self, updates, validator=None):
        self.updates = updates
        self.validator = validator
        self.original_config = None

    def __enter__(self):
        self.original_config = GLOBAL_CONFIG.copy()
        GLOBAL_CONFIG.update(self.updates)
        if self.validator:
            try:
                if not self.validator(GLOBAL_CONFIG):
                    raise ValueError("error and i won't tell about your bad")
            except ValueError as e:
                GLOBAL_CONFIG.clear()
                GLOBAL_CONFIG.update(self.original_config)
                raise e
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            GLOBAL_CONFIG.clear()
            GLOBAL_CONFIG.update(self.original_config)
        except Exception as e:
            print(f"Error {e}")

def validate_config(config):
    return config.get("max_retries", 0) >= 0

print("Original Configuration:", GLOBAL_CONFIG)
with Configuration({"feature_a": False, "max_retries": 5}, validator=validate_config):
    print("Inside Context (Valid Updates):", GLOBAL_CONFIG)
print("Restored Configuration:", GLOBAL_CONFIG)

try:
    with Configuration({"max_retries": -1},):
        print("Inside Context (Invalid Updates):", GLOBAL_CONFIG)
except KeyboardInterrupt as e:
    print("ctrl c Error:", e)
print("Restored Configuration:", GLOBAL_CONFIG)

try:
    with Configuration({"feature_a": False}, validator=validate_config):
        print("Inside Context (Before Error):", GLOBAL_CONFIG)
        raise RuntimeError("error")
except RuntimeError as e:
    print("Caught Exception:", e)
print("Restored Configuration:", GLOBAL_CONFIG)
