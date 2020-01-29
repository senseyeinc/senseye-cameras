from senseye_cameras import create_output

# create a raw video Output object that points to the path1.raw file.
output = create_output('raw', path='path1.raw')

output.write(data=b'dummy data 1')

# Output objects write to a temporary file.
# this allows users to change the path of the Output file anytime before closing the Output.
output.set_path('path2.raw')
output.write(data='dummy data 2')

output.close()
