# coding=utf-8
from random import shuffle

from bs4 import BeautifulSoup

from bandcamp_parser.request import Request


class AlbumResult(object):
    """ Just for autocompletion and more 'static' structure instead of json/soup """
    def __init__(self, soup):
        self.title = soup.attrs['title']
        self.href = soup.attrs['href']

    def __repr__(self) -> str:
        return '\n<BandcampAlbumResult: title: {0} href: {1}>'.format(self.title, self.href)


class Album(object):
    """ Album object provides access to its tracks """
    def __init__(self, url):
        self.url = url

    def page(self) -> str:
        """ :returns: album's page html """
        return Request.get(self.url).content

    def tracks(self) -> list:
        """ :returns: list of urls of tracks in album """
        soup = BeautifulSoup(self.page(), "html.parser")
        results = soup.find('table', attrs={'id': 'track_table'}).find_all('a')
        results = [item.attrs['href'] for item in results if item.has_attr('href')]
        results = [item for item in results if '#lyrics' not in item]
        return [self.url[:self.url.find('/album')] + item for item in results]

    def track_random(self) -> str:
        """ :returns: link to random track """
        tracks = self.tracks()
        shuffle(tracks)
        return tracks[0]
