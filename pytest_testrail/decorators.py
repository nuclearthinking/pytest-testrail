import pytest


def case_id(*args):
    return pytest.mark.case_id(*args)
