from fastapi import FastAPI, HTTPException

from app.config_manager import ConfigManager, Service
from app.health_check import check_health

app = FastAPI(title="LISA")
config_manager = ConfigManager("config/services.yaml")


@app.get("/health/{service_id}")
async def get_service_health(service_id: str):
    """
    Fetch the health status of a service given the id of the service
    """

    service: Service = config_manager.get_service_by_id(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # Extract the health_check_url field for this service and check its status
    status = check_health(service.health_check_url)
    return {"service_name": service.id, "status": status}


@app.get("/")
async def root():
    return {"message": "Welcome to LISA"}


