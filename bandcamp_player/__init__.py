# coding=utf-8
import logging
import sys

from bandcamp_parser.album import Album
from bandcamp_parser.tag import Tag
from bandcamp_parser.track import Track

logging.basicConfig(level=logging.INFO)


def loop():
    """ Playing tracks in infinite loop """
    tag_data = Tag(sys.argv[1])
    while True:
        album_url = tag_data.album_random().href
        album = Album(album_url)
        track_url = album.track_random()
        track = Track(track_url)
        track.play()


def main():
    """ Playing the tracks until CTRL-C """
    try:
        loop()
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
