import ffmpeg
import logging
from pathlib import Path

from . output import Output

log = logging.getLogger(__name__)


class VideoFfmpeg(Output):
    '''
    Records raw video using python file IO.
    Writes to a temp file.
    Renames the temp file once recording is done.

    Args:
        path (str): Output path of video.
        config (dict): Configuration dictionary. Accepted keywords:
            fps (int)
            pixel_format (str)
            codec (str)
            format (str): defaults to 'rawvideo'
            res (tuple)
    '''

    def __init__(self, **kwargs):
        defaults = {
            'fps': 30,
            'pixel_format': 'rgb24',
            'format': 'rawvideo',
            'file_codec': {},
        }
        Output.__init__(self, defaults=defaults, **kwargs)

        self.generate_file_codec()
        self.initialize()


    def generate_file_codec(self):
        '''Determines a good codec to use based on path.suffix.'''
        codec_lookup = {
            '.avi': {'vcodec': 'huffyuv'},
            '.mp4': {'vcodec': 'libx264', 'crf': 0, 'preset': 'ultrafast'},
            '.mkv': {'vcodec': 'h264', 'crf': 23, 'preset': 'ultrafast'},
            '.yuv': {'vcodec': 'rawvideo'}
        }

        suffix = Path(self.path).suffix
        self.config['file_codec'] = codec_lookup.get(suffix, codec_lookup['.yuv'])

    def initialize(self):
        '''
        Ffmpeg requires us to pass in frame size.
        Thus, we must have a frame to initialize our recorder.
        '''

        # only include pixel_format and size if we're encoding raw video.
        raw_args = dict(
            pix_fmt=self.config.get('pixel_format'),
            s='1280x720'
        ) if self.config['output_format'] == 'rawvideo' else {}

        self.process = (
            ffmpeg
            .input(
                'pipe:',
                format=self.config.get('output_format'),
                framerate=30,

                **raw_args
            )
            .output(
                self.tmp_path,
                **self.config.get('file_codec'),
            )
            # hide logging
            .global_args('-loglevel', 'error', '-hide_banner')
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )
        log.info(f'Running command: {" ".join(self.process.args)}')
        self.output = self.process.stdin

    def write(self, data=None):
        if data is None:
            return

        try:
            self.output.write(data)
        except: pass

    def close(self):
        '''
        Closes ffmpeg process.
        Renames tmp file.
        '''
        if self.process:
            self.process.stdin.close()
            self.process.wait()
            Output.close(self)
        self.process = None
        self.output = None
