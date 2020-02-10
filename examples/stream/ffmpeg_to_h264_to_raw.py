import time
from senseye_cameras import Stream

s = Stream(
    input_type='ffmpeg', id=0, input_config={
        # 'output_format': 'h264',
    },
    output_type='ffmpeg', path='./tmp/usb.yuv',
    reading=True,
    writing=True,
)
s.start()

time.sleep(10)

s.stop()
