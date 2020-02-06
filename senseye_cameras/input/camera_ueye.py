import time
import logging
import numpy as np
from pyueye import ueye

from . input import Input

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class CameraUeye(Input):
    '''
    Camera that interfaces with ueye cameras.

    Args:
        id (int): Id of the ueye camera.
        config (dict): Configuration dictionary. Accepted keywords:
            fps (int): desired frames per second
            exposure (str): desired exposure
            autofocus (bool): whether to enable autofocus
            autogain (bool): whether to enable autogain
    '''

    def __init__(self, id=0, config={}):
        defaults = {
            'fps': 60,
            'exposure': 60,
            'autofocus': True,
            'autogain': True,
        }
        Input.__init__(self, id=id, config=config, defaults=defaults)

        self.input = ueye.HIDS(self.id)

    def initialize_dimensions(self):
        '''
        Gets dimensions of the camera.
        Sets:
            self.width
            self.height
        '''
        log.info('Getting camera dimensions...')
        rectAOI = ueye.IS_RECT()
        nRet = ueye.is_AOI(self.input, ueye.IS_AOI_IMAGE_GET_AOI, rectAOI, ueye.sizeof(rectAOI))
        if nRet != ueye.IS_SUCCESS:
            log.error("is_AOI ERROR")
        self.width = rectAOI.s32Width
        self.height = rectAOI.s32Height
        self.config['res'] = (self.width.value, self.height.value)

    def initialize_color_mode(self):
        '''
        Initializes color mode.
        Sets:
            self.m_nColorMode
            self.bits_per_pixel
            self.bytes_per_pixel
        '''
        # get color mode
        sensor_info = ueye.SENSORINFO()
        color_mode = int.from_bytes(sensor_info.nColorMode.value, byteorder='big')
        self.m_nColorMode = ueye.INT()

        # determine the number of bits/bytes per pixel through the color mode
        bits_per_pixel = ueye.INT(24)
        if color_mode == ueye.IS_COLORMODE_BAYER:
            # setup the color depth to the current windows setting
            ueye.is_GetColorDepth(self.input, bits_per_pixel, self.m_nColorMode)
        elif color_mode == ueye.IS_COLORMODE_CBYCRY:
            self.m_nColorMode = ueye.IS_CM_BGRA8_PACKED
            bits_per_pixel = ueye.INT(32)
        elif color_mode == ueye.IS_COLORMODE_MONOCHROME:
            self.m_nColorMode = ueye.IS_CM_MONO8
            bits_per_pixel = ueye.INT(8)
        else:
            self.m_nColorMode = ueye.IS_CM_MONO8
            bits_per_pixel = ueye.INT(8)
        self.bytes_per_pixel = int(bits_per_pixel / 8)
        self.bits_per_pixel = bits_per_pixel

    def initialize_memory(self):
        '''
        Allocates image memory.
        Sets:
            self.mem_id
            self.mem_image
        '''
        # Allocates an image memory for an image having its dimensions defined by width and height and its color depth defined by nBitsPerPixel
        mem_id = ueye.int()
        mem_image = ueye.c_mem_p()
        nRet = ueye.is_AllocImageMem(self.input, self.width, self.height, self.bits_per_pixel, mem_image, mem_id)
        if nRet != ueye.IS_SUCCESS:
            log.error("is_AllocImageMem ERROR")
        else:
            # Makes the specified image memory the active memory
            nRet = ueye.is_SetImageMem(self.input, mem_image, mem_id)
            if nRet != ueye.IS_SUCCESS:
                log.error("is_SetImageMem ERROR")
            else:
                # Set the desired color mode
                nRet = ueye.is_SetColorMode(self.input, self.m_nColorMode)
        self.mem_id = mem_id
        self.mem_image = mem_image

    def initialize_modes(self):
        '''
        Enables live video mode.
        Enables queue mode.
        Sets:
            self.pitch
        '''
        # Activates the camera's live video mode (free run mode)
        nRet = ueye.is_CaptureVideo(self.input, ueye.IS_DONT_WAIT)
        if nRet != ueye.IS_SUCCESS:
            log.error("is_CaptureVideo ERROR")

        # Enables the queue mode for existing image memory sequences
        self.pitch = ueye.INT()
        nRet = ueye.is_InquireImageMem(self.input, self.mem_image, self.mem_id, self.width, self.height, self.bits_per_pixel, self.pitch)
        if nRet != ueye.IS_SUCCESS:
            log.error("is_InquireImageMem ERROR")

    def initialize_camera_settings(self):
        '''Sets pixel_clock, fps, exposure, autofocus, autogain based on self.config.'''
        # get max pixel clock
        pixel_clock_range = (ueye.c_uint * 3)()
        ret = ueye.is_PixelClock(self.input, ueye.IS_PIXELCLOCK_CMD_GET_RANGE, pixel_clock_range, 3 * ueye.sizeof(ueye.UINT()))
        log.info(f'pixel_clock max: {pixel_clock_range[0]}, pixel_clock min: {pixel_clock_range[1]}, ret val: {ret}')
        # max out pixel clock
        pixel_clock = ueye.c_int(pixel_clock_range[1])
        ret = ueye.is_PixelClock(self.input, ueye.IS_PIXELCLOCK_CMD_SET, pixel_clock, ueye.sizeof(pixel_clock))
        self.config['pixel_clock'] = pixel_clock.value
        log.info(f'Actual pixel clock: {pixel_clock}, ret val: {ret}')

        # max out frame rate
        target_frame_rate = ueye.double(self.config.get('fps'))
        actual_frame_rate = ueye.double(0.0)
        ret = ueye.is_SetFrameRate(self.input, target_frame_rate, actual_frame_rate)
        self.config['fps'] = actual_frame_rate.value
        log.info(f'Attempted to set frame rate to {target_frame_rate}, ret value: {ret}, actual frame rate: {actual_frame_rate}')

        # max out exposure
        target_exposure = ueye.double(self.config.get('exposure'))
        actual_exposure = ueye.double(0.0)
        ret = ueye.is_Exposure(self.input, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, target_exposure, ueye.sizeof(target_exposure))
        get_ret = ueye.is_Exposure(self.input, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, actual_exposure, ueye.sizeof(actual_exposure))
        self.config['exposure'] = actual_exposure.value
        log.info(f'Attempted to set exposure to {target_exposure}, ret value: {ret}, actual frame rate: {actual_exposure}')

        # enable autofocus
        if self.config.get('autofocus'):
            ret = ueye.is_Focus(self.input, ueye.FOC_CMD_SET_ENABLE_AUTOFOCUS, None, 0)

        # enable autogain
        if self.config.get('autogain'):
            ret = ueye.is_SetAutoParameter(self.input, ueye.IS_SET_ENABLE_AUTO_GAIN, ueye.double(1), ueye.double(0))

    def open(self):
        '''Opens and initializes ueye camera.'''
        # initialize camera
        if(ueye.is_InitCamera(self.input, None) != ueye.IS_SUCCESS):
            log.error("is_InitCamera ERROR")

        self.initialize_color_mode()
        self.initialize_dimensions()
        self.initialize_memory()
        self.initialize_modes()
        self.initialize_camera_settings()

    def read(self):
        array = ueye.get_data(self.mem_image, self.width, self.height, self.bits_per_pixel, self.pitch, copy=False)
        frame = np.reshape(array, (self.height.value, self.width.value, self.bytes_per_pixel))
        return frame, time.time()

    def close(self):
        ueye.is_FreeImageMem(self.input, self.mem_image, self.mem_id)
        ueye.is_ExitCamera(self.input)
