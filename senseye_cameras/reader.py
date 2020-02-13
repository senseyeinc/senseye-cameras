import logging
from . loop_thread import LoopThread

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
