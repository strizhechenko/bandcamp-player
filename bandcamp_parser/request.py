# coding=utf-8
import logging

import requests


class Request(object):
    """ Simplifies querying bandcamp that protects from python-requests User-Agent """
    headers = {'User-Agent': 'bandcamp_player/0.1'}

    @staticmethod
    def get(url) -> requests.Response:
        """ :returns: Response from bandcamp """
        logging.info("request: %s", url)
        return requests.get(url, headers=Request.headers)
