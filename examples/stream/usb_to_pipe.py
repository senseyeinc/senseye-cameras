import time
from senseye_cameras import Stream

'''
Takes a usb input and pipes it out as an h264 bytestream.
The bytestream output can be intercepted by passing a callback to the output_config.
'''

SLEEP_TIME = 5
CAMERA_ID = 0
# how many bytes from the bytestream should be passed to our callback
BLOCK_SIZE = 2048


def my_callback(data):
    print(f'Got block of h264: {len(data)}')

s = Stream(
    input_type='usb', id=CAMERA_ID,
    output_type='h264_pipe', output_config={
        'callback': my_callback,
        'block_size': BLOCK_SIZE,
    },
    reading=True,
    writing=True,
)
s.start()
time.sleep(SLEEP_TIME)
s.stop()
