"""
File used for checking health of services
"""
import requests
from requests.exceptions import RequestException

from app.config_manager import Status


def check_health(url: str) -> Status:
    """
    Ping a given endpoint to see if it is healthy
    :param url: The health check URL
    :return: Status dictionary, must contain "status" key
    """

    # TODO implement cache
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Status.UP
        elif response.status_code == 503:
            return Status.MAINTENANCE
        else:
            return Status.DOWN
    except RequestException:
        return Status.FAILED
