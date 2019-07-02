import multiprocessing

from gunicorn.app.base import BaseApplication
from gunicorn.six import iteritems

MAX_NUMBER_OF_WORKERS = 1


class GunicornServer(BaseApplication):
    """
    This class provides the ability to run gunicorn server from
    inside of python instead of the running it through the command prompt
    Gives you a nicer way to handle it and you can override key methods
    to make it more specific for our use case
    """

    def init(self, parser, opts, args):
        pass

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(GunicornServer, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        self.load_metric_server()
        return self.application

    @staticmethod
    def load_metric_server():
        """
        When run() is called on Gunicorn it starts a new process with this flask App.
        The metric server must run in the same process as the Flask API in order to
        share the metrics. This function starts the metric server when the Flask APP
        is loaded into the new process.
        """
        from redirectory.libs_int.metrics import start_metrics_server
        start_metrics_server()

    @staticmethod
    def get_number_of_workers(is_worker: bool = False):
        """
        Calculates the number of workers the gunicorn server will use
        """
        if is_worker:
            return 1
        return min((multiprocessing.cpu_count() * 2) + 1, MAX_NUMBER_OF_WORKERS)
