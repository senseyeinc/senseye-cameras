import numpy as np
from senseye_cameras import create_output

# supported extensions
# FILE_PATH = './tmp/usb.avi'
# FILE_PATH = './tmp/usb.mp4'
# FILE_PATH = './tmp/usb.mkv'
# FILE_PATH = './tmp/usb.yuv'
FILE_PATH = './tmp/usb.raw'

data = np.random.rand(256, 256, 3)

# create a raw video Output object that points to the path1.raw file.
output = create_output('file', path=FILE_PATH)

output.write(data=data)
output.close()
