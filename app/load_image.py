"""
Serve images from file
"""

import os

from starlette.responses import FileResponse

from app import PROJECT_DIR
from app.models import Status

# Get the image directory
IMAGE_DIR = os.path.join(PROJECT_DIR, 'images')

# Map status to image filename
status_to_image = {
    Status.UP: "up.svg",
    Status.DOWN: "down.svg",
    Status.DODGY: "maybe.svg",
    Status.MAINTENANCE: "maintenance.svg",
    Status.FAILED: "failed.svg",
    Status.UNKNOWN: "unknown.svg"
}


def load_image(status: Status) -> FileResponse:
    """
    Given a service status, load
    an appropriate SVG
    """

    # Determine the appropriate image file based on the status
    image_file = status_to_image.get(status, "unknown.svg")
    image_path = os.path.join(IMAGE_DIR, image_file)

    return FileResponse(image_path, media_type='image/svg+xml')
