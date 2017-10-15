#!/usr/bin/env python3

import requests
import os
import time

from bs4 import BeautifulSoup as Soup


SENDUNGEN = 'http://www.hr-fernsehen.de/sendungen-a-z/strassen-stars/sendungen/index.html'
TARGET = '/volume1/familie/videos/serien/strassenstars/'


def log(text):
    current_time = time.strftime('%d.%m.%Y %H:%M:%S')
    print(current_time, "-", text)
    with open('getstrassenstars.log', 'w') as f:
        f.write(current_time + ' - ' + text + '\n')


def get_current_episode():
    log("Suche aktuelle Episode.")
    link = Soup(requests.get(SENDUNGEN).text, 'html.parser').find('a', 'c-teaser__mediaLink')

    if link is not None:
        return link['href']
    else:
        log("Sorry, keinen Link gefunden!")
        exit()


def get_recorded_episodes():
    with open('recorded_episodes.txt', 'r') as f:
        return [line.strip() for line in f]


def learn_episode(link):
    lines = get_recorded_episodes()
    lines.append(link)

    with open('recorded_episodes.txt', 'a') as f:
        for line in lines:
            f.write(line + '\n')


def download_video(source, targetdir):
    """Tests if Episode is already downloaded.
    Else, gets the actual video link and downloads the video to target folder."""

    if not targetdir.endswith('/'):
        targetdir += '/'

    log("Suche den Link zur Videodatei.")

    VIDEO = {'type': 'video/mp4'}

    if source in get_recorded_episodes():
        log("Aktuelle Episode bereits heruntergeladen.")
        exit()
    else:
        learn_episode(source)

    link = Soup(requests.get(source).text, 'html.parser').find('source', attrs=VIDEO)
    if link is not None:
        filename = targetdir + link['src'].split('/')[-1]
        if not os.path.isfile(filename):
            log("Starte Download von " + link['src'] + " ...")
            with open(filename, 'wb') as f:
                f.write(requests.get(link['src']).content)
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
