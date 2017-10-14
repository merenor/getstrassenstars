#!/usr/bin/env python3

import requests
import os

from bs4 import BeautifulSoup as Soup


SENDUNGEN = 'http://www.hr-fernsehen.de/sendungen-a-z/strassen-stars/sendungen/index.html'
TARGET = '/volume1/familie/videos/serien/strassenstars/'


def log(text):
    print(text)


def get_current_episode():
    log("Suche aktuelle Episode.")
    link = Soup(requests.get(SENDUNGEN).text, 'html.parser').find('a', 'c-teaser__mediaLink')

    if link is not None:
        return link['href']
    else:
        log("Sorry, keinen Link gefunden!")
        exit()


def download_video(source, targetdir):
    if not targetdir.endswith('/'):
        targetdir += '/'

    log("Suche den Link zur Videodatei.")

    VIDEO = {'type': 'video/mp4'}
    link = Soup(requests.get(source).text, 'html.parser').find('source', attrs=VIDEO)
    if link is not None:
        filename = targetdir + link['src'].split('/')[-1]
        if not os.path.isfile(filename):
            log("Starte Download von " + link['src'] + " ...")
            with open(filename, "wb") as file:
                response = requests.get(link['src'])
                file.write(response.content)
        else:
            log("Datei {} existiert bereits.".format(filename))
            exit()
    else:
        log("Sorry, keinen Video-Link gefunden!")
        exit()


def main():
    log("Starte getstrassenstars.")
    ep = get_current_episode()
    download_video(ep, TARGET)


if __name__ == '__main__':
    main()
