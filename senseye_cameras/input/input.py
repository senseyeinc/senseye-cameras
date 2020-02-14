import logging
import atexit

log = logging.getLogger(__name__)


class Input:
    '''General interface for cameras/other frame sources.'''

    def __init__(self, id=0, config={}, defaults={}):
        self.id = id
        self.input = None
        self.config = {**defaults, **config}
        atexit.register(self.close)

    def open(self):
        '''Initializes the camera.'''
        log.warning(f'Open not implemented for {str(self)}. There was most likely an error initializing this object.')

    def read(self):
        log.debug(f'Read not implemented for {str(self)}')
        return None, None

    def close(self):
        '''Properly disposes of the camera object.'''
        log.warning(f'Close not implemented for {str(self)}.')

    def __str__(self):
        return f'{self.__class__.__name__}:{self.id}'
