import logging
import numpy as np
from subprocess import Popen, PIPE

from senseye_utils.date_utils import timestamp_now

from . input import Input

log = logging.getLogger(__name__)


class CameraFfmpeg(Input):
    '''
    Opens a camera using ffmpeg.
    '''

    def __init__(self, id=0, config={}):
        defaults = {
            'fps': 30,
            'res': (1280, 720, 3),
            'codec': 'h264',
            'pixel_format': 'rgb24',
        }
        Input.__init__(self, id=id, config=config, defaults=defaults)
        self.input = None

    def open(self):
        '''
        Opens the ffmpeg subprocess and logs.
        '''
        self.cmd = (
            f'ffmpeg '
            f'-f avfoundation '
            f'-video_size {self.config.get("res")[0]}x{self.config.get("res")[1]} '
            f'-framerate {self.config.get("fps")} '
            f'-an -i {self.id} '
            f'-vcodec {self.config.get("codec")} '
            f'-pix_fmt {self.config.get("pixel_format")} '
            f'-f image2pipe -'
        )

        # TODO: os agnostic
        self.process = Popen(self.cmd.split(), stdout=PIPE, stderr=PIPE)
        self.input = self.process.stdout

    def read(self):
        '''
        Reads in raw frames.
        '''
        frame = None

        try:
            if self.config.get('codec') == 'rawvideo':
                frame_size = np.prod(np.array(self.config.get('res')))
                frame_bytes = self.input.read(frame_size)
                frame_str = np.fromstring(frame_bytes, dtype='uint8')
                frame = frame_str.reshape((self.config.get('res')[1], self.config.get('res')[0], self.config.get('res')[2]))
            elif self.config.get('codec') == 'h264':
                frame = self.input.read(8192)
        except Exception as e:
            log.error(f"Ffmpeg camera error: {e}")


        log.critical(len(frame))
        return frame, timestamp_now()

    def close(self):
        if self.process:
            self.process.kill()
        self.process = None
        self.input = None
