from setuptools import setup
from pathlib import Path

readme = str(Path(Path(__file__).parent.absolute(), 'README.md'))
long_description = open(readme, encoding='utf-8').read()

setup(
    name='senseye_cameras',
    description='Senseye Camera Utilities',
    author='Senseye Inc',
    version='1.0.2',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
        'ffmpeg-python',
        'senseye-pyueye',
    ],
)
