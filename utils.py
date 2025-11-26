import json
import config

def calculate_metric(data, factor):
    # A simple function that uses the config file
    base = config.DEFAULT_SCALING
    return [d * factor * base for d in data]

def load_registry():
    return json.loads('{"status": "active"}')