from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="Microservices Health Monitor")


# Define a model to validate your service data (optional)
class Service(BaseModel):
    name: str
    health_check_url: HttpUrl


# Mocked services dictionary
services = {
    "1": Service(name="SDX Transformer", health_check_url="http://example.com/health"),
    "2": Service(name="SDX Survey", health_check_url="http://example2.com/health")
}


@app.get("/health/{service_id}")
async def get_service_health(service_id: str):
    service = services.get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    try:
        response = requests.get(service.health_check_url)
        return {"service_name": service.name, "status": response.status_code}
    except requests.RequestException as e:
        return {"service_name": service.name, "status": "unreachable", "reason": str(e)}

@app.get("/")
async def root():
    return {"message": "Welcome to LISA"}


