from senseye_cameras import create_input

# initialize and open a pylon camera
# a pylon camera can accept a path to a pfs file.
# pfs files can be generated using the PylonViewer application that comes with the pylon Camera Software Suite.
camera = create_input(type='pylon', id=0, config={'pfs': None})


camera.open()
frame, timestamp = camera.read()

print(frame)
