import time
from senseye_cameras import Stream

s = Stream(
    input_type='ffmpeg', id=0,
    output_type='ffmpeg', path='./tmp/usb.yuv', output_config = {
                'fps': 80,
                'pixel_format': 'rgb24',
                'format': 'rawvideo',
                # 'res': (1224,1024),
            },
    reading=True,
    writing=True,
)
s.start()

time.sleep(5)

s.stop()
