import time
from senseye_cameras import Stream


'''Takes a usb input and writes to a file.'''

CAMERA_ID = 0

# supported file extensions
# FILE_PATH = './tmp/usb.avi'
# FILE_PATH = './tmp/usb.mp4'
# FILE_PATH = './tmp/usb.mkv'
# FILE_PATH = './tmp/usb.yuv'
FILE_PATH = './tmp/usb.raw'

s = Stream(
    input_type='usb', id=CAMERA_ID,
    output_type='file', path=FILE_PATH,
    reading=True,
    writing=True,
)
s.start()

time.sleep(5)

s.stop()
