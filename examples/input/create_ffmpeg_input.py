from senseye_cameras import create_input

# initialize and open an ffmpeg camera
camera = create_input(type='ffmpeg', id=0, config={})


camera.open()
frame, timestamp = camera.read()

print(frame)
