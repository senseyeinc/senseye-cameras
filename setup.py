from setuptools import setup

setup(
    name='senseye_cameras',
    description='Senseye Camera Utilities',
    author='Senseye Inc',
    version='0.1.0',
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
