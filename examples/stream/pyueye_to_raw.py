import time
from senseye_cameras import Stream

s = Stream(
    input_type='ueye', id=0, input_config={
        'fps': 60,
        'exposure': 60,
        'autofocus': 1,
        'autogain': 1,
    },
    output_type='raw', path='./tmp/ueye.raw',
    reading=True,
    writing=True,
)
s.start()

time.sleep(10)

s.stop()
