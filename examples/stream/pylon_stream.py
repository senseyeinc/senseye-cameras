import time
from senseye_cameras import Stream

'''
Example pylon stream.
'''

SLEEP_TIME = 5
CAMERA_ID = 0
FILE_PATH = './tmp/usb.mkv'

s = Stream(
    input_type='pylon', id=CAMERA_ID,

    output_type='file',
    output_config = {
        'fps': 80,
    },
    path='./tmp/usb.mkv',

    reading=True,
)
s.start()

time.sleep(2)

s.start_writing()

time.sleep(10)

s.stop()
