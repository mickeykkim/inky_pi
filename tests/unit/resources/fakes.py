"""
Test double fake classes
"""
from typing import Optional


class FakeResponse:
    """Fake response object for use in returning fake json data

    See FakeRequests class for more info
    """

    def __init__(self, json_data: dict, status_code: int) -> None:
        """Initialize fake response object

        Args:
            json_data (dict): json data to return
            status_code (str): status code to return
        """
        self.json_data: dict = json_data
        self.status_code: int = status_code

    def json(self) -> dict:
        """Return json data as a dictionary"""
        return self.json_data


class FakeRequests:
    """Fake requests object. Used to mock requests.get() in tests.

    Usage:
    >>> import json
    >>> file_name = "your_file.json"
    >>> requests = FakeRequests()
    >>> with open(file_name, "r", encoding="utf-8") as file:
    >>>     test_data = json.load(file)
    >>>     requests.add_response(test_data, 200)
    >>> response = requests.get("https://www.example.com")
    >>> assert response ...
    """

    def __init__(self) -> None:
        """Initialize fake requests object"""
        self.response: Optional[FakeResponse] = None

    def add_response(self, json_data: dict, status_code: int) -> None:
        """Set fake response

        Args:
            json_data (dict): json data
            status_code (str): status code
        """
        self.response = FakeResponse(json_data, status_code)

    # pylint: disable=unused-argument
    def get(self, url: str, params: dict = None) -> Optional[FakeResponse]:
        """Fake get method

        Args:
            url (str): url
            params (dict): params
        """
        assert url is not None
        assert self.response is not None
        return self.response
