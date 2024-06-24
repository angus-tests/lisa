"""
Responsible for loading and managing configuration from the config directory
"""

import yaml
from typing import Dict
from fastapi import HTTPException

from app.models import Service


class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.services = self.load_config()

    def load_config(self) -> Dict[str, Service]:
        """
        Load services in a dict, [service_id -> Service]
        :return:
        """
        with open(self.config_path, 'r') as file:
            config_data = yaml.safe_load(file)
            return {service['id']: Service(**service) for service in config_data['services']}

    def get_service_by_id(self, service_id: str) -> Service:
        service = self.services.get(service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        return service
