from configparser import ConfigParser

filepath = "../opt/default.conf"

def load_config(section):
    parser = ConfigParser()
    parser.read(filepath)
    config = dict(parser.items(section))
    return config