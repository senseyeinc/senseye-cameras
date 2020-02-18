import ffmpeg
import logging
from threading import Thread

from . output import Output

log = logging.getLogger(__name__)


class H264Pipe(Output):
    '''
    Converts raw video to a h264 stream.
    h264 data can be accessed by passing a callback to the config that access the data positional argument.
        for example:
            def my_callback(data):
                print(f'My h264 bytestream data: {data}')
            h264_pipe = H264Pipe(config={'callback': my_callback})

    Args:
        config (dict): Configuration dictionary. Accepted keywords:
            callback (func): user passed in function that gives the user access to the h264 data.
                Accepts the data positional argument.
            block_size (int): amount of h264 bytes to read in the callback func.
            fps: (int)
            pixel_format (str): pixel format of the inputted raw video (eg: rgb24)
    '''

    def __init__(self, **kwargs):
        defaults = {
            'fps': 30,
            'pixel_format': 'rgb24',
            'callback': None,
            'block_size': 16384,
        }
        Output.__init__(self, defaults=defaults, **kwargs)

        self.decoder = None

    def initialize_decoder(self):
        self.decoder = (
            ffmpeg
            .input(
                'pipe:',
                format='rawvideo',
                pix_fmt=self.config.get('pixel_format'),
                s=f'{self.config.get("res")[0]}x{self.config.get("res")[1]}',
                framerate='30',
            )
            .output('pipe:', format='h264', crf=20, preset='ultrafast')
            .global_args('-loglevel', 'error', '-hide_banner')
            .run_async(pipe_stdin=True, pipe_stdout=True)
        )

        read_thread = Thread(target=self.read_from_decoder)
        read_thread.daemon = True
        read_thread.start()

    def read_from_decoder(self):
        while 1:
            if self.decoder is None:
                break
            data = self.decoder.stdout.read(self.config.get('block_size'))
            self.config.get('callback')(data)

    def write(self, data=None):
        if self.decoder is None:
            self.config['res'] = [data.shape[1], data.shape[0]] + list(data.shape[2:])
            self.initialize_decoder()
        self.decoder.stdin.write(data.tostring())

    def close(self):
        if self.decoder:
            self.decoder.stdin.close()
            self.decoder = None
