"""
File used for checking health of services
"""
from typing import Dict

import requests
from fastapi import HTTPException
from requests.exceptions import RequestException
from app.config_manager import Status, Service
from aiohttp import ClientSession, ClientError


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


async def perform_health_check(service: Service, manager: HealthStatusManager):
    """
    Asynchronously ping a given endpoint to see if it is healthy, then store
    the health status of the service in the Health Status Manager
    :param service: The service to check
    :param manager: The HealthStatus manager to store the health status in
    """
    print(f"Starting health check for service {service.id}")
    async with ClientSession() as session:
        try:
            async with session.get(service.health_check_url) as response:
                if response.status == 200:
                    manager.update_status(service.id, Status.UP)
                elif response.status == 503:
                    manager.update_status(service.id, Status.MAINTENANCE)
                else:
                    manager.update_status(service.id, Status.DOWN)
            print(f"Health check for {service.name} [ID: {service.id}]: {manager.get_status(service.id).name}")
        except ClientError as e:
            manager.update_status(service.id, Status.FAILED)
            print(f"Failed to perform health check for {service.name} [ID: {service.id}]: {str(e)}")

