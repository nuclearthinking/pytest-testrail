import requests


class APIError(Exception):
    pass


class APIClient(requests.Session):

    def __init__(self, base_url: str):
        super().__init__()
        self.verify = False

        self.base_url = f'{base_url}/' if not base_url.endswith('/') else base_url
        self.base_url += 'index.php?/api/v2/'

        self.user = None
        self.password = None

        self.headers.update({
            'Content-Type': 'application/json',
        })

    def build_url(self, path: str) -> str:
        if path.startswith('/'):
            # remove first slash
            path = path[1:]
        return self.base_url + path

    def request(self, method, path, **kwargs):
        try:
            kwargs['auth'] = (self.user, self.password)
            url = self.build_url(path)
            response = super().request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.HTTPError as e:
            code = e.response.status_code
            error = 'No additional error message received'

            if 'error' in e.response.text:
                error = e.response.json()['error']
            raise APIError(f'TestRail API returned HTTP {code} ({error})')

    def get_cases_for_suite(self, project_id: int, suite_id: int) -> dict:
        response = self.get(f'get_cases/{project_id}&suite_id={suite_id}')
        return response.json()
