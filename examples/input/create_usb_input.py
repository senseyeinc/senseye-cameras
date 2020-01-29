from senseye_cameras import create_input

# initialize and open a usb camera
camera = create_input(type='usb', id=0, config={})

# print documentation for the CameraUsb module
# docs will show what key/value pairs can go into the config dictionary
print(camera.__doc__)

camera.open()
frame, timestamp = camera.read()

print(frame)
