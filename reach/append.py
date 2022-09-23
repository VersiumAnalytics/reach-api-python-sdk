import asyncio
import logging
import time
import urllib
from collections import namedtuple
import aiohttp

logger = logging.getLogger(__name__)

QUERIES_PER_SECOND_HARD_CAP = 100

QueryResult = namedtuple('QueryResult', ['result', 'success', 'match'], defaults=(None, False, False))
QueryRecord = namedtuple('QueryRecord', ['data', 'index'])

API_BASE_URL = "https://api.versium.com/v2/"

REACH_APIS = ("contact", "demographic", "b2cOnlineAudience", "b2bOnlineAudience", "firmographic", "c2b", "iptodomain", "hemtobusinessdomain")


class QueryError(RuntimeError):
    """Exception class for errors that occur when querying the Reach API
    """
    pass


class RateLimiter(object):
    """ Limits the number of calls to a function within a timeframe. Also limits the number of total active function calls.

            Parameters
            ----------
            max_calls : int
                Maximum number of function calls to make within a time period.
            period : float
                Length of time period in seconds.
            n_connections : int
                Maximum number of total active function calls to allow. Once this limit is reached, no more function calls will be made until an
                active call returns.
            n_retry : int
                Number of times to retry a function call until it succeeds.
            retry_wait_time : float
                Number of seconds to wait between retries. The wait time will increase by a factor of `retry_wait_time` everytime the call
                fails. For example, if `retry_wait_time`=3, then it will wait 0 seconds on the first retry, 3 seconds on the second retry,
                6 seconds on the third retry, etc.
        """

    def __init__(self, *, max_calls=20, period=1, n_connections=100, n_retry=3, retry_wait_time=2):

        if (max_calls // period) > QUERIES_PER_SECOND_HARD_CAP:
            raise ValueError(f"The maximum queries per second allowed is {QUERIES_PER_SECOND_HARD_CAP}. Instead got "
                             f"{max_calls / period:.2f} queries per second.")

        self.max_calls = max_calls
        self.period = period
        self.n_retry = n_retry
        self.retry_wait_time = retry_wait_time
        self.clock = time.monotonic
        self.last_reset = 0
        self.num_calls = 0
        self.sem = asyncio.Semaphore(n_connections)

    def __call__(self, func):

        async def wrapper(*args, **kwargs):
            # Semaphore will block more than {self.max_connections} from happening at once.
            self.last_reset = self.clock()
            async with self.sem:
                for i in range(self.n_retry + 1):
                    while self.num_calls >= self.max_calls:
                        await asyncio.sleep(self.__period_remaining())

                    try:
                        self.num_calls += 1
                        result = await func(*args, attempts_left=self.n_retry - i, **kwargs)
                        return result

                    except QueryError:
                        if self.n_retry - i > 0:
                            await asyncio.sleep(self.retry_wait_time * i)
                # Failed to perform the query after n_retry attempts. Return empty responses
                return QueryResult(None, False, False)

        return wrapper

    def __period_remaining(self):
        elapsed = self.clock() - self.last_reset
        period_remaining = self.period - elapsed
        if period_remaining <= 0:
            self.num_calls = 0
            self.last_reset = self.clock()
            period_remaining = self.period
        return max(period_remaining, 0)


async def _fetch(session, record, query_params, api, headers, attempts_left):
    """Internal fetch method."""
    if query_params is None:
        query_params = {}
    row_dict = {key: value for key, value in record.data.items() if value is not None}
    idx = record.index

    params = {**query_params, **row_dict}
    response = None
    try:
        async with session.post(api, params=params, headers=headers) as response:
            response.raise_for_status()  # raise error if bad http status
            body = await response.json(content_type=None)  # get json representation of responses

            if "errors" in body["versium"]:
                raise QueryError(f"Received error response from REACH API: {body['versium']['errors']}")

            elif body["versium"].get("results", []):
                result = QueryResult(body, success=True, match=True)

            else:
                logger.debug(f"API call successful but there were no matches for record at index (starting from 0) {idx}")
                result = QueryResult(result={}, success=True, match=False)

            return result

    except aiohttp.ClientError as e:
        status = getattr(response, "status", "UNKNOWN")
        logger.error(f"Error during api fetch: {e}\n\tIndex: {idx}\n\tURL: {session.make_url(api)}?{urllib.parse.urlencode(params)}"
                     f"\n\tResponse Status: {status}\n\tAttempts Left: {attempts_left:d}")
        # Use a different error class so that we only catch errors from making the http request
        raise QueryError("Failed to fetch api.")


async def _create_tasks(api, records, query_params, headers=None, *, queries_per_second=20, n_connections=100, timeout=20, n_retry=3,
                        retry_wait_time=3):
    tasks = []
    limit = RateLimiter(max_calls=queries_per_second,
                        period=1,
                        n_connections=n_connections,
                        n_retry=n_retry,
                        retry_wait_time=retry_wait_time)
    limited_fetch = limit(_fetch)

    async with aiohttp.ClientSession(base_url=API_BASE_URL, read_timeout=timeout) as session:
        for rec in records:
            task = asyncio.ensure_future(
                limited_fetch(session=session, record=rec, query_params=query_params, api=api, headers=headers))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        return await responses


def query_api(api, records, query_params, headers=None, *, n_retry=3, queries_per_second=20, n_connections=3, retry_wait_time=3,
              timeout=3):

    # Check that appropriate api name was passed
    for valid_api in REACH_APIS:
        if api.lower().strip() == valid_api.lower().strip():
            api = valid_api

    if api is None:
        raise ValueError(f"Got `api` {api}. Valid api names are: {REACH_APIS}")

    records = [QueryRecord(rec, i) for i, rec in enumerate(records)]
    logger.info(f'Started querying {len(records)} records')
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(_create_tasks(api=api,
                                                 records=records,
                                                 query_params=query_params,
                                                 headers=headers,
                                                 timeout=timeout,
                                                 retry_wait_time=retry_wait_time,
                                                 n_retry=n_retry,
                                                 queries_per_second=queries_per_second,
                                                 n_connections=n_connections))
    try:
        responses = loop.run_until_complete(future)

    except KeyboardInterrupt:
        # Canceling pending tasks and stopping the loop.
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        loop.stop()

        raise KeyboardInterrupt
    return responses

