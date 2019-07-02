import pytest


@pytest.fixture
def configuration(monkeypatch, mocker):
    """
    This py.test fixture mocks the Configuration object used by the application
    """
    def pass_mock(*args):
        mock = mocker.MagicMock()

        mock.values.deployment: str = 'test'
        mock.values.log_level: str = 'debug'
        mock.values.node_type: str = 'management'

        mock.values.directories.data: str = '/home/test/redirectory_data'
        mock.values.directories.ui: str = '/home/test/redirectory_ui'

        mock.values.service.ip: str = '0.0.0.0'
        mock.values.service.port: int = 8001
        mock.values.service.metrics_port: int = 8002

        mock.values.database.type: str = 'sqlite'
        mock.values.database.path: str = 'redirectory_sqlite.db'

        mock.values.hyperscan.domain_db: str = 'hs_compiled_domain.hsd'
        mock.values.hyperscan.rules_db: str = 'hs_compiled_rules.hsd'

        mock.values.kubernetes.namespace: str = 'redirectory'
        mock.values.kubernetes.worker_selector: str = ''
        mock.values.kubernetes.management_selector: str = ''
        return mock

    from redirectory.libs_int.config import Configuration
    monkeypatch.setattr(Configuration, '__new__', pass_mock)

    from kubi_ecs_logger import Logger, Severity
    Logger().severity_output_level = Severity[str(Configuration().values.log_level).upper()]
