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
