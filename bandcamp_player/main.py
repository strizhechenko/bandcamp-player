# coding=utf-8

import json
import logging
import os
import sys
from random import shuffle

import requests
from bandcamp_dl.bandcampjson import BandcampJSON
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


class BandcampRequest(object):
    headers = {'User-Agent': 'bandcamp_player/0.1'}

    @staticmethod
    def get(url):
        logging.info("request: %s", url)
        return requests.get(url, headers=BandcampRequest.headers)


class BandcampAlbumResult(object):
    def __init__(self, soup):
        self.title = soup.attrs['title']
        self.href = soup.attrs['href']

    def __repr__(self):
        return '\n<BandcampResult: title: {0} href: {1}>'.format(self.title, self.href)


class BandcampTag(object):
    def __init__(self, tag):
        self.tag = tag

    def url(self):
        return "https://bandcamp.com/tag/{0}".format(self.tag)

    def page(self):
        return BandcampRequest.get(self.url()).content

    def albums(self):
        soup = BeautifulSoup(self.page(), "html.parser")
        results = soup.find('div', attrs={'class': 'results'}).find_all('a')
        return [BandcampAlbumResult(result) for result in results]

    def album_random(self):
        albums = self.albums()
        shuffle(albums)
        return albums[0]


class BandcampAlbum(object):
    def __init__(self, url):
        self.url = url

    def page(self):
        return BandcampRequest.get(self.url).content

    def tracks(self):
        soup = BeautifulSoup(self.page(), "html.parser")
        results = soup.find('table', attrs={'id': 'track_table'}).find_all('a')
        results = [item.attrs['href'] for item in results if item.has_attr('href')]
        results = [item for item in results if '#lyrics' not in item]
        return [self.url[:self.url.find('/album')] + item for item in results]

    def track_random(self):
        tracks = self.tracks()
        shuffle(tracks)
        return tracks[0]


class BandcampTrack(object):
    tmp_file_path = "/tmp/bandcamp.mp3"

    def __init__(self, url):
        self.url = url

    def download_link(self):
        data = BandcampRequest.get(self.url).content
        soup = BeautifulSoup(data, "html.parser")
        track_meta = json.loads(BandcampJSON(soup).generate()[0])
        return "https:" + track_meta['trackinfo'][0]['file']['mp3-128']

    def save(self):
        response = BandcampRequest.get(self.download_link())
        if response.status_code != 200:
            return
        with open(self.tmp_file_path, 'wb') as tmp_file:
            tmp_file.write(response.content)

    def play(self):
        self.save()
        os.system("mplayer " + self.tmp_file_path)


def __main():
    tag_data = BandcampTag(sys.argv[1])
    while True:
        album_url = tag_data.album_random().href
        album = BandcampAlbum(album_url)
        track_url = album.track_random()
        track = BandcampTrack(track_url)
        track.play()


def main():
    try:
        __main()
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
