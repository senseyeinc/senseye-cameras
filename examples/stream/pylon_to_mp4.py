import time
from senseye_cameras import Stream

s = Stream(
    input_type='pylon', id=0,
    output_type='ffmpeg', path='./tmp/usb.mp4', output_config = {
                'fps': 80,
                'pixel_format': 'gray',
                'format': 'rawvideo',
                'res': (1224,1024),
            },
    reading=True,
)
s.start()

time.sleep(2)

s.start_writing()

time.sleep(10)

s.stop()
