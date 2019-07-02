import abc

from redirectory.libs_int.config import Configuration


class Runnable(abc.ABC):
    config: Configuration = None

    def __init__(self):
        self.config = Configuration().values

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def _run_production(self):
        pass

    @abc.abstractmethod
    def _run_development(self):
        pass

    @abc.abstractmethod
    def _run_test(self):
        pass


