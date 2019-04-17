# -*- coding:utf8 -*-

import re
import sys
import json
import codecs
import requests
import traceback
from bs4 import BeautifulSoup
# fix issue: 'ascii' codec can't encode characters in position 10-13: ordinal not in range(128)
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def get_playlist_by_artist_id(artist_id):
    url = 'https://music.163.com/artist?id={}'.format(artist_id)
    pattern = r'<a.*?href="\/song\?id=([0-9]*)".*?>(.*?)</a>'
    headers = {
        "Host":
            "music.163.com",
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"
    }
    resp = requests.get(url, headers=headers)
    # print(resp.text)
    # song_id_list = re.findall(r'"\/song\?id=([0-9]*)"', resp.text)
    playlist = []
    soup = BeautifulSoup(resp.text, "html.parser")
    for item in soup.find('ul', class_='f-hide').children:
        result = re.search(pattern, str(item))
        if not result:
            continue
        song_id, song_name = result.groups()
        # print('song_id:%s' % song_id)
        # print('song_name:%s' % song_name)
        lyrics = get_song_lyrics(song_id)
        if lyrics is None:
            lyrics = ''
        lyrics = lyrics.split('\n')
        song = {'name': song_name, 'lyrics': lyrics}
        playlist.append(song)
    return playlist


def get_song_lyrics(song_id):
    url = "http://music.163.com/api/song/lyric?id={}&lv=1&kv=1&tv=-1".format(
        song_id)
    try:
        resp = requests.post(url)
        data = resp.json()
        lyric = data['lrc']['lyric']
    except KeyError:
        return None
    pat = re.compile(r'\[.*\]')
    lrc = re.sub(pat, '', lyric)
    # lrc = lrc.strip()
    return lrc.encode('utf8')


air_artist_id = 1203045
xjk_artist_id = 13333
songs = get_playlist_by_artist_id(air_artist_id)
# data = {"artist": "艾热", "songs": songs}
data = {"artist": "新街口组合", "songs": songs}
# print data
with open('xjk.json', 'w') as f:
    f.write(json.dumps(data))
