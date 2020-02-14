import time
from senseye_cameras import Stream

'''
Example pyueye stream.
'''

SLEEP_TIME = 5
CAMERA_ID = 0
FILE_PATH = './tmp/usb.mkv'

s = Stream(
    input_type='ueye', id=CAMERA_ID, input_config={
        'fps': 60,
        'exposure': 60,
        'autofocus': 1,
        'autogain': 1,
    },
    output_type='file', path=FILE_PATH,
    reading=True,
    writing=True,
)
s.start()

time.sleep(SLEEP_TIME)

s.stop()
