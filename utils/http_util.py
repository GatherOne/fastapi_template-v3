import threading
import requests
from tenacity import stop_after_attempt, wait_fixed, retry


class RequestsUtil:
    _instance_lock = threading.Lock()

    def __init__(self, max_retries=3, backoff_factor=1, status_forcelist=(500, 502, 504)):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist

    def __new__(cls, *args, **kwargs):
        if not hasattr(RequestsUtil, "_instance"):
            with RequestsUtil._instance_lock:
                if not hasattr(RequestsUtil, "_instance"):
                    RequestsUtil._instance = object.__new__(cls)
        return RequestsUtil._instance

    @retry(stop=stop_after_attempt(3),
           wait=wait_fixed(1),
           reraise=True,
           retry_error_callback=lambda retry_state: print(f"Failed after {retry_state.attempt_number} attempts"))
    def send_request(self, method, url, **kwargs):
        """
        Send an HTTP request with retries.

        :param method: HTTP method to use.
        :param url: URL for the request.
        :param kwargs: Optional arguments that `requests.request` takes.
        :return: Response object.
        """
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx).
        return response

    def get(self, url, **kwargs):
        return self.send_request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.send_request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self.send_request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.send_request('DELETE', url, **kwargs)
