import time
from senseye_cameras import Stream

f = open('hmm.mkv', 'wb')
def callback(data):
    global f
    f.write(data)

s = Stream(
    input_type='usb', id=0,
    output_type='h264_pipe', output_config={
        'pixel_format': 'bgr24',
        'callback': callback
    },
    reading=True,
    writing=True,
)
s.start()

time.sleep(10)

s.stop()
