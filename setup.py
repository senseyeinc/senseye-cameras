from setuptools import setup

# Get version number from version file
with open('.version', 'r') as f:
    VERSION = f.read()

setup(
    name='senseye_cameras',
    description='Senseye Camera Utilities',
    author='Senseye Inc',
    version=VERSION,
    packages=[
        'senseye_cameras',
        'senseye_cameras.input',
        'senseye_cameras.output',
    ],
    install_requires=[
        'sounddevice',
        'soundfile',

        'numpy',
        'opencv-python',
    ],
)
