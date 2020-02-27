import atexit
import logging

log = logging.getLogger(__name__)


class Output:
    '''
    General interface for frame writing.
    Takes a path, config.
    '''

    def __init__(self, config={}, defaults={}, input_config={}, **kwargs):
        self.output = None
        self.config = {**defaults, **input_config, **config}
        # ffmpeg expects gray, not mono8 pixel format.
        if self.config.get('pixel_format') == 'mono8':
            self.config['pixel_format'] = 'gray'

        atexit.register(self.close)

    def write(self, data=None):
        log.debug('write not implemented.')

    def close(self):
        log.debug('close not implemented.')

    def __str__(self):
        return f'{self.__class__.__name__}'
