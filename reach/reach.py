from .append import query_api
import logging

logger = logging.getLogger(__name__)


class ReachClient:
    """Client for querying Versium Reach APIs

    Parameters
    ----------
    api_key : string
        Versium Reach API key. To get an API key see https://api-documentation.versium.com/docs/start-building-with-versium

    queries_per_second : int (default 20)
        Number of queries to perform each second. By default, Versium APIs have a limit of 20 QPS. Only change this if you know that your
        rate limit has been increased.

    n_connections : int (default 100)
        Number of simultaneous connections to allow while querying. The client will keep performing queries at the `queries_per_second` rate
        limit until there are `n_connections` active queries waiting for a response.

    timeout : int (default 20)
        Number of seconds to wait for a response before timing out.

    retry_wait_time : int (default 3)
        Number of seconds to wait until retrying a failed query. The wait time is increased by a multiple of `retry_wait_time` every time
        the query fails (e.g. 0, 3, 6, 9, 12, etc.)

    n_retry : int (default 3)
        Number of times to retry a query if it fails.
    """

    def __init__(self, api_key, *, queries_per_second=20, n_connections=100, timeout=20, retry_wait_time=3, n_retry=3):

        self.headers = {'Accept': 'application/json', 'x-versium-api-key': api_key}
        self.queries_per_second = queries_per_second
        self.n_connections = n_connections
        self.timeout = timeout
        self.n_retry = n_retry
        self.retry_wait_time = retry_wait_time

    def append(self, api_name, input_records, outputs=(), config_params=None):
        """Perform an append on the input records and return the results.

        Parameters
        ----------
        api_name : string
            Name of the api you wish to use (e.g. 'contact', 'demographic', 'firmographic', etc.).

        input_records : list[dict]
            Input records to query. Each record should be a dict with `input_param_name: value` pairs. For the names of input parameters, 
            see the input section of https://api-documentation.versium.com/reference/common-api-inputs-and-options

        outputs : list[str]
            Desired output from the path. Each string in the list must be a recognized output type keyword. The recognized output type keywords
            will depend on the API, so check the documentation for the specific API you are using.

        config_params: dict
            Configuration parameters to pass to each API call. See the Configuration Parameters section of https://api-documentation.versium.com/reference/common-api-inputs-and-options

        Returns
        -------
        list[QueryResult]: A list of QueryResult objects
        """
        query_params = dict()
        if config_params is None:
            config_params = dict()

        query_params.update(config_params)

        query_params["output[]"] = list(set(outputs))  # remove duplicate outputs

        logger.info(f"Reach API set to {api_name}.")
        logger.info(f"API outputs set to {outputs}.")
        logger.info(f"API config params set to {config_params}")

        return query_api(api_name, input_records, query_params, headers=self.headers, queries_per_second=self.queries_per_second,
                         n_connections=self.n_connections, timeout=self.timeout, retry_wait_time=self.retry_wait_time,
                         n_retry=self.n_retry)
