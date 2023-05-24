import asyncio
import logging
import time

logger = logging.getLogger(__name__)


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

        self.max_calls = max_calls
        self.period = period
        self.n_retry = n_retry
        self.retry_wait_time = retry_wait_time
        self.clock = time.monotonic
        self.last_reset = 0
        self.num_calls = 0
        self.sem = asyncio.Semaphore(n_connections)

    def __call__(self, func):
        """

        Parameters
        ----------
        func : Callable
            function that returns a QueryResult object

        Returns
        -------
        Callable: Input function wrapped with a rate limiting functionality
        """

        async def wrapper(*args, **kwargs):
            # Semaphore will block more than {self.max_connections} from happening at once.
            self.last_reset = self.clock()
            async with self.sem:
                for i in range(self.n_retry + 1):
                    while self.num_calls >= self.max_calls:
                        await asyncio.sleep(self.__period_remaining())

                    self.num_calls += 1
                    result = await func(*args, **kwargs)
                    if result.success:
                        return result

                    if (result.http_status in (429, 500)) and (self.n_retry - i > 0):
                        logger.error(result.error_msg + f"\n\tAttempts Left: {self.n_retry - i: d}")
                        await asyncio.sleep(self.retry_wait_time * i)
                        continue
                    elif self.n_retry - i <= 0:
                        logger.error(result.error_msg + f"\n\tNo attempts left.")
                    else:
                        logger.error(result.error_msg + f"\n\tNot retrying for http status: {result.http_status}")

                    return result

        return wrapper

    def __period_remaining(self):
        """ Gets the amount of time remaining in the period. If there is no time remaining, resets the call counter and updates the reset
        timer.

        Returns
        -------
        float: Amount of time remaining in this period

        """
        elapsed = self.clock() - self.last_reset
        period_remaining = self.period - elapsed
        if period_remaining <= 0:
            self.num_calls = 0
            self.last_reset = self.clock()
            period_remaining = self.period
        return max(period_remaining, 0)
