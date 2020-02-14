import logging
from . loop_thread import LoopThread
from . output.output_factory import create_output

log = logging.getLogger(__name__)


class Writer(LoopThread):
    '''Writes data from a queue into an output file.'''
    def __init__(self, q, on_write=None, type='ffmpeg', config={}, path=0, frequency=None, writing=False, input_config={}):
        self.q = q
        self.on_write = on_write
        self.writing = writing
        self.frequency = frequency

        self.type = type
        self.config = config
        self.path = path
        self.input_config = input_config

        if self.frequency is None:
            self.frequency = self.config.get('fps', 100)
        LoopThread.__init__(self, frequency=self.frequency)

    def initialize_writer(self):
        self.output = create_output(type=self.type, config=self.config, path=self.path, input_config=self.input_config)
        log.info(f'Started {str(self.output)}. Config: {self.output.config}')
        self.frames_written = 0

    def loop(self):
        if self.writing:
            data = self.q.get_nowait()
            if data is not None:
                self.output.write(data)
                self.frames_written += 1
                if self.on_write is not None:
                    self.on_write(data=data)

    def set_path(self, path=None):
        self.output.set_path(path)
        log.info(f'{str(self)} path set to {path}')

    def on_stop(self):
        # clear out the current q
        if self.writing:
            purge = self.q.to_list()
            for data in purge:
                self.output.write(data)
            self.output.close()
            log.info(f'Stopped {str(self.output)}.')
            self.frames_written = 0
