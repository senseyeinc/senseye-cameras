import cv2
import time
import logging

from . input import Input

log = logging.getLogger(__name__)


class CameraUsb(Input):
    '''
    Opens a usb camera or video using OpenCV.

    Args:
        id (int OR str): id of the camera, or path to a video file.
        config (dict): Configuration dictionary. Accepted keywords:
            res (tuple): frame size
            codec (str)
            fps (int)
    '''

    def __init__(self, id=0, config={}):
        defaults = {
            'fps': 30,
            'codec': 'MJPG',
            'use_dshow': 0,
            'channels': 3,
            'format': 'rawvideo',
        }
        Input.__init__(self, id=id, config=config, defaults=defaults)

    def configure(self):
        '''
        Configures the camera using a config.
        Supported configurations: fps, codec, res

        Fills self.config with camera attributes.
        Logs camera start.
        '''
        if 'fps' in self.config:
            self.input.set(cv2.CAP_PROP_FPS, self.config.get('fps'))
        if 'codec' in self.config:
            self.input.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self.config.get('codec')))
        if 'res' in self.config:
            self.input.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.get('res')[0])
            self.input.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.get('res')[1])

        self.config['res'] = (int(self.input.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.input.get(cv2.CAP_PROP_FRAME_HEIGHT)), 3)
        self.config['width'] = int(self.input.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.config['height'] = int(self.input.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.config['fps'] = (int(self.input.get(cv2.CAP_PROP_FPS)))
        self.config['codec'] = (int(self.input.get(cv2.CAP_PROP_FOURCC)))


    def open(self):
        # If specified, enable DSHOW. This is required for some camera APIs,
        # Specifically involved with choosing camera resolution
        if self.config['use_dshow'] and type(self.id) is str:
            self.id += cv2.CAP_DSHOW

        self.input = cv2.VideoCapture(self.id)

        if not self.input.isOpened():
            raise Exception(f'USB Camera {self.id} failed to open.')
        else:
            self.configure()

        # the first read is usually delayed on linux/windows by ~0.4 seconds
        # prime the opencv object for delayless reads
        self.input.read()

    def read(self):
        '''
        Reads in frames.
        Converts frames from BGR to the more commonly used RGB format.
        '''
        frame = None

        try:
            ret, frame = self.input.read()
            if not ret:
                raise Exception(f'Opencv VideoCapture ret error: {ret}')
            # bgr to rgb
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except Exception as e:
            log.error(f'{str(self)} read error: {e}')

        return frame, time.time()

    def close(self):
        if self.input:
            self.input.release()
        self.input = None
