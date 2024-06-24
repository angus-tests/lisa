import asyncio
from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import Json
from starlette.responses import FileResponse

from app.auth import authenticate_user, get_current_active_user
from app.config_manager import ConfigManager
from app.health_check import perform_health_check, HealthStatusManager
from app.load_image import load_image
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.models import User, Token, fake_users_db
from app.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI(title="LISA")
config_manager = ConfigManager("config/services.yaml")
scheduler = AsyncIOScheduler()
status_manager = HealthStatusManager()


# -------------- Dependencies -------------
def get_status_manager():
    """
    Tiny helper function used to retrieve an instance
    of the health status manager. For use with FastAPI dependency injection
    """
    return status_manager

# -------------- Endpoints -------------


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    Get an authentication token
    :param form_data:
    :return:
    """

    # Attempt to fetch this user
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)

    # If the user is not found, throw an error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate and return a new token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user


@app.get("/health/{service_id}")
async def get_service_health(
        service_id: str,
        manager: Annotated[HealthStatusManager, Depends(get_status_manager)]
) -> Json:
    """
    Fetch the health status of a service
    :param service_id: The ID of the service
    :param manager: An instance of a health status manager to fetch status' from
    """
    return {"service_id": service_id, "status": manager.get_status(service_id).name}


@app.get("/badge/{service_id}")
async def get_service_badge(
        service_id: str,
        manager: Annotated[HealthStatusManager, Depends(get_status_manager)]
) -> FileResponse:
    """
    Generate an SVG badge which indicates the status
    of this service
    :param service_id: The ID of the service to get the badge of
    :param manager: An instance of a health status manager to fetch status' from
    """
    return load_image(manager.get_status(service_id))


@app.get("/version/{service_id}")
async def get_service_version(
        service_id: str,
        manager: Annotated[HealthStatusManager, Depends(get_status_manager)]
) -> Json:
    """
    Get the current version of a service
    :param service_id: The ID of the service to get the badge of
    :param manager: An instance of a health status manager to fetch status' from
    """
    pass


@app.get("/")
async def root():
    return {"message": "Welcome to LISA"}


# -------------- Schedules -----------------
@app.on_event("startup")
async def start_scheduler():

    # Initialize the status of all services on startup
    status_manager.initialize_statuses(config_manager.services.values())

    # Run the initial health checks asynchronously
    await perform_periodic_health_checks()

    # Start the schedule
    scheduler.start()

    # Every five minutes ping all the apps
    scheduler.add_job(perform_periodic_health_checks, 'interval', minutes=5)


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()


async def perform_periodic_health_checks():
    """
    Periodically check all the services, instead of doing it ONLY when we get an API request.
    """

    # Check the health of all services asynchronously to avoid waiting for unresponsive apps
    tasks = []
    for service in config_manager.services.values():
        task = asyncio.create_task(perform_health_check(service, status_manager))
        tasks.append(task)
    await asyncio.gather(*tasks)


