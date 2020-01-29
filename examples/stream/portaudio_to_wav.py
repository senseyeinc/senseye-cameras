import time
from senseye_cameras import Stream

s = Stream(
    input_type='audio_port', id=0,
    output_type='audio_port', path='./tmp/audio.wav',
    reading=True, writing=True,
)
s.start()

time.sleep(5)

s.stop()
