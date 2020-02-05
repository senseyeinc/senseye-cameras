import time
import logging
import numpy as np

from . input import Input
from pyueye import ueye

log = logging.getLogger(__name__)

class CameraUeye(Input):
    '''
    Camera that interfaces with  cameras.

    Args:
        id (int): Id of the pylon camera.
        config (dict): Configuration dictionary. Accepted keywords:
            pfs (str): path to a pfs file.
    '''

    def __init__(self, id=0, config={}):
        defaults = {}
        Input.__init__(self, id=id, config=config, defaults=defaults)

        self.input = ueye.HIDS(0)

    def open(self):
        '''Opens raw video as a bytes file.'''
        # initialize camera
        if(ueye.is_InitCamera(self.input, None) != ueye.IS_SUCCESS):
            log.error("is_InitCamera ERROR")

        # sensor info
        sInfo = ueye.SENSORINFO()
        pcImageMemory = ueye.c_mem_p()
        MemID = ueye.int()
        rectAOI = ueye.IS_RECT()
        pitch = ueye.INT()
        nBitsPerPixel = ueye.INT(24)    #24: bits per pixel for color mode; take 8 bits per pixel for monochrome
        channels = 3                    #3: channels for color mode(RGB); take 1 channel for monochrome
        m_nColorMode = ueye.INT()		# Y8/RGB16/RGB24/REG32
        bytes_per_pixel = int(nBitsPerPixel / 8)

        if int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
            # setup the color depth to the current windows setting
            ueye.is_GetColorDepth(self.input, nBitsPerPixel, m_nColorMode)
            bytes_per_pixel = int(nBitsPerPixel / 8)
        elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
            m_nColorMode = ueye.IS_CM_BGRA8_PACKED
            nBitsPerPixel = ueye.INT(32)
            bytes_per_pixel = int(nBitsPerPixel / 8)
        elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
            m_nColorMode = ueye.IS_CM_MONO8
            nBitsPerPixel = ueye.INT(8)
            bytes_per_pixel = int(nBitsPerPixel / 8)
        else:
            m_nColorMode = ueye.IS_CM_MONO8
            nBitsPerPixel = ueye.INT(8)
            bytes_per_pixel = int(nBitsPerPixel / 8)

        # Can be used to set the size and position of an "area of interest"(AOI) within an image
        nRet = ueye.is_AOI(self.input, ueye.IS_AOI_IMAGE_GET_AOI, rectAOI, ueye.sizeof(rectAOI))
        if nRet != ueye.IS_SUCCESS:
            print("is_AOI ERROR")

        width = rectAOI.s32Width
        height = rectAOI.s32Height

        #---------------------------------------------------------------------------------------------------------------------------------------

        # Allocates an image memory for an image having its dimensions defined by width and height and its color depth defined by nBitsPerPixel
        nRet = ueye.is_AllocImageMem(self.input, width, height, nBitsPerPixel, pcImageMemory, MemID)
        if nRet != ueye.IS_SUCCESS:
            print("is_AllocImageMem ERROR")
        else:
            # Makes the specified image memory the active memory
            nRet = ueye.is_SetImageMem(self.input, pcImageMemory, MemID)
            if nRet != ueye.IS_SUCCESS:
                print("is_SetImageMem ERROR")
            else:
                # Set the desired color mode
                nRet = ueye.is_SetColorMode(self.input, m_nColorMode)

        # Activates the camera's live video mode (free run mode)
        nRet = ueye.is_CaptureVideo(self.input, ueye.IS_DONT_WAIT)
        if nRet != ueye.IS_SUCCESS:
            print("is_CaptureVideo ERROR")

        # Enables the queue mode for existing image memory sequences
        nRet = ueye.is_InquireImageMem(self.input, pcImageMemory, MemID, width, height, nBitsPerPixel, pitch)
        if nRet != ueye.IS_SUCCESS:
            print("is_InquireImageMem ERROR")
        else:
            print("Press q to leave the programm")

        self.pcImageMemory = pcImageMemory
        self.width = width
        self.height = height
        self.nBitsPerPixel = nBitsPerPixel
        self.pitch = pitch
        self.bytes_per_pixel = bytes_per_pixel
        self.pcImageMemory = pcImageMemory
        self.MemID = MemID


    def read(self):
        '''
        Reads in raw video.
        config['res'] dictates how many bytes are read in.
        '''
        array = ueye.get_data(self.pcImageMemory, self.width, self.height, self.nBitsPerPixel, self.pitch, copy=True)
        frame = np.reshape(array, (self.height.value, self.width.value, self.bytes_per_pixel))
        return frame, time.time()

    def close(self):
        ueye.is_FreeImageMem(self.input, self.pcImageMemory, self.MemID)
        ueye.is_ExitCamera(self.input)
