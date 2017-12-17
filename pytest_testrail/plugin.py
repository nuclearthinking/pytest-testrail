import pytest

from testrail_api import APIClient

URL = None
USER = None
PASSWORD = None


class ConfigurationException(Exception):
    pass


def pytest_addoption(parser):
    parser.addoption(
        '--suite',
        action='store',
        dest='suite',
        default=None,
        help='Run cases from specified project:suite, '
             'example py.test mytests/ --suite=1:79 run all tests from directory mytests '
             'which annotation @case_id relates to one of ids in project 1 suite 79 '
    )
    parser.addoption(
        '--testrail_url',
        action='store',
        dest='testrail_url',
        default=None,
        help='Define the url to your testrail server'
    )
    parser.addoption(
        '--testrail_user',
        action='store',
        dest='testrail_user',
        default=None,
        help='Define testrail api username to login in'
    )
    parser.addoption(
        '--testrail_pass',
        action='store',
        dest='testrail_pass',
        default=None,
        help='Define testrail api user password'
    )


@pytest.hookimpl
def pytest_configure(config):
    global URL, USER, PASSWORD
    try:  # trying to receive params from command line arguments
        URL = config.getoption('testrail_url', skip=True)
        USER = config.getoption('testrail_user', skip=True)
        PASSWORD = config.getoption('testrail_pass', skip=True)
    except:
        pass
    if not all([URL, USER, PASSWORD]):  # if not already defined before, trying receiving settings from pytest.ini
        pytest_ini = config.inicfg
        if pytest_ini:
            try:
                testrail_section = pytest_ini.config.sections.get('testrail')
                URL = testrail_section.get('url')
                USER = testrail_section.get('user')
                PASSWORD = testrail_section.get('password')
                if not all([URL, USER, PASSWORD]):
                    raise ConfigurationException('TestRail API connection params doesnt specify properly')
            except Exception:
                raise ConfigurationException('pytest.ini section [testrail] doesnt configured properly')
        else:
            raise ConfigurationException('pytest.ini doesnt contains [testrail] section')


@pytest.hookimpl
def pytest_collection_modifyitems(config, items):
    run_options = config.getoption('suite')
    if run_options:
        project_id = int(run_options.split(':')[0])
        suites = [int(i) for i in run_options.split(':')[-1].split(',')]
        client = APIClient(URL)
        client.user = USER
        client.password = PASSWORD
        cases = list()
        for suite in suites:
            cases.extend(client.get_cases_for_suite(project_id, suite))
        tests = []
        for item in items:
            if item.keywords._markers.get('case_id'):
                for val in item.keywords._markers.get('case_id').args:
                    tests.append((item, val))
        case_ids_to_run = [item.get('id') for item in cases]
        tests_to_remove = list(filter(lambda test: test[1] not in case_ids_to_run, tests))
        [items.remove(item_to_remove[0]) for item_to_remove in tests_to_remove]
