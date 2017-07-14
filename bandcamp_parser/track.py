# coding=utf-8
import json
import os

from bandcamp_dl.bandcampjson import BandcampJSON
from bs4 import BeautifulSoup

from bandcamp_parser.request import Request


class Track(object):
    """ Provides a way to finally download & play music via mplayer """
    tmp_file_path = "/tmp/bandcamp.mp3"

    def __init__(self, url):
        self.url = url

    def download_link(self) -> str:
        """ :returns: link where the file awaits to be downloaded """
        data = Request.get(self.url).content
        soup = BeautifulSoup(data, "html.parser")
        track_meta = json.loads(BandcampJSON(soup).generate()[0])
        return "https:" + track_meta['trackinfo'][0]['file']['mp3-128']

    def save(self) -> None:
        """ Saves the file to local disk """
        response = Request.get(self.download_link())
        if response.status_code != 200:
            raise ValueError(response.status_code)
        with open(self.tmp_file_path, 'wb') as tmp_file:
            tmp_file.write(response.content)

    def play(self) -> None:
        """ Saves the file to local disk and play it via mplayer """
        self.save()
        os.system("mplayer " + self.tmp_file_path)
