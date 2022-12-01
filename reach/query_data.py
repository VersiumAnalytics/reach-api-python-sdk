
class QueryRecord:
    """Data structure representing an input record for a query.

    Parameters
    ----------
    data : dict
        Dictionary of `input_param_name: value` pairs.

    index : int
        Index of the record
    """

    def __init__(self, data, index):
        self.data = data
        self.index = index


class QueryResult:
    """Data structure to the output from an append hold results from a

    Parameters
    ----------
    body : dict
        The parsed body of the response from the Versium Reach API.

    success : bool
        Indicates whether the request returned with a successful status code.

    match_found : bool
        Indicates whether a match was found for the queried record

    http_status: int
        The http status code for the response.

    reason: str
        Explanation of the http status code (e.g. 200 => "OK", 404 => "Not Found", 401 => "Unauthorized", etc.)

    headers: dict
        The headers of the response.

    body_raw: bytes
        The body of the response as raw bytes

    request_error: aiohttp.ClientError
        If the client errored out during a request, this stores the error object
    """

    def __init__(self, body=None, success=False, match_found=False, *, http_status=None, reason=None, headers=None,
                 body_raw=None, request_error=None):
        if body is None:
            body = {}
        self.body = body
        self.success = success
        self.match_found = match_found
        self.http_status = http_status
        self.headers = headers
        self.body = body
        self.body_raw = body_raw
        self.request_error = request_error
        self.reason = reason

    def __repr__(self):
        headers = str(self.headers)
        if len(headers) > 60:
            headers = headers[:60] + '...'

        body = str(self.body)
        if len(body) > 60:
            body = body[:60] + '...'

        output = f"success={self.success}, match_found={self.match_found}, http_status={self.http_status}, reason={self.reason}," \
                 f" headers={headers}, body={body}, request_error={self.request_error}"
        return self.__class__.__name__ + '(' + output + ')'


