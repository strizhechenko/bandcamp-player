# coding=utf-8
from random import shuffle

from bs4 import BeautifulSoup

from bandcamp_parser.album import AlbumResult
from bandcamp_parser.request import Request


class Tag(object):
    """ Provides access to album list by specified tag/genre """

    def __init__(self, tag):
        self.tag = tag

    def url(self) -> str:
        """ :returns: page url for given tag/genre """
        return "https://bandcamp.com/tag/{0}".format(self.tag)

    def page(self) -> str:
        """ :returns: html for tag's/genre's page """
        return Request.get(self.url()).content

    def albums(self) -> list:
        """ :returns: list of Albums from first tag/genre page """
        soup = BeautifulSoup(self.page(), "html.parser")
        results = soup.find('div', attrs={'class': 'results'}).find_all('a')
        return [AlbumResult(result) for result in results]

    def album_random(self) -> AlbumResult:
        """ :returns: random Album from first tag/genre page """
        albums = self.albums()
        shuffle(albums)
        return albums[0]
