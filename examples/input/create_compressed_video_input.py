import inspect
from pathlib import Path
from senseye_cameras import create_input

# get the path to the sample compressed video in the tests/resources folder
video = str(
    Path(
        Path(inspect.getfile(inspect.currentframe())).parents[2].absolute(),
        'tests/resources/usb_video.mp4'
    )
)

# initialize and open a usb camera
camera = create_input(type='usb', id=video, config={'res': (1920, 1080)})

camera.open()
frame, timestamp = camera.read()

print(frame)
