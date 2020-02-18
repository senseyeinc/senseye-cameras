import sys
import time
import ffmpeg
import logging
import numpy as np

from . input import Input

log = logging.getLogger(__name__)


class CameraFfmpeg(Input):
    '''
    Opens a camera using ffmpeg.
    Args:
        id (int/str): id of the ffmpeg camera
        config (dict): Configuration dictionary. Accepted keywords:
            fps (int): framerate of the camera
            res (tuple): resolution in the format (width, height, channels)
            block_size (int): how many bytes to read from the camera if the camera outputs a stream of bytes.

            camera_pixel_format (str): pixel format of the camera (eg: bgr24, uyvy422)
            pixel_format (str): desired output pixel format of the camera (eg: rawvideo, h264)
    '''

    def __init__(self, id=0, config={}):
        defaults = {
            'fps': 30,
            'res': (1280, 720, 3),
            'block_size': 16384,
            'camera_pixel_format': 'uyvy422',
            'pixel_format': 'rawvideo',
        }
        Input.__init__(self, id=id, config=config, defaults=defaults)

    def get_format(self):
        '''Get os specific format.'''
        if 'linux' in sys.platform:
            return 'v412'
        if sys.platform == 'darwin':
            return 'avfoundation'
        return 'dshow'

    def open(self):
        '''
        Opens the ffmpeg subprocess and logs.
        '''
        self.process = (
            ffmpeg
            .input(
                f'{self.id}',
                format=self.get_format(),
                pix_fmt=self.config.get('camera_pixel_format'),
                framerate=self.config.get('fps'),
                s=f'{self.config.get("res")[0]}x{self.config.get("res")[1]}',
            )
            .output('pipe:', format=self.config.get('pixel_format'))
            # hide logging
            .global_args('-loglevel', 'error', '-hide_banner')
            # disable audio
            .global_args('-an')
            .run_async(pipe_stdout=True)
        )
        log.info(f'Running command: {" ".join(self.process.args)}')
        self.input = self.process.stdout

    def read(self):
        '''
        Reads in raw frames.
        '''
        frame = None

        try:
            if self.config.get('pixel_format') == 'rawvideo':
                # convert rawvideo frames into a numpy array
                frame_size = np.prod(np.array(self.config.get('res')))
                frame_bytes = self.input.read(frame_size)
                frame_str = np.fromstring(frame_bytes, dtype='uint8')
                # add shape metadata to the frame
                # numpy expects (width, height, channels)
                numpy_res = self.config.get('res')[1::-1] + self.config.get('res')[2:]
                frame = frame_str.reshape(numpy_res)
            else:
                # directly read in bytes otherwise
                frame = self.input.read(self.config.get('block_size'))
        except Exception as e:
            log.error(f"Ffmpeg camera error: {e}")

        return frame, time.time()

    def close(self):
        if self.process:
            self.process.stdout.close()
            self.process.wait()
        self.process = None
        self.input = None
