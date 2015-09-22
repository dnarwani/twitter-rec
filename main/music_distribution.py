__author__ = 'dhiraj'

import sys
from recsys.algorithm.dbconn import DBConn
from recsys.algorithm.functions import Functions
from recsys.algorithm.baseline import Baseline
try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict

reload(sys)
sys.setdefaultencoding("utf-8")

db = DBConn()
myFunctions = Functions()

artists = db.get_artists_soundcloud()

genres = ['alternative', 'acoustic', 'accoustic', 'blues', 'classical', 'country', 'dance', 'dj', 'electronica', 'folk', 'gospel', 'hip hop', 'hiphop', 'house', 'indie', 'instrumental', 'jazz', 'metal', 'pop', 'r&b', 'rnb', 'rap', 'reggae', 'rock', 'soul']
filename = '/home/dhiraj/projects/resources/data/genres_artist_distinct_count.txt'
inc = 0

with open(filename, 'w') as myFile:
    for artist in artists:
        inc += 1
        print inc
        dict_authors = []
        found = 0
        artist_distinct_count = OrderedDict()
        artist_distinct_count['1-9'] = 0
        artist_distinct_count['10-20'] = 0
        artist_distinct_count['20-30'] = 0
        artist_distinct_count['30-40'] = 0
        artist_distinct_count['40-50'] = 0
        artist_distinct_count['50-60'] = 0
        artist_distinct_count['60-70'] = 0
        artist_distinct_count['70-80'] = 0
        artist_distinct_count['80-90'] = 0
        artist_distinct_count['90-100'] = 0
        artist_distinct_count['100-110'] = 0
        artist_distinct_count['120-860'] = 0

        get_artist = db.get_reverbnation_artist(artist_id=str(artist['artist_id']).encode('utf-8'))
        if get_artist['genres'] > 0:
            for genre in get_artist['genres']:
                if any(ext in str(genre).encode('utf-8').lower() for ext in genres):
                    found = 1
                    break
            if found == 1:
                if len(get_artist['handles']) > 0:
                    for handle in get_artist['handles']:
                        objHandle = db.get_handle_artist(handle=handle)
                        if objHandle:
                            authors = db.get_authors(handle_id=objHandle['_id'])
                            for author in authors:
                                if str(author['_id']).encode('utf-8') not in dict_authors:
                                    user = db.get_user_id(USER_ID=author['_id']['author_id'])
                                    if user:
                                        if 'artist_distinct_count' in user and user['artist_distinct_count'] > 0:
                                            artist_count = user['artist_distinct_count']
                                            if artist_count >= 1 and artist_count <= 9:
                                                artist_distinct_count['1-9'] += 1
                                            elif artist_count >= 10 and artist_count < 20:
                                                artist_distinct_count['10-20'] += 1
                                            elif artist_count >= 20 and artist_count < 30:
                                                artist_distinct_count['20-30'] += 1
                                            elif artist_count >= 30 and artist_count < 40:
                                                artist_distinct_count['30-40'] += 1
                                            elif artist_count >= 40 and artist_count < 50:
                                                artist_distinct_count['40-50'] += 1
                                            elif artist_count >= 50 and artist_count < 60:
                                                artist_distinct_count['50-60'] += 1
                                            elif artist_count >= 60 and artist_count < 70:
                                                artist_distinct_count['60-70'] += 1
                                            elif artist_count >= 70 and artist_count < 80:
                                                artist_distinct_count['70-80'] += 1
                                            elif artist_count >= 80 and artist_count < 90:
                                                artist_distinct_count['80-90'] += 1
                                            elif artist_count >= 90 and artist_count < 100:
                                                artist_distinct_count['90-100'] += 1
                                            elif artist_count >= 100 and artist_count < 110:
                                                artist_distinct_count['100-110'] += 1
                                            elif artist_count >= 120 and artist_count < 900:
                                                artist_distinct_count['120-860'] += 1
                                            dict_authors.append(str(author['_id']).encode('utf-8'))
                    for genre in get_artist['genres']:
                        if 'alternative' in genre.lower():
                            genre_name = 'Alternative'
                        elif 'acoustic' in genre.lower() or 'accoustic' in genre.lower():
                            genre_name = 'Acoustic'
                        elif 'blues' in genre.lower():
                            genre_name = 'Blues'
                        elif 'classical' in genre.lower():
                            genre_name = 'Classical'
                        elif 'country' in genre.lower():
                            genre_name = 'Country'
                        elif 'dance' in genre.lower():
                            genre_name = 'Dance'
                        elif 'dj' in genre.lower():
                            genre_name = 'DJ'
                        elif 'electronica' in genre.lower():
                            genre_name = 'Electronica'
                        elif 'folk' in genre.lower():
                            genre_name = 'Folk'
                        elif 'gospel' in genre.lower():
                            genre_name = 'Gospel'
                        elif 'hiphop' in genre.lower() or 'hip hop' in genre.lower():
                            genre_name = 'Hip Hop'
                        elif 'house' in genre.lower():
                            genre_name = 'House'
                        elif 'indie' in genre.lower():
                            genre_name = 'Indie'
                        elif 'instrumental' in genre.lower():
                            genre_name = 'Instrumental'
                        elif 'jazz' in genre.lower():
                            genre_name = 'Jazz'
                        elif 'metal' in genre.lower():
                            genre_name = 'Metal'
                        elif 'pop' in genre.lower():
                            genre_name = 'Pop'
                        elif 'r&b' in genre.lower() or 'rnb' in genre.lower():
                            genre_name = 'R&B'
                        elif 'rap' in genre.lower():
                            genre_name = 'Rap'
                        elif 'reggae' in genre.lower():
                            genre_name = 'Reggae'
                        elif 'rock' in genre.lower():
                            genre_name = 'Rock'
                        elif 'soul' in genre.lower():
                            genre_name = 'Soul'

                        if genre_name:
                            if artist['soundcloud'] == 0:
                                soundcloud = 'Sound Cloud'
                            else:
                                soundcloud = 'Not on SoundCloud'

                            for name, count in artist_distinct_count.iteritems():
                                myFile.write(str(genre_name) + ',' + str(name) + ',' + str(count) + ',' + str(soundcloud) + "\n")
myFile.close()

