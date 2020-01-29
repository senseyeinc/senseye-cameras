import time
from senseye_cameras import Stream

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
    input_type='usb', id=0,
    output_type='ffmpeg', path='./tmp/usb.avi',
    on_read=on_frame_read,
    on_write=on_frame_written,
    # whether to start reading immediately when start() is called
    reading=True,
    # whether to start writing immediately when start() is called
    writing=False,
)
s.start()

time.sleep(2)

# since the writing kwarg passed to Stream was False, we must manually tell the stream to start writing
s.start_writing()

time.sleep(5)

s.stop()

print(f'frames_read: {frames_read}')
print(f'frames_written: {frames_written}')
