HOST = "localhost"
PORT = 4223

SHORT_IDENT = "XXXXXX"

INFLUX_AUTH = {
    "host": "127.0.0.1",
    "port": 8086,
    "user": "admin",
    "pass": "admin",
    "db": "iotdesks",
    "ssl": False,
}

try:
    config_module = __import__('config_local',
                               globals(), locals())
    for setting in dir(config_module):
        if setting == setting.upper():
            locals()[setting] = getattr(config_module, setting)
except Exception:
    pass
