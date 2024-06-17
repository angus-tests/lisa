from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from app.health_check import check_health
from app.util import load_config

app = FastAPI(title="LISA")


# TODO move to models file?
# Define a model to validate service data
class Service(BaseModel):
    name: str
    description: str
    id: str
    health_check_url: HttpUrl


# Load the services yaml from file
services = load_config("config/services.yaml")


@app.get("/health/{service_id}")
async def get_service_health(service_id: str):
    """
    Fetch the health status of a service given the id of the service
    """
    service = services.get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # Extract the health_check_url field for this service and check its status
    result = check_health(service["health_check_url"])
    return {"service_name": service["name"], "health_check_result": result}


@app.get("/")
async def root():
    return {"message": "Welcome to LISA"}


