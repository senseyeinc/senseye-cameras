import time
import atexit
import logging
from . loop_thread import LoopThread
from . safe_queue import SafeQueue

from . output.output_factory import create_output
from . input.input_factory import create_input

log = logging.getLogger(__name__)


class Reader(LoopThread):
    '''Reads data into a queue.'''

    def __init__(self, q, on_read=None, type='usb', config={}, id=0, frequency=None, reading=False, writing=False):
        self.q = q
        self.on_read = on_read

        self.type = type

        self.input = create_input(type=type, config=config, id=id)
        self.input.open()
        self.reading = reading
        self.writing = writing
        log.info(f'Started {str(self.input)}. Config: {self.input.config}')

        self.frequency = frequency
        if self.frequency is None:
            self.frequency = self.input.config.get('fps', 100)
        LoopThread.__init__(self, frequency=self.frequency)

    def loop(self):
        if self.reading:
            data, timestamp = self.input.read()
            if data is not None:
                if self.on_read is not None:
                    self.on_read(data=data, timestamp=timestamp)
                if self.writing:
                    self.q.put_nowait(data)

    def on_stop(self):
        self.input.close()
        log.info(f'Stopped {str(self.input)}.')


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
            log.info(f'Stopped {str(self.output)}. Path: {self.output.path}. Frames written: {self.frames_written}')
            self.frames_written = 0

class Stream(LoopThread):
    '''
    IO Stream with a reader/writer on seperate threads.

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
        min_disk_space_bytes=-1,
    ):
        LoopThread.__init__(self, frequency=1)

        self.q = SafeQueue(700)

        self.min_disk_space_bytes = min_disk_space_bytes

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

        self.reader = Reader(self.q, on_read=self.on_read, type=self.input_type, config=self.input_config, id=self.id, frequency=self.input_frequency)
        self.reader.start()

        self.writer = Writer(self.q, on_write=self.on_write, type=self.output_type, config=self.output_config, path=self.path, frequency=self.reader.frequency, input_config=self.reader.input.config)
        self.writer.start()

        if reading:
            self.start_reading()
        if writing:
            self.start_writing()

    def set_path(self, path=None):
        self.path = path
        if self.writer:
            self.writer.set_path(path)

    ####################
    # READER FUNCTIONS
    ####################
    def start_reading(self):
        self.reader.reading = True
        log.info(f'{str(self)} reading started - {time.time()}')

    def stop_reading(self):
        self.reader.reading = False
        log.info(f'{str(self)} reading stopped - {time.time()}')

    def set_prop(self, name=None, value=None):
        if self.reader and self.reader.input:
            self.reader.input.set_prop(name, value)

    def get_prop(self, name=None):
        if self.reader and self.reader.input:
            return self.reader.input.get_prop(name)
        return None

    ####################
    # WRITER FUNCTIONS
    ####################
    def start_writing(self):
        self.writer.initialize_writer()
        self.writer.writing = True
        self.reader.writing = True
        log.info(f'{str(self)} writing started - {time.time()}')

    def stop_writing(self):
        self.writer.on_stop()
        self.writer.writing = False
        self.reader.writing = False
        log.info(f'{str(self)} writing stopped - {time.time()}')

    ####################
    # LOOPTHREAD FUNCTIONS
    ####################
    def on_stop(self):
        self.stop_reading()
        self.stop_writing()
        self.reader.stop()
        self.writer.stop()

    def __str__(self):
        return f'{self.__class__.__name__}'
