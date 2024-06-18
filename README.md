# LISA

Logging, information & system analysis

## App structure
```
/LISA
|-- app/
    |-- __init__.py
    |-- config_manager.py  # For loading config from file
    |-- health_checker.py  # For performing health checks
    |-- main.py            # Entry point of the FastAPI application
    |-- util.py            # Various utility functions
    
```

## Services.yaml

The `config/services.yaml` file is used to define services that LISA should monitor. The structure of the file is explained below...

```yaml

microservices:
  - name: User Service  # The display name of the microservice
    id: user_service # Unique slug for the service
    description: Handles user data and authentication  # Brief description of the service
    health_check_url: http://user-service/health  # URL to check the health of the service
```