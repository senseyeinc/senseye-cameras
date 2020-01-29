import numpy as np
from senseye_cameras import create_output

# create sample numpy array
data = np.random.rand(256, 256, 3)

# create an ffmpeg video Output object
output = create_output('ffmpeg', path='path1.avi')

output.write(data=data)
output.close()
