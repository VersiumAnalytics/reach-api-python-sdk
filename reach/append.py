import asyncio
import json
import logging
import urllib

import aiohttp

from .query_data import QueryResult, QueryRecord
from .rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

API_BASE_URL = "https://api.versium.com"
API_VERSION = "/v2/"


async def _fetch(session, record, query_params, path, headers):
    """Make an HTTP request to the API

    Parameters
    ----------
    session : aiohttp.ClientSession

    record : QueryRecord

    query_params : dict
        Additional query parameters to pass to the API call

    path : string
        Full path of the Versium Reach API endpoint

    headers : dict
        Additional headers to pass with the HTTP request.

    Returns
    -------
    QueryResult
    """
    if query_params is None:
        query_params = {}
    row_dict = {key: value for key, value in record.data.items() if value is not None}
    idx = record.index
    err_msg = ""
    result = QueryResult()

    params = {**query_params, **row_dict}
    response = None
    try:
        async with session.post(path, params=params, headers=headers) as response:
            result.http_status = response.status
            result.success = 200 <= result.http_status < 300
            result.reason = response.reason
            result.headers = dict(response.headers)

            if not result.success:
                err_msg = f"Unsuccessful url fetch: {result.reason}\n\tIndex: {idx}\n\tURL: {API_BASE_URL + path}?{urllib.parse.urlencode(params)}"\
                          f"\n\tResponse Status: {result.http_status}"
                result.error_msg = err_msg
                return result

            result.body_raw = await response.read()
            result.body = json.loads(result.body_raw.decode('utf-8'))

            if "errors" in result.body["versium"]:
                result.success = False

            elif result.body["versium"].get("results", []):
                result.match_found = True

            else:
                logger.debug(f"API call successful but there were no matches for record at index (starting from 0) {idx}")

    except aiohttp.ClientError as e:
        result.request_error = e
        status = getattr(response, "status", "UNKNOWN")
        err_msg = f"Error during url fetch: {e.message}\n\tIndex: {idx}\n\tURL: {path}?{urllib.parse.urlencode(params)}"\
                  f"\n\tResponse Status: {status}"
    result.error_msg = err_msg
    return result


async def _create_tasks(api, records, query_params, headers=None, *, n_retry=3, queries_per_second=20, n_connections=100, retry_wait_time=3,
                        timeout=20):
    """ Split the API calls into asynchronous tasks and wrap them in a rate limiter.

        Parameters
        ----------
        api : string
            Specifies the name of the Versium Reach API endpoint to query ('contact', 'demographic', 'b2conlineaudience', etc.)

        records : list[QueryRecord]
            List containing QueryRecord objects

        query_params : dict
            Additional query parameters to pass to each API call (e.g. {'cfg_max_recs': 1})

        headers : dict
            Additional header parameters  to pass to the API call.

        n_retry : int
            Number of times to retry the query if it fails.

        queries_per_second : int
            Maximum number of queries to perform each second to avoid 429 errors.

        n_connections : int
            Number of simultaneous calls to make when querying.

        retry_wait_time : int
            Number of seconds to wait until retrying a failed query. The wait time is increased by a multiple of `retry_wait_time` every time
            the query fails (e.g. 0, 3, 6, 9, 12, etc.)

        timeout : float
            Number of seconds to wait for the response before timing out.

        Returns
        -------
        list[dict]: List of responses from the API calls. This will be in the same order as given in the input.
        """
    tasks = []
    limit = RateLimiter(max_calls=queries_per_second,
                        period=1,
                        n_connections=n_connections,
                        n_retry=n_retry,
                        retry_wait_time=retry_wait_time)
    limited_fetch = limit(_fetch)
    path = API_VERSION + api.strip('/')

    async with aiohttp.ClientSession(base_url=API_BASE_URL, read_timeout=timeout) as session:
        for rec in records:
            task = asyncio.ensure_future(
                limited_fetch(session=session, record=rec, query_params=query_params, path=path, headers=headers))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        return await responses


def query_api(api, records, query_params, headers=None, *, n_retry=3, queries_per_second=20, n_connections=3, retry_wait_time=3,
              timeout=3):
    """ Query the Versium Reach API and return the results.

    Parameters
    ----------
    api : string
        Specifies the name of the Versium Reach API endpoint to query ('contact', 'demographic', 'b2conlineaudience', etc.)

    records : list[dict]
        List containing records as key, value pairs e.g [{'first': 'John', 'last': 'Smith'}]

    query_params : dict
        Additional query parameters to pass to each API call (e.g. {'cfg_max_recs': 1})

    headers : dict
        Additional header parameters  to pass to the API call.

    n_retry : int
        Number of times to retry the query if it fails.

    queries_per_second : int
        Maximum number of queries to perform each second to avoid 429 errors.

    n_connections : int
        Number of simultaneous calls to make when querying.

    retry_wait_time : int
        Number of seconds to wait until retrying a failed query. The wait time is increased by a multiple of `retry_wait_time` every time
        the query fails (e.g. 0, 3, 6, 9, 12, etc.)

    timeout : float
        Number of seconds to wait for the response before timing out.

    Returns
    -------
    list[dict]: List of responses from the API calls. This will be in the same order as given in the input.
    """

    if len(records) < 1:
        logger.warning("No input records were given.")
        return []

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

