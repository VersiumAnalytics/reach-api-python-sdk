import logging

from reach import ReachClient
from .base import BaseTestCase

logging.basicConfig(level=logging.INFO)


class TestReachClient(BaseTestCase):
    async def setUpAsync(self):
        await super().setUpAsync()
        # Need to create the ReachClient after the append module has been patched
        self.reach_client = ReachClient('123-abc-def-456')

    def test_correct_params(self):
        records = [{"first": "John", "last": "Doe"}] * 3
        self.reach_client.append('contact', records, ['demographic'])
        q_string = self.request_handler.requests[0].query_string
        assert ('cfg_max_recs=1' in q_string) and ('rcfg_max_time' in q_string)
