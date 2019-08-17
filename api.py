#!/usr/bin/env python3

import requests
import os

# SONG = 2421807
__URL__ = 'https://api.planningcenteronline.com/services/v2/songs/'
__ID__ = os.environ.get('ID') or ''
__SECRET__ = os.environ.get('SECRET') or ''
__COOKIE__ = {'_account_center_session' : os.environ.get('COOKIE') or ''}


class Song:

    def __init__(self, id, name, yt, spotify):
        self.id = id
        self.name = name
        self.yt = yt
        self.spotify = spotify

def get_songs():

    param = '?per_page=100'
    urlpath = f'{__URL__}{param}'
    r = requests.get(urlpath, auth=requests.auth.HTTPBasicAuth(__ID__,__SECRET__))
    j = r.json()
    s_total = j['meta']['total_count']
    s_list = []

    while len(s_list) < s_total:
        for song in j.get('data'):

            # Create Song
            s_obj = Song(song['id'], song['attributes']['title'], [], [])

            s_list.append(s_obj)
        if (j['links'].get('next')):
            r = requests.get(j['links']['next'], auth=requests.auth.HTTPBasicAuth(__ID__,__SECRET__))
            j = r.json()

    return s_list

def get_song_attachments(song_obj):

    s_id = str(song_obj.id)
    s_name = song_obj.name
    print(f'[{s_id}] {s_name}')

    param = f'{s_id}/attachments?per_page=100'
    urlpath = f'{__URL__}{param}'

    r1 = requests.get(urlpath, auth=requests.auth.HTTPBasicAuth(__ID__,__SECRET__))
    j1 = r1.json()

    for a in j1.get('data'):
        # AttachmentSpotify or AttachmentYoutube or AttachmentLink
        pco = str(a['attributes']['pco_type'])
        if (pco == 'AttachmentYoutube'):
            get_url_from_attachment('yt', a, song_obj)
        elif (pco == 'AttachmentSpotify'):
            get_url_from_attachment('sp', a, song_obj)
        # elif (pco == 'AttachmentLink'):
            #link_url = str(a['attributes']['remote_link'])
            #print(f'Link: {link_url}')

    print('+++')

    param2 = f'{s_id}/arrangements?per_page=100'
    urlpath2 = f'{__URL__}{param2}'

    r2 = requests.get(urlpath2, auth=requests.auth.HTTPBasicAuth(__ID__,__SECRET__))
    j2 = r2.json()

    for ar in j2.get('data'):
        ar_id = str(ar['id'])

        param3 = f'{s_id}/arrangements/{ar_id}/attachments?per_page=100'
        urlpath3 = f'{__URL__}{param3}'

        r3 = requests.get(urlpath3, auth=requests.auth.HTTPBasicAuth(__ID__,__SECRET__))
        j2 = r3.json()

        for a in j2.get('data'):
             # AttachmentSpotify or AttachmentYoutube or AttachmentLink
            pco = str(a['attributes']['pco_type'])
            if (pco == 'AttachmentYoutube'):
                get_url_from_attachment('yt', a, song_obj)
            elif (pco == 'AttachmentSpotify'):
                get_url_from_attachment('sp', a, song_obj)
            elif (pco == 'AttachmentLink'):
                link_url = str(a['attributes']['remote_link'])
                print(f'Link: {link_url}')

    print('-------------------')
    return 0

def get_url_from_attachment(urltype, a, song_obj):
    if (a['attributes']['remote_link']):
        link_url = str(a['attributes']['remote_link'])
        if (urltype == 'yt'):
            song_obj.yt.append(link_url)
            print(f'Youtube: {link_url}')
        elif (urltype == 'sp'):
            song_obj.spotify.append(link_url)
            print(f'Spotify: {link_url}')

    else:
        urlpath = str(a['attributes']['url'])
        # Hack to allow access to attachments
        r2 = requests.get(urlpath, cookies=__COOKIE__)
        link_url = str(r2.url)
        if (urltype == 'yt'):
            song_obj.yt.append(link_url)
            print(f'Youtube: {link_url}')
        elif (urltype == 'sp'):
            song_obj.spotify.append(link_url)
            print(f'Spotify: {link_url}')

songs = get_songs()
for song in songs:
    get_song_attachments(song)
