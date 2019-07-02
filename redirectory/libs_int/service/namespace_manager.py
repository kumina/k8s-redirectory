from flask_restplus import Namespace


class NamespaceManager:
    __instance = None
    namespace_map = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(NamespaceManager, cls).__new__(cls)
        return cls.__instance

    def get_namespace(self, name: str):
        if name not in self.namespace_map:
            self.namespace_map[name] = Namespace(path=f"/{name}", name=name)

        return self.namespace_map[name]
