import json

# local path to json config 

def import_config():
    config_path = "exampleTopo.json"

    #config_path = input("Path to config file: ")

    with open(config_path, "r") as file:
        config = json.load(file)

    return config

def export_config(config):
    config_path = "exampleTopo.json"

    with open(config_path, "w") as file:
        json.dump(config, file, indent = 3)