# LISA

Logging, information & system analysis

## App structure
```
/LISA
|-- app/
    |-- __init__.py
    |-- config_manager.py  # For loading config from file
    |-- health_checker.py  # For performing health checks
    |-- load_image.py      # Loading badges
    |-- main.py            # Entry point of the FastAPI application
|-- config/
    |-- services.yaml      # A list of services to monitor
|-- images/                # Directory of images
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

## Badges

The status of services can be returned as SVG badges, using the endpoint `"/badge/{service_id}"`

<table style="width:100%;">
    <tr>
        <th>Status</th>
        <th>Description</th>
        <th>Badge Image</th>
    </tr>
    <tr>
        <td>UP</td>
        <td>The service is operating normally.</td>
        <td><img src="/images/up.svg" alt="UP Badge"></td>
    </tr>
    <tr>
        <td>DOWN</td>
        <td>The service is not reachable.</td>
        <td><img src="/images/down.svg" alt="DOWN Badge"></td>
    </tr>
    <tr>
        <td>DODGY</td>
        <td>The service is taking longer than usual to respond</td>
        <td><img src="/images/maybe.svg" alt="DODGY Badge"></td>
    </tr>
    <tr>
        <td>MAINTENANCE</td>
        <td>The service is under maintenance.</td>
        <td><img src="/images/maintenance.svg" alt="Maintenance Badge"></td>
    </tr>
    <tr>
        <td>FAILED</td>
        <td>The service check failed.</td>
        <td><img src="/images/failed.svg" alt="Failed Badge"></td>
    </tr>
    <tr>
        <td>UNKNOWN</td>
        <td>Status is not determined.</td>
        <td><img src="/images/unknown.svg" alt="Unknown Badge"></td>
    </tr>
</table>