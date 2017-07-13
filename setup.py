from setuptools import setup

setup(
    name='bandcamp-player',
    version='0.1.0',
    packages=['bandcamp_player'],
    url='https://github.com/strizhechenko/bandcamp-player',
    license='MIT',
    author='Oleg Strizhechenko',
    author_email='oleg.strizhechenko@gmail.com',
    description='Utility for streaming random music from bandcamp by specified tag',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Sound/Audio',
        'License :: Public Domain',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'beautifulsoup4',
        'requests',
        'bandcamp-downloader'
    ],
    entry_points={
        'console_scripts': [
            'bandcamp-player=bandcamp_player.main:main',
        ],
    },
)
