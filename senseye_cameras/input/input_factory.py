import logging

from . camera_usb import CameraUsb
from . camera_pylon import CameraPylon
from . camera_raw_video import CameraRawVideo
from . audio_ffmpeg_input import AudioFfmpegInput
from . audio_port_input import AudioPortInput
from . camera_ueye import CameraUeye

log = logging.getLogger(__name__)


def create_input(type='usb', *args, **kwargs):
    '''
    Factory method for creating media input.
    Supports 'usb', 'video', 'pylon', 'raw_video', 'audio_ffmpeg', 'audio_port'.
    '''
    if type == 'usb' or type == 'video':
        return CameraUsb(*args, **kwargs)
    if type == 'pylon':
        return CameraPylon(*args, **kwargs)
    if type == 'raw_video':
        return CameraRawVideo(*args, **kwargs)
    if type == 'emergent':
        return CameraEmergent(*args, **kwargs)
    if type == 'audio_ffmpeg':
        return AudioFfmpegInput(*args, **kwargs)
    if type == 'audio_port':
        return AudioPortInput(*args, **kwargs)
    if type == 'ueye':
        return CameraUeye(*args, **kwargs)

    log.warning(f'Input type: {type} not supported.')
