import logging

from . h264_pipe import H264Pipe
from . file import File

log = logging.getLogger(__name__)


def create_output(type='usb', *args, **kwargs):
    '''
    Factory method for creating recorders.
    Supports types: 'file', 'h264_pipe'
    '''
    if type == 'h264_pipe':
        return H264Pipe(*args, **kwargs)
    if type == 'file' or type == 'raw' or type == 'ffmpeg':
        return File(*args, **kwargs)

    log.warning(f'Output type: {type} not supported.')
