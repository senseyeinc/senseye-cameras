import time
import logging
import numpy as np

from . input import Input

log = logging.getLogger(__name__)


class CameraRawVideo(Input):
    '''
    Treats raw video as a camera.
    Args:
        id (str): path to the raw video file.
        config (dict): Configuration dictionary. Accepted keywords:
            res (tuple): frame size in the format (width, height)
    '''

    def __init__(self, id=0, config={}):
        defaults = {
            'res': (1920, 1080),
        }
        Input.__init__(self, id=id, config=config, defaults=defaults)

    def open(self):
        '''Opens raw video as a bytes file.'''
        self.input = open(self.id, 'rb')

    def read(self):
        '''
        Reads in raw video.
        config['res'] dictates how many bytes are read in.
        '''
        frame = None

        try:
            # Length of frame in bytes
            frame_length = np.uint8().itemsize * np.product(self.config.get('res'))
            frame_bytes = self.input.read(frame_length)

            buf = np.frombuffer(frame_bytes, dtype=np.uint8)
            if buf.size != 0:
                frame = buf.reshape(self.config.get('res'))
        except Exception as e:
            log.error(f'{str(self)} read error: {e}')

        return frame, time.time()

    def close(self):
        if self.input:
            self.input.close()
        self.input = None
