import time
from senseye_cameras import Stream

'''
Shows use of callbacks that allow users to process a frame right after it's read, and right before it's written.
'''

SLEEP_TIME = 5
CAMERA_ID = 0
FILE_PATH = './tmp/usb.mkv'

frames_read = 0
frames_written = 0

def on_frame_read(data, timestamp):
    global frames_read
    print(f'Read frame at time: {timestamp}')
    frames_read += 1

def on_frame_written(data):
    global frames_written
    print(f'Wrote frame.')
    frames_written += 1

# create a stream using a usb camera that outputs to an avi file.
# every time a frame is read, call the function on_frame_read.
# every time a frame is written, call the function on_frame_written.
s = Stream(
    input_type='usb', id=CAMERA_ID,
    output_type='file', path=FILE_PATH,
    on_read=on_frame_read,
    on_write=on_frame_written,
    reading=True,
    writing=False,
)
s.start()

time.sleep(1)

# since the writing kwarg passed to the stream was False, we must manually start the stream
s.start_writing()

time.sleep(SLEEP_TIME)
s.stop()

print(f'frames_read: {frames_read}')
print(f'frames_written: {frames_written}')
