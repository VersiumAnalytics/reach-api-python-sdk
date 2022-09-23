from .append import query_api


class ReachClient:
    f"""Client for querying Versium Reach APIs

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

    n_retry : int (default 3)
        Number of times to retry a query if it fails.

    retry_wait_time : int (default 3)
        Number of seconds to wait until retrying a failed query. The wait time is increased by a multiple of `retry_wait_time` every time
        the query fails (e.g. 0, 3, 6, 9, 12, etc.)

    timeout : int (default 20)
        Number of seconds to wait for a response before timing out.
    """

    def __init__(self, api_key, *, queries_per_second=20, n_connections=100, timeout=20, retry_wait_time=3, n_retry=3):

        self.headers = {'Accept': 'application/json', 'x-versium-api-key': api_key}
        self.queries_per_second = queries_per_second
        self.n_connections = n_connections
        self.timeout = timeout
        self.n_retry = n_retry
        self.retry_wait_time = retry_wait_time

    def _append(self, api_name, input_records, outputs=(), config_params=None):
        f"""Perform an append on the input records and return the results.

        Parameters
        ----------
        api_name : string
            Name of the api you wish to use.
        input_records : list[dict]
            Input records to query. Each record should be a dict with `input_param_name: value` pairs. For the names of input parameters, 
            see the input section of https://api-documentation.versium.com/reference/common-api-inputs-and-options
        outputs : list[str]
            Desired output from the api. Each string in the list must be a recognized output type keyword. The recognized output type keywords
            will depend on the API, so check the documentation for the specific API you are using.
        config_params: dict
            Configuration parameters to pass to each API call. See the Configuration Parameters section of https://api-documentation.versium.com/reference/common-api-inputs-and-options

        Returns
        -------
        dict: The results of the api query in JSON.
            See https://api-documentation.versium.com/reference/common-outputs for an example output.
        """
        query_params = dict()
        if config_params is None:
            config_params = dict()

        query_params.update(config_params)

        query_params["output[]"] = list(set(outputs))  # remove duplicate outputs

        return query_api(api_name, input_records, query_params, headers=self.headers, queries_per_second=self.queries_per_second,
                         n_connections=self.n_connections, timeout=self.timeout, retry_wait_time=self.retry_wait_time,
                         n_retry=self.n_retry)

    def contact(self, input_records, outputs=("address", "phone", "email"), config_params=None):
        f"""Perform a contact append on the input records and return the results.

        Parameters
        ----------
        input_records : list[dict]
            Input records to query. Each record should be a dict with `input_param_name: value` pairs.
        outputs : list[str] ('address', 'phone', 'phone_mobile', 'phone_mutliple', 'email')
            Desired output from the API. Each string in the list must be one of the recognized output type keywords as listed above.
        config_params: dict
            Configuration parameters to pass to each API call.

        Returns
        -------
        dict: The results of the api query in JSON.
        
        See https://api-documentation.versium.com/reference/contact-append-api for more info.
        """
        return self._append(api_name="contact", input_records=input_records, outputs=outputs, config_params=config_params)

    def demographic(self, input_records, outputs=("demographic", "lifestyle", "financial", "political"), config_params=None):
        f"""Perform a demographic append on the input records and return the results.

        Parameters
        ----------
        input_records : list[dict]
            Input records to query. Each record should be a dict with `input_param_name: value` pairs.
        outputs : list[str] ('demographic', 'lifestyle', 'financial', 'political'')
            Desired output from the API. Each string in the list must be one of the recognized output type keywords as listed above.
        config_params: dict
            Configuration parameters to pass to each API call.

        Returns
        -------
        dict: The results of the api query in JSON.
            
        See https://api-documentation.versium.com/reference/demographic-append-api for more info.
        """
        return self._append(api_name="demographic", input_records=input_records, outputs=outputs, config_params=config_params)

    def b2c_online_audience(self, input_records,  config_params=None):
        f"""Perform a business to consumer online audience append on the input records and return the results.

        Parameters
        ----------
        input_records : list[dict]
            Input records to query. Each record should be a dict with `input_param_name: value` pairs. 
        config_params: dict
            Configuration parameters to pass to each API call.

        Returns
        -------
        dict: The results of the api query in JSON.
    
        See https://api-documentation.versium.com/reference/online-audience-append for more info.
        """
        return self._append(api_name="b2cOnlineAudience", input_records=input_records, config_params=config_params)

    def b2b_online_audience(self, input_records, config_params=None):
        f"""Perform a business to business online audience append on the input records and return the results.

        Parameters
        ----------
        input_records : list[dict]
            Input records to query. Each record should be a dict with `input_param_name: value` pairs. 
        config_params: dict
            Configuration parameters to pass to each API call.

        Returns
        -------
        dict: The results of the api query in JSON.

        See https://api-documentation.versium.com/reference/online-audience-append for more info.
        """
        return self._append(api_name="b2bOnlineAudience", input_records=input_records, config_params=config_params)

    def firmographic(self, input_records, config_params=None):
        f"""Perform a firmographic append on the input records and return the results.

        Parameters
        ----------
        input_records : list[dict]
            Input records to query. Each record should be a dict with `input_param_name: value` pairs. 
        config_params: dict
            Configuration parameters to pass to each API call.

        Returns
        -------
        dict: The results of the api query in JSON.

        See https://api-documentation.versium.com/reference/firmographic-api for more info.
        """
        return self._append(api_name="firmographic", input_records=input_records, config_params=config_params)

    def c2b(self, input_records, config_params=None):
        f"""Perform a consumer to business append on the input records and return the results.

        Parameters
        ----------
        input_records : list[dict]
            Input records to query. Each record should be a dict with `input_param_name: value` pairs. 
        config_params: dict
            Configuration parameters to pass to each API call.

        Returns
        -------
        dict: The results of the api query in JSON.

        See https://api-documentation.versium.com/reference/consumer-to-business-append-api for more info.
        """
        return self._append(api_name="c2b", input_records=input_records, config_params=config_params)

    def ip_to_domain(self, input_records, config_params=None):
        f"""Perform an IP to domain append on the input records and return the results.

        Parameters
        ----------
        input_records : list[dict]
            Input records to query. Each record should be a dict with `input_param_name: value` pairs. 
        config_params: dict
            Configuration parameters to pass to each API call.

        Returns
        -------
        dict: The results of the api query in JSON.

        See https://api-documentation.versium.com/reference/ip-to-domain for more info.
        """
        return self._append(api_name="iptodomain", input_records=input_records, config_params=config_params)

    def hem_to_business_domain(self, input_records, config_params=None):
        f"""Perform a hashed email to business domain append on the input records and return the results.

        Parameters
        ----------
        input_records : list[dict]
            Input records to query. Each record should be a dict with `input_param_name: value` pairs. 
        config_params: dict
            Configuration parameters to pass to each API call.

        Returns
        -------
        dict: The results of the api query in JSON.

        See https://api-documentation.versium.com/reference/hem-to-business-domain for more info.
        """
        return self._append(api_name="hemtobusinessdomain", input_records=input_records, config_params=config_params)
