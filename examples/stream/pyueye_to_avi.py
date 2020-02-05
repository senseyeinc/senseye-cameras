import time
from senseye_cameras import Stream

s = Stream(
    input_type='ueye', id=0,
    output_type='ffmpeg', path='./tmp/usb.mp4', output_config = {
                'fps': 80,
                'pixel_format': 'gray',
                'format': 'rawvideo',
                'res': (3088,2076),
            },
    reading=True,
    writing=True,
)
s.start()

time.sleep(3)

s.stop()
