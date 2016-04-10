#!/usr/bin/python3

# (C) Oliver Diedrich, oliver.die@gmail.com. Feel free to use as you like. No warranty.

# lists all the albums in your google play music collection and lets you delete them with one key stroke

# needs gmusicapi, install it with pip

# ENTER YOUR ACCOUNT DATA BELOW. If you're using 2 factor authentication, you need to create an app-specific password (https://security.google.com/settings/security/apppasswords)


from gmusicapi import Mobileclient
import csv

USER = 'YOUR.ACCOUNT@GMAIL.COM'
PASS = 'PASSWORD'

class Album(object):      # holds all the relevant data for one album 
  def __init__(self, album):
    self.album = album
    self.title = []       # list of titles of this album
    self.artist = []      # could be a sampler with... 
    self.genre = []       # ...different artists and genres
    self.ID = []          # id is needed to remove a song
  
  def add(self, artist, genre, title, ID):   # add a song to the album
    self.artist.append(artist)
    self.genre.append(genre)
    self.title.append(title)
    self.ID.append(ID)


all_albums = {}          # dict of albums, indexed by album name
n = 0                    # counts the songs
api = Mobileclient()     # Mobileclient is the simple gmusicapi interface

if api.login(USER, PASS, Mobileclient.FROM_MAC_ADDRESS):
  songs = api.get_all_songs()
  for i in songs:                          # iterate across the songs
    if i['album'] == '':                   # no album title, artist, song title? invent one
      i['album'] = 'ALBUM-' + str(n)
    if i['artist'] == '':
      i['artist'] = 'ARTIST-' + str(n)
    if i['title'] == '':
      i['title'] = 'TITLE-' + str(n)
    try:                                   # try to add song to existing album
    	all_albums[i['album']].add(i['artist'], i['genre'], i['title'], i['id'])
#    	print('>>> added', i['title'], 'to album', i['album'])
    except:                                # no album exists -> create it, then add song
    	all_albums[i['album']] = Album(i['album'])
    	all_albums[i['album']].add(i['artist'], i['genre'], i['title'], i['id'])
#    	print('>>> created', i['album'], '(' + i['artist'] + ')')
    n += 1
else:
  print('login for', USER, 'failed')

print('read', n, 'songs in', len(all_albums), 'albums')

for a in sorted(all_albums):        # across all albums    
  i = all_albums[a]
  print(i.artist[0], ':', i.album, '('+i.genre[0]+')')   # Artist : Album (Genre)
  for t in i.title:                 # list all titles of the album
    print('\t', t)

  rm = input("Delete album? (y/n)? ")
  if rm == 'y':
    ret = api.delete_songs(i.ID)    # delete all songs of the album
    print(ret, 'deleted')
    print()

