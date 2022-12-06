import logging
import sys
import time
from asyncio import sleep
from functools import partial

from aiohttp import web

from .responses import MOCK_RESPONSES, GENERIC_RESPONSE


class RateLimitExceededError(RuntimeError):
    pass


class LowQPSError(RuntimeError):
    pass


class MaxConnectionsExceededError(RuntimeError):
    pass


class UnusedConnectionsError(RuntimeError):
    pass


class RateChecker:
    """ Checks that the number of calls and connections to the test server do not exceed the maximum.

        Checks for exceeding connections or queries per second are deferred until the end of a test.
        Parameters
        ----------
        max_calls : int
            Maximum number of function calls allowed within a time period.

        max_connections : int
            Maximum number of total active function calls to allow.

        min_calls : int
            Minimum number of calls per period required. When `raise_if_error` is called, an error is thrown if the highest number of calls
            per period is less than `min_calls` - `min_calls_tol`

        min_connections : int
            Minimum number of connections required. When `raise_if_error` is called, an error is thrown if the highest number of connections
            is less than `min_connections`

        period : float
            Length of time period in seconds.

        min_calls_tol : float
            Tolerance allowed for `min_calls` criteria before an error is thrown.
        """

    def __init__(self, *, max_calls=20, max_connections=100, min_calls=0, min_connections=0, period=1, min_calls_tol=0.1):
        # Max allowed connections and calls
        self.max_calls = max_calls
        self.max_connections = max_connections
        self.min_calls = min_calls
        self.min_connections = min_connections
        self.min_calls_tol = min_calls_tol
        self.period = period

        # Timers
        self.clock = time.monotonic
        self.last_reset = time.monotonic()

        # Current number of connections and calls
        self.num_calls = 0
        self.num_connections = 0
        self.total_calls = 0

        # Highest observed connections and queries per second
        self.highest_qps = 0.0
        self.highest_connections = 0

    @property
    def qps(self):
        return self.num_calls / self.period

    @property
    def max_qps(self):
        return self.max_calls / self.period

    @property
    def min_qps(self):
        return self.min_calls / self.period

    def __call__(self):
        self.num_calls += 1
        self.total_calls += 1
        if self.__period_remaining():
            self.highest_qps = max(self.highest_qps, self.qps)

    def __period_remaining(self):
        elapsed = self.clock() - self.last_reset
        period_remaining = self.period - elapsed
        if period_remaining <= 0:
            self.num_calls = 0
            self.last_reset = self.clock()
            period_remaining = self.period
        return period_remaining

    def add_connection(self):
        self.num_connections += 1
        self.highest_connections = max(self.num_connections, self.highest_connections)

    def remove_connection(self):
        self.num_connections -= 1

    def raise_if_error(self):
        if self.highest_qps > self.max_qps:
            raise RateLimitExceededError(f"Rate limit exceeded. Max rate limit was: {self.max_qps:.2f} qps. "
                                         f"Instead got {self.highest_qps:.2f} qps")

        elif self.highest_connections > self.max_connections:
            raise MaxConnectionsExceededError(f"Got {self.highest_connections} connections. Max connections set to {self.max_connections}")

        elif self.highest_qps < self.min_qps - self.min_calls_tol:
            raise LowQPSError(f"Low QPS rate. Min rate was: {self.min_qps:.2f} qps. Instead got {self.highest_qps:.2f}")

        elif self.highest_connections < self.min_connections:
            raise UnusedConnectionsError(f"Unused connections. Min number of connections was: {self.min_connections}. Instead got "
                                         f" {self.highest_connections} connections.")


class RequestHandler:

    def __init__(self, rate_checker, response_time=0.0):
        self.rate_checker = rate_checker
        self.response_time = response_time

    async def test_ratelimit(self, request):
        self.rate_checker.add_connection()
        try:
            self.rate_checker()
            await sleep(self.response_time)
            return web.json_response(GENERIC_RESPONSE)
        finally:
            self.rate_checker.remove_connection()

    async def handle_request(self, api, request):
        return MOCK_RESPONSES[api.tolower()]

    async def handle_request_delayed(self, api, request):
        await sleep(self.response_time)
        return self.handle_request(api, request)


def make_app(rh: RequestHandler):
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')
    sh = logging.StreamHandler(sys.stderr)
    logger.addHandler(sh)
    logger.handlers = []

    app = web.Application(logger=logger)
    app.router.add_routes(
        [web.post('/v2/test_rate_limit', rh.test_ratelimit),
         web.post('/v2/contact', partial(rh.handle_request, 'contact')),
         web.post('/v2/demographic', partial(rh.handle_request, 'demographic')),
         web.post('/v2/b2cOnlineAudience', partial(rh.handle_request, 'b2cOnlineAudience')),
         web.post('/v2/b2bOnlineAudience', partial(rh.handle_request, 'b2bOnlineAudience')),
         web.post('/v2/firmographic', partial(rh.handle_request, 'firmographic')),
         web.post('/v2/c2b', partial(rh.handle_request, 'c2b')),
         web.post('/v2/iptodomain', partial(rh.handle_request, 'iptodomain')),
         web.post('/v2/hemtobusinessdomain', partial(rh.handle_request, 'hemtobusinessdomain'))])
    return app
