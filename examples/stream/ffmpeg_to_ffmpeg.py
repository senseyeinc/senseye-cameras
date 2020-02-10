import time
import random
from senseye_cameras import Stream

'''Examples of ffmpeg camera to ffmpeg video streams.'''
WRITE_TIME = 10

def ffmpeg_to_raw_video():
    '''
    input: ffmpeg camera, reads in raw frames
    output: ffmpeg raw video

    functionally equivalent to output_type='raw'
    '''
    s = Stream(
        input_type='ffmpeg', id=0,
        output_type='ffmpeg', path='./tmp/usb.yuv',
        # this is the same
        # output_type='raw', path='./tmp/usb.yuv',
        reading=True,
        writing=True,
    )
    s.start()

    time.sleep(WRITE_TIME)

    s.stop()

def ffmpeg_to_compressed_video():
    '''
    input: ffmpeg camera, reads in raw frames
    output: ffmpeg compressed video, using a random supported compressed video extension
    '''
    supported_video_extensions = ['avi', 'mp4', 'mkv']
    s = Stream(
        input_type='ffmpeg', id=0,
        output_type='ffmpeg', path=f'./tmp/usb.{random.choice(supported_video_extensions)}',
        reading=True,
        writing=True,
    )
    s.start()

    time.sleep(WRITE_TIME)

    s.stop()

def ffmpeg_to_h264_to_raw():
    '''
    input: ffmpeg camera, reads in compressed frames in h264 format
    output: ffmpeg raw video
    '''
    s = Stream(
        input_type='ffmpeg', id=0, input_config={'output_format': 'h264'},
        output_type='ffmpeg', path='./tmp/usb.yuv',
        reading=True,
        writing=True,
    )
    s.start()

    time.sleep(WRITE_TIME)

    s.stop()

# ffmpeg_to_raw_video()
# ffmpeg_to_compressed_video()
ffmpeg_to_h264_to_raw()
