import configparser

__conf = {}


def config_init(config_file):
    global __conf
    config = configparser.ConfigParser()
    config.read(config_file)
    sections = config.sections()
    for piece in sections:
        __conf[piece] = {}
        for k, v in config.items(piece):
            __conf[piece].update({k: v})


def get_conf():
    return __conf
