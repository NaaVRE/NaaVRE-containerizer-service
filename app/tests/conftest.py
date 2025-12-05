import logging
import os

import pytest


@pytest.fixture(autouse=True)
def capture_logs(caplog):
    """ Automatically captures logs for all tests """
    caplog.set_level(logging.DEBUG)  # Capture all log levels
    yield
    if caplog.records:
        print("\n===== API LOG MESSAGES =====")
        for record in caplog.records:
            print(f"{record.levelname}: {record.message}")
        print("============================")


def pytest_addoption(parser):
    parser.addoption(
        '--containerize-github-all',
        action='store_true',
        help='Submit all containerization test cases to GitHub',
        )


def pytest_generate_tests(metafunc):
    if os.path.exists('resources'):
        base_path = 'resources'
    elif os.path.exists('app/tests/resources/'):
        base_path = 'app/tests/resources/'
    else:
        raise RuntimeError('cannot find test resources')

    if "cell_dir" in metafunc.fixturenames:
        notebook_cells_dir = os.path.join(base_path, 'notebook_cells')
        if metafunc.config.getoption('containerize_github_all', None):
            cells_dirs = [f.path for f in os.scandir(notebook_cells_dir) if
                          f.is_dir()]
        else:
            cells = [
                'check-var-types-dev-user-name-domain-com',
                'r-check-var-types-dev-user-name-domain-com',
                ]
            cells_dirs = [os.path.join(notebook_cells_dir, d) for d in cells]
        metafunc.parametrize("cell_dir", cells_dirs)
