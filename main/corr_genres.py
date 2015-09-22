from recsys.algorithm.dbconn import DBConn

db = DBConn()

filename = "/home/dhiraj/projects/resources/data/people"
count = 0

predefined_genres = ['alternative', 'acoustic', 'accoustic', 'blues', 'classical', 'country', 'dance', 'dj', 'electronica', 'folk', 'gospel', 'hip hop', 'hiphop', 'house', 'indie', 'instrumental', 'jazz', 'metal', 'pop', 'r&b', 'rnb', 'rap', 'reggae', 'rock', 'soul']
with open(filename, 'r') as myFile:
    for line in myFile:
        line = line.split(',')
        USER_ID = line[0].encode('utf-8').replace('\n', '')
        artists = db.get_artists_eval2(user_id=USER_ID)
        rec_genres = []
        if artists.count() > 0:
            for artist in artists:
                get_artist = db.get_reverbnation_artist(artist_id=str(artist['artist_id']).encode('utf-8'))
                if get_artist['genres'] > 0:
                    for genre in get_artist['genres']:
                        if genre.lower() in predefined_genres and genre.lower() not in rec_genres:
                            rec_genres.append(genre.lower())
            if len(rec_genres) > 0:
                user_genres = db.get_genres(user_id=USER_ID)
                chosen_genres = []
                for genre in user_genres['genres']:
                    if genre.lower() in predefined_genres:
                        chosen_genres.append(genre.lower())
                if len(chosen_genres) > 0:
                    inter = set(chosen_genres).intersection(rec_genres)
                    print str(len(chosen_genres)) + "," + str(len(inter))
            count += 1
print count