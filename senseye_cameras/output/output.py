import atexit
import logging
import tempfile
from pathlib import Path

log = logging.getLogger(__name__)


class Output:
    '''
    General interface for frame writing.
    Takes a path, config.

    'path' points to the final destination of our video.
    Writes to a generated 'tmp_path'.
    When finished writing, renames 'tmp_path' to 'path'.
    tmp_paths allow users to change 'path' while the 'tmp_path' is being written to.
    '''

    def __init__(self, path=None, config={}, defaults={}, input_config={}):
        self.output = None
        self.set_path(path=path)
        self.set_tmp_path(path=self.path)

        self.config = {**defaults, **input_config, **config}
        atexit.register(self.close)

    def set_path(self, path=None):
        '''Setter for self.path.'''
        self.path = Path(path).absolute()
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)

    def set_tmp_path(self, path):
        '''Generates a tmpfile name in 'path's directory.'''
        path = Path(path)
        self.tmp_path = tempfile.NamedTemporaryFile(
            prefix=path.stem,
            dir=path.parent,
            suffix=path.suffix,
            delete=True
        ).name

        log.debug(f'{str(self)} tmp path set to {self.tmp_path}')

    def write(self, data=None):
        log.debug('write not implemented.')

    def close(self):
        '''
        Attempts to move the file from 'tmp_path' to 'path'.
        Writes config to path.
        '''
        try:
            # make the stream reusable by creating a new tmp path
            old_tmp_path = self.tmp_path
            self.set_tmp_path(self.path)
            if self.path.exists():
                raise Exception(f'Rename from {old_tmp_path} to {self.path} failed, {self.path} already exists.')
            Path(old_tmp_path).replace(self.path)
        except Exception as e:
            log.error(f'Recording rename failed: {e}')

    def __str__(self):
        return f'{self.__class__.__name__}'
