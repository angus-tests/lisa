"""
File used for checking version of a service
"""
import logging
from typing import Union

from app.config_manager import Service
from app.request import perform_async_request, AsyncResponse

logger = logging.getLogger(__name__)


async def perform_version_check(service: Service) -> Union[None, str]:
    """
    Fetch the version of a service
    :param service: The service to check the version for
    :return: version of the service, or None if the service is unavailable
    """
    logger.info(f"Checking version for service {service.id}")

    # Perform an async request to get the version from the service endpoint
    response: AsyncResponse = await perform_async_request(service.version_url, timeout_threshold=30)

    # If any error was raised log it out
    if response.error:
        logger.error(f"Failed to fetch version for {service.id} due to {response.error}")
    else:

        # Only extract the version for a successful request
        if response.status_code == 200:
            version = response.body.get('version')
            logger.info(f"Version for service {service.id}: {version}")
            return version
        else:
            logger.error(f"Failed to fetch version for {service.id}, HTTP status {response.status_code}")

