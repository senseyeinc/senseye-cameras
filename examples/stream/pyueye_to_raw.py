import time
from senseye_cameras import Stream

s = Stream(
    input_type='ueye', id=0,
    output_type='raw', path='./tmp/ueye.raw',
    reading=True,
    writing=True,
)
s.start()

time.sleep(10)

s.stop()
