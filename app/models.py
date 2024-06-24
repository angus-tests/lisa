from enum import Enum, auto

from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Status(Enum):
    UP = auto()           # App is up and running normally
    DOWN = auto()         # App is not responding to health check
    DODGY = auto()        # App took a long time to respond
    UNKNOWN = auto()      # Status is unknown (not yet checked status)
    MAINTENANCE = auto()  # App is down for planned maintenance
    FAILED = auto()       # An error occurred checking the health


class Service(BaseModel):
    id: str
    name: str
    description: str
    health_check_url: str
    version_url: str
