# -*- coding: utf-8 -*-

import json
import requests

import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

class NeteaseSearch():
    headers = {
        'User-Agent':
            '''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15''',
        'Cookie':
            'appver=1.5.0.75771'
    }

    def __init__(self, keyword, search_type=1, offset=0, limit=10):
        search_url = 'http://music.163.com/api/search/get'
        data = {
            's': keyword,  # S stands for keyword to search
            'type':
                search_type,  # 1 for songs, 10 for albums, 100 for artists, 1000 for playlists, 1002 for users
            'offset': offset,  # For splitting pages
            'limit': limit  # Item quantity to return #'MUSIC_U' Meaning unknown
        }

        self.raw_response = requests.post(
            search_url, data, headers=self.headers)

        self.search_result_dict = json.loads(self.raw_response.text)
        print(self.search_result_dict)

        # if self.search_result_dict['result']['songCount'] == 0:
        #     self.song_availability = False
        #     try:
        #         logging.critical(
        #             'Unable to find song with keyword {}'.format(keyword))
        #     except:
        #         pass
        # else:
        self.song_availability = True

    def get_song_url(self, encrypted_ID):
        request_url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        req = {"ids": encrypted_ID, "br": '320', "csrf_token": ''}
        raw_responce_url = requests.post(request_url, req)
        return raw_responce_url.text

    def get_song_ID(self):
        if self.song_availability == False:
            return None
        self.song_id = self.search_result_dict['result']['songs'][0]['id']
        try:
            logging.info('Song ID: {0}'.format(self.song_id))
        except:
            pass

        return self.song_id

    def _fetch_lrc(self):
        if self.song_availability == False:
            return None
        if not (('self.song_id' in locals()) or ('self.song_id' in globals())):
            individual_id = self.get_song_ID()
        else:
            individual_id = self.song_id
        lyrics_url = 'http://music.163.com/api/song/lyric?id={0}&lv=-1&kv=-1&tv=-1'.format(
            individual_id)
        lyrics_raw = requests.get(lyrics_url, self.headers)
        self.lyrics_result = json.loads(lyrics_raw.text)
        try:
            logging.debug('Lyrics JSON result: {0}'.format(self.lyrics_result))
        except:
            pass

        # Get uploader's nickname
        try:
            self.lyrics_username = self.lyrics_result['lyricUser']['nickname']
        except:
            self.lyrics_username = None
        # Get translator's nickname
        try:
            self.translater_username = self.lyrics_result['transUser'][
                'nickname']
        except:
            self.lyrics_username = None
        # Get lyrics
        try:
            self.lrc_original_text = self.lyrics_result['lrc']['lyric']
        except:
            self.lrc_original_text = None
        # Get translation
        try:
            self.lrc_translation_text = self.lyrics_result['tlyric']['lyric']
        except:
            self.lrc_translation_text = None

    # Get LRC lyrics
    def lrc(self):
        if self.song_availability == False:
            return None
        try:
            return self.lrc_original_text
        except:
            self._fetch_lrc()
            return self.lrc_original_text

    # Get lyrics translation
    def translation(self):
        if self.song_availability == False:
            return None
        try:
            return self.lrc_translation_text
        except:
            self._fetch_lrc()
            return self.lrc_translation_text


def main():
    keyword = '艾热'
    search_type = 100
    search = NeteaseSearch(keyword, search_type)
    songID = search.get_song_ID()
    print(songID)


if __name__ == '__main__':
    main()
