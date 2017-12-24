import pytest

from pytest_testrail.testrail_api import APIClient


class TestAPIClient:

    @pytest.mark.parametrize('path', [
        '/get_cases',
        'get_cases',
    ])
    @pytest.mark.parametrize('url', [
        'http:/url.path.com',
        'http:/url.path.com/',
    ])
    def test_build_url(self, path, url):
        cl = APIClient(url)
        url = cl.build_url(path)

        assert url == 'http:/url.path.com/index.php?/api/v2/get_cases'
