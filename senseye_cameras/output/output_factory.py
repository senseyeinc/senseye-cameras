import logging

from . video_raw import VideoRaw
from . video_ffmpeg_bayer import VideoFfmpegBayer
from . video_ffmpeg import VideoFfmpeg
from . audio_ffmpeg_output import AudioFfmpegOutput
from . audio_port_output import AudioPortOutput

log = logging.getLogger(__name__)


def create_output(type='usb', *args, **kwargs):
    '''
    Factory method for creating recorders.
    Supports 'raw', 'ffmpeg_bayer', 'ffmpeg', 'audio_ffmpeg', 'audio_port'
    '''
    if type == 'raw':
        return VideoRaw(*args, **kwargs)
    if type == 'ffmpeg_bayer':
        return VideoFfmpegBayer(*args, **kwargs)
    if type == 'ffmpeg':
        return VideoFfmpeg(*args, **kwargs)
    if type == 'audio_ffmpeg':
        return AudioFfmpegOutput(*args, **kwargs)
    if type == 'audio_port':
        return AudioPortOutput(*args, **kwargs)

    log.warning(f'Output type: {type} not supported.')
