import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taxi_service.settings")
django.setup()


@pytest.fixture(scope="session", autouse=True)
def django_test_database():
    from django.test.runner import DiscoverRunner

    runner = DiscoverRunner(verbosity=0, interactive=False)
    runner.setup_test_environment()
    database_config = runner.setup_databases()
    try:
        yield
    finally:
        runner.teardown_databases(database_config)
        runner.teardown_test_environment()
