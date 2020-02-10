import logging
from pathlib import Path
from subprocess import Popen, PIPE

from . output import Output
from .. utils import ffmpeg_string

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

    def __init__(self, path=None, config={}):
        defaults = {
            'fps': 30,
            'pixel_format': 'rgb24',
            'format': 'rawvideo',
        }
        Output.__init__(self, path=path, config=config, defaults=defaults)

        # update codec based on suffix
        self.generate_codec()

        self.process = None

    def generate_codec(self):
        '''Determines a good codec to use based on path.suffix.'''
        codec_lookup = {
            '.avi': 'huffyuv',
            '.mp4': 'libx264 -crf 0 -preset ultrafast',
            '.mkv': 'h264 -crf 23 -preset ultrafast',
            '.yuv': 'rawvideo',
        }

        suffix = Path(self.path).suffix
        self.config['codec'] = codec_lookup.get(suffix, 'huffyuv')

    def initialize_recorder(self, frame=None):
        '''
        Ffmpeg requires us to pass in frame size.
        Thus, we must have a frame to initialize our recorder.
        '''
        try:
            # if 'res' not in self.config:
            #     self.config['res'] = (frame.shape[1], frame.shape[0])
            # if 'width' not in self.config:
            #     self.config['width'] = frame.shape[1]
            # if 'height' not in self.config:
            #     self.config['height'] = frame.shape[0]
            # if 'channels' not in self.config:
            #     if len(frame.shape) > 2:
            #         self.config['channels'] = frame.shape[2]
            #     else:
            #         self.config['channels'] = 1

            cmd = ffmpeg_string(path=self.tmp_path, **self.config)
            self.process = Popen(cmd.split(), stdin=PIPE)
            self.output = self.process.stdin
            log.critical(cmd)
        except Exception as e:
            log.error(f'Failed to initialize recorder: {self.path} with exception: {e}.')

    def write(self, data=None):
        if data is None:
            return

        if self.output is None:
            self.initialize_recorder(frame=data)

        try:
            self.output.write(data)
        except Exception as e:
            print(e)

    def close(self):
        '''
        Closes ffmpeg process.
        Renames tmp file.
        When ffmpeg writes to a PIPE, communicate closes it cleanly.
        '''
        if self.process:
            if self.process.poll() == None:
                self.process.communicate()
            Output.close(self)

        self.process = None
        self.output = None
