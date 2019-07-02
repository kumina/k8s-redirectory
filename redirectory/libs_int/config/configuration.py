import confuse

configuration_path_env_var = "REDIRECTORY_CONFIG_DIR"

configuration_template = {
    "deployment": confuse.Choice(["prod", "dev", "test"]),
    "log_level": confuse.Choice(["debug", "info", "warning", "error", "critical"]),
    "node_type": confuse.Choice(["management", "worker", "compiler"]),
    "directories": {
        "data": confuse.String(),
        "ui": confuse.String()
    },
    "service": {
        "ip": confuse.String(),
        "port": confuse.Integer(),
        "metrics_port": confuse.Integer()
    },
    "database": {
        "type": confuse.Choice(["sqlite", "mysql"]),
        "path": confuse.String(default="redirectory_sqlite.db"),
        "host": confuse.String(default="localhost"),
        "port": confuse.Integer(default=3306),
        "name": confuse.String(default="redirectory"),
        "username": confuse.String(default="user"),
        "password": confuse.String(default="pass")
    },
    "hyperscan": {
        "domain_db": confuse.String(default="hs_compiled_domain.hsd"),
        "rules_db": confuse.String(default="hs_compiled_rules.hsd")
    },
    "kubernetes": {
        "namespace": confuse.String(default="redirectory"),
        "worker_selector": confuse.String(default="app=redirectory-worker"),
        "management_selector": confuse.String(default="app=redirectory-management")
    }
}


class Configuration:
    __instance = None
    __config_parser = None

    values = None
    path = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Configuration, cls).__new__(cls)

            cls.__instance.__config_parser = confuse.Configuration("redirectory", __name__, read=False)
            cls.__instance.__config_parser._env_var = configuration_path_env_var
            cls.__instance.__config_parser.read()

            cls.__instance.values = cls.__instance.__config_parser.get(template=configuration_template)
            cls.__instance.path = cls.__instance.__config_parser.config_dir()

        return cls.__instance
