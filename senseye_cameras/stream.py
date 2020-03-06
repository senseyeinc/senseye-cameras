import time
import atexit
import logging
from . safe_queue import SafeQueue

from . reader import Reader
from . writer import Writer

log = logging.getLogger(__name__)


class Stream:
    '''
    Links an Input with an Output.
    Args:
        input_type/input_config/id: see create_input.
        output_type/output_config/path: see create_output
        reading/writing (bool): whether to read/write on start.
        on_read (func): called on frame read. Function should take fn(data=None, timestamp=None) as args.
        on_read/on_write (func): called on frame write. Function should take fn(data=None)
    '''

    def __init__(self,
        input_type='usb', input_config={}, id=0,
        output_type='ffmpeg', output_config={}, path='.',
        input_frequency=None, output_frequency=None,
        reading=False, writing=False,
        on_read=None, on_write=None,
    ):
        self.q = SafeQueue(700)

        self.input_type = input_type
        self.input_config = input_config
        self.id = id

        self.output_type = output_type
        self.output_config = output_config
        self.path = path

        self.input_frequency = input_frequency
        self.output_frequency = output_frequency

        self.on_read = on_read
        self.on_write = on_write

        self.writer = self.reader = None
        atexit.register(self.stop)

        self.reader = Reader(
            self.q, on_read=self.on_read, type=self.input_type, config=self.input_config, frequency=self.input_frequency,
            id=self.id,
        )
        self.reader.start()

        self.writer = Writer(
            self.q, on_write=self.on_write, type=self.output_type, config=self.output_config, frequency=self.reader.frequency,
            input_config=self.reader.input.config, path=self.path,
        )
        self.writer.start()

        if reading:
            self.start_reading()
        if writing:
            self.start_writing()

    def set_path(self, path=None):
        '''Sets the writers' path.'''
        self.path = path
        if self.writer:
            self.writer.set_path(path)

    ####################
    # READER FUNCTIONS
    ####################
    def start_reading(self):
        '''Starts reading in frames.'''
        self.reader.reading = True
        log.info(f'{str(self)} reading started - {time.time()}')

    def stop_reading(self):
        '''Stops reading in frames.'''
        self.reader.reading = False
        log.info(f'{str(self)} reading stopped - {time.time()}')

    ####################
    # WRITER FUNCTIONS
    ####################
    def start_writing(self):
        '''Starts writing frames.'''
        self.writer.initialize_writer()
        self.writer.writing = True
        self.reader.writing = True
        log.info(f'{str(self)} writing started - {time.time()}')

    def stop_writing(self):
        '''Stops writing frames.'''
        self.writer.on_stop()
        self.writer.writing = False
        self.reader.writing = False
        log.info(f'{str(self)} writing stopped - {time.time()}')

    ####################
    # LOOPTHREAD FUNCTIONS
    ####################
    def stop(self):
        self.stop_reading()
        self.stop_writing()
        self.reader.stop()
        self.writer.stop()

    def start(self):
        pass

    def run(self):
        pass

    def __str__(self):
        return f'{self.__class__.__name__}'
