from setuptools import setup
import sys

version='0.0.0'

requires = []

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name = 'mlx90641-driver',
    version = version,
    description = 'MLX90641 FIR Array python interface',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = 'Apache License, Version 2.0',
    # entry_points = {'console_scripts': ['mlx90641-dump-frame = mlx.examples.mlx90640_dump_frame:main']},
    entry_points = {'console_scripts': []},
    install_requires = requires,
    url = 'https://github.com/melexis-fir/mlx90641-driver-py',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/melexis-fir/mlx90641-driver-py/archive/V'+version+'.tar.gz',
    packages = ['mlx90641'],
    package_dir = {'mlx90641': 'mlx90641'},
    package_data = {'mlx90641': ['libs/**/*.dll', 'libs/**/*.so']},

    classifiers = [
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)
