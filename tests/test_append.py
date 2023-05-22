import logging

from reach import append
from .base import BaseTestCase

logging.basicConfig(level=logging.INFO)


class TestAppend(BaseTestCase):

    def test_rate_limit(self):
        self.request_handler.response_time = 1.5
        self.rate_checker.min_calls = 5
        self.rate_checker.min_connections = 5
        records = [{"first": "John", "last": "Doe"}] * 15
        append.query_api("contact", records, query_params={"cfg_max_recs": 1},
                         headers={'Accept': 'application/json', 'x-versium-api-key': "123-456"},
                         n_retry=0,
                         queries_per_second=5,
                         n_connections=5,
                         retry_wait_time=1,
                         timeout=5)
        self.rate_checker.raise_if_error()

    def test_retry_429_all_fail(self):
        records = [{"first": "John", "last": "Doe"}] * 2
        self.request_handler.http_status = 429
        append.query_api("contact", records, query_params={"cfg_max_recs": 1},
                         headers={'Accept': 'application/json', 'x-versium-api-key': "123-456"},
                         n_retry=2,
                         queries_per_second=5,
                         n_connections=5,
                         retry_wait_time=1,
                         timeout=5)
        # Should have 6 calls. 2 records each query 1 time, then each
        assert self.rate_checker.total_calls == 6

    def test_retry_429_some_fail(self):
        self.request_handler.store_requests = True
        records = [{"first": "John", "last": "Doe"}] * 2
        self.request_handler.http_status = [429, 429, 200, 200, 200, 200, 200]
        append.query_api("contact", records, query_params={"cfg_max_recs": 1},
                         headers={'Accept': 'application/json', 'x-versium-api-key': "123-456"},
                         n_retry=2,
                         queries_per_second=5,
                         n_connections=5,
                         retry_wait_time=1,
                         timeout=5)

        print(dir(self.request_handler.requests[0]))
        print(self.request_handler.requests[0].query_string)
        # Should have 4 calls. 2 records each query 1 time and fail 1 time, then each succeed on their next call
        assert self.rate_checker.total_calls == 4

    def test_retry_500_all_fail(self):
        records = [{"first": "John", "last": "Doe"}] * 2
        self.request_handler.http_status = 500
        append.query_api("contact", records, query_params={"cfg_max_recs": 1},
                         headers={'Accept': 'application/json', 'x-versium-api-key': "123-456"},
                         n_retry=2,
                         queries_per_second=5,
                         n_connections=5,
                         retry_wait_time=1,
                         timeout=5)
        # Should have 6 calls. 2 records each query 1 time, then each
        assert self.rate_checker.total_calls == 6

    def test_retry_500_some_fail(self):
        records = [{"first": "John", "last": "Doe"}] * 2
        self.request_handler.http_status = [500, 500, 200, 200, 200, 200, 200]
        append.query_api("contact", records, query_params={"cfg_max_recs": 1},
                         headers={'Accept': 'application/json', 'x-versium-api-key': "123-456"},
                         n_retry=2,
                         queries_per_second=5,
                         n_connections=5,
                         retry_wait_time=1,
                         timeout=5)

        # Should have 4 calls. 2 records each query 1 time and fail 1 time, then each succeed on their next call
        assert self.rate_checker.total_calls == 4

    def test_no_retry_bad_status(self):
        records = [{"first": "John", "last": "Doe"}] * 15
        self.request_handler.http_status = [400, 401, 402, 403, 404, 405, 408, 413, 415, 501, 502, 503, 504, 505]
        append.query_api("contact", records, query_params={"cfg_max_recs": 1},
                         headers={'Accept': 'application/json', 'x-versium-api-key': "123-456"},
                         n_retry=3,
                         queries_per_second=5,
                         n_connections=5,
                         retry_wait_time=1,
                         timeout=5)
        # Should have 4 calls. 2 records each query 1 time and fail 1 time, then each succeed on their next call
        assert self.rate_checker.total_calls == 15
