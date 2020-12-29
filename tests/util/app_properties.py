import configparser


def get_property(section, property_name):
    config = configparser.RawConfigParser()
    config.read('config.properties')
    return config.get(section, property_name)
