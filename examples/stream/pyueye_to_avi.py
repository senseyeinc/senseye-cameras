import time
from senseye_cameras import Stream

s = Stream(
    input_type='ueye', id=0,
    output_type='raw', path='./tmp/usb.raw',
    reading=True,
    writing=False,
)
s.start()

time.sleep(100)

s.stop()
