"""
File used for checking health of services
"""
import asyncio
import logging
from typing import Dict

from fastapi import HTTPException
from app.config_manager import Status, Service
from aiohttp import ClientSession, ClientError, ClientTimeout

logger = logging.getLogger(__name__)


class HealthStatusManager:
    """
    A HealthStatus manager stores
    the health status of services in memory
    to reduce strain on service endpoints and increase
    api response time
    """
    def __init__(self):
        self._statuses: Dict[str, Status] = {}

    def initialize_statuses(self, services):
        """
        Set all initial services to unknown
        to avoid 404 for existing services
        """
        for service in services:
            self._statuses[service.id] = Status.UNKNOWN  # or any default status

    def update_status(self, service_id: str, status: Status):
        self._statuses[service_id] = status

    def get_status(self, service_id: str) -> Status:
        try:
            return self._statuses[service_id]
        except KeyError:
            raise HTTPException(status_code=404, detail="Status not found for the specified service ID")


async def perform_health_check(service: Service, manager: HealthStatusManager,
                               response_time_threshold: int = 5, timeout_threshold: int = 30):
    """
    Asynchronously ping a given endpoint to see if it is healthy, then store
    the health status of the service in the Health Status Manager
    :param service: The service to check
    :param manager: The HealthStatus manager to store the health status in
    :param response_time_threshold Maximum amount of time to be considered a healthy service
    :param timeout_threshold Any service taking longer than this will be considered DOWN, a service inbetween the
    threshold and the timeout will be considered DODGY
    """
    logger.info(f"Starting health check for service {service.id}")
    async with ClientSession() as session:
        try:
            # Set a timeout for the HTTP request
            timeout = ClientTimeout(total=timeout_threshold)
            start_time = asyncio.get_event_loop().time()

            # Start a request to the health point URL
            async with session.get(service.health_check_url, timeout=timeout) as response:

                # Get the elapsed time
                elapsed = asyncio.get_event_loop().time() - start_time
                logger.info(f"Response time for {service.id}: {elapsed:.2f} seconds")

                # If we get a normal OK status from the endpoint
                if response.status == 200:

                    # A response is considered DODGY if it's longer than the response_time_threshold but shorter than
                    # the timeout
                    if elapsed > response_time_threshold:
                        manager.update_status(service.id, Status.DODGY)

                    # Otherwise the service is operating normally
                    else:
                        manager.update_status(service.id, Status.UP)

                # A 503 status means the service is down for maintenance
                elif response.status == 503:
                    manager.update_status(service.id, Status.MAINTENANCE)

                # Any other status code we assume the application is down
                else:
                    manager.update_status(service.id, Status.DOWN)
        except asyncio.TimeoutError:
            # If a timeout error is thrown, we assume the service is down
            logger.error(f"Timeout while trying to reach {service.id}")
            manager.update_status(service.id, Status.DOWN)
        except ClientError as e:

            # If a general exception is thrown we set to FAILED as we cannot confirm it is the client
            logger.error(f"Failed to perform health check for {service.name} [ID: {service.id}]: {str(e)}")
            manager.update_status(service.id, Status.FAILED)