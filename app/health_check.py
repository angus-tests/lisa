"""
File used for checking health of services
"""
import requests
from requests.exceptions import RequestException


def check_health(url: str) -> dict:
    """
    Ping a given endpoint to see if it is healthy
    :param url: The health check URL
    :return: Status dictionary, must contain "status" key
    """

    # TODO implement cache
    try:
        response = requests.get(url)
        return {'status': response.status_code, 'body': response.text}
    except RequestException as e:
        return {'status': 'failed', 'reason': str(e)}
