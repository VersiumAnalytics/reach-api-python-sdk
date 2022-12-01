import logging
from unittest.mock import patch

from aiohttp.test_utils import AioHTTPTestCase, TestServer, Application

from reach import append
from tests.utils import make_app, RequestHandler, RateChecker


class TestAppend(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        self.rate_checker = RateChecker(max_calls=5, max_connections=5, min_calls=5, min_connections=5, period=1)
        self.request_handler = RequestHandler(self.rate_checker, response_time=1.5)
        return make_app(self.request_handler)

    async def get_server(self, app: Application) -> TestServer:
        """Return a TestServer instance."""
        test_server = TestServer(app, loop=self.loop, skip_url_asserts=False)
        return test_server

    async def setUpAsync(self):
        await super().setUpAsync()
        patcher = patch.object(append.aiohttp, 'ClientSession', autospec=True)
        self.addCleanup(patcher.stop)
        self.ClientSession = patcher.start()
        self.ClientSession.return_value = self.client

        # Silence aiohttp logs
        aiohttp_logs = ['aiohttp.access',
                        'aiohttp.client',
                        'aiohttp.internal',
                        'aiohttp.server',
                        'aiohttp.web',
                        'aiohttp.websocket']
        for log_name in aiohttp_logs:
            logging.getLogger(log_name).handlers = []

    def test_rate_limit(self):
        records = [{"first": "John", "last": "Doe"}] * 15
        append.query_api("test_rate_limit", records, query_params={"cfg_max_recs": 1},
                         headers={'Accept': 'application/json', 'x-versium-api-key': "123-456"},
                         n_retry=0,
                         queries_per_second=5,
                         n_connections=5,
                         retry_wait_time=1,
                         timeout=5)
        self.rate_checker.raise_if_error()
