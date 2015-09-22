from pytz import _CountryNameDict

__author__ = 'dhiraj'

from recsys.algorithm.dbconn import DBConn

db = DBConn()
filename = "/home/dhiraj/projects/resources/data/people"

genres = ['alternative', 'acoustic', 'accoustic', 'blues', 'classical', 'country', 'dance', 'dj', 'electronica', 'folk', 'gospel', 'hip hop', 'hiphop', 'house', 'indie', 'instrumental', 'jazz', 'metal', 'pop', 'r&b', 'rnb', 'rap', 'reggae', 'rock', 'soul']

count = 0

with open(filename, 'r') as myFile:
    for line in myFile:
        line = line.split(',')
        USER_ID = line[0].encode('utf-8').replace('\n', '')

        alternative = 0
        acoustic = 0
        blues = 0
        classical = 0
        country = 0
        dance = 0
        dj = 0
        electronica = 0
        folk = 0
        gospel = 0
        hiphop = 0
        house = 0
        indie = 0
        instrumental = 0
        jazz = 0
        metal = 0
        pop = 0
        rnb = 0
        reggae = 0
        rock = 0
        rap = 0
        soul = 0

        if str(line[1]).encode('utf-8 ').replace('\n', '') == 'Italy' or str(line[1]).encode('utf-8 ').replace('\n', '') == 'Cyprus' or \
            str(line[1]).encode('utf-8 ').replace('\n', '') == 'Ireland' or str(line[1]).encode('utf-8 ').replace('\n', '') == 'Spain' or \
            str(line[1]).encode('utf-8 ').replace('\n', '') == 'Libya' or str(line[1]).encode('utf-8 ').replace('\n', '') == 'Greece' or \
            str(line[1]).encode('utf-8 ').replace('\n', '') == 'Mexico' or str(line[1]).encode('utf-8 ').replace('\n', '') == 'USA':
            liked = db.get_liked_artists_eval2(user_id=USER_ID)
            for item in liked:
                get_artist = db.get_reverbnation_artist(artist_id=str(item['artist_id']).encode('utf-8'))
                if get_artist['genres'] > 0:
                    for genre in get_artist['genres']:
                        if 'alternative' in genre.lower():
                            alternative += 1
                            #alternative_found = True
                        elif ('acoustic' in genre.lower() or 'accoustic' in genre.lower()):
                            acoustic += 1
                            #acoustic_found = True
                        elif 'blues' in genre.lower():
                            blues += 1
                            #blues_found = True
                        elif 'classical' in genre.lower():
                            classical += 1
                            #classical_found = True
                        elif 'country' in genre.lower():
                            country += 1
                            #country_found = True
                        elif 'dance' in genre.lower():
                            dance += 1
                            #dance_found = True
                        elif 'dj' in genre.lower():
                            dj += 1
                            #dj_found = True
                        elif 'electronica' in genre.lower():
                            electronica += 1
                            #electronica_found = True
                        elif 'folk' in genre.lower():
                            folk += 1
                            #folk_found = True
                        elif 'gospel' in genre.lower():
                            gospel += 1
                            #gospel_found = True
                        elif ('hiphop' in genre.lower() or 'hip hop' in genre.lower()):
                            hiphop += 1
                            #hiphop_found = True
                        elif 'house' in genre.lower():
                            house += 1
                            #house_found = True
                        elif 'indie' in genre.lower():
                            indie += 1
                            #indie_found = True
                        elif 'instrumental' in genre.lower():
                            instrumental += 1
                            #instrumental_found = True
                        elif 'jazz' in genre.lower():
                            jazz += 1
                            #jazz_found = True
                        elif 'metal' in genre.lower():
                            metal += 1
                            #metal_found = True
                        elif 'pop' in genre.lower():
                            pop += 1
                            #pop_found = True
                        elif ('r&b' in genre.lower() or 'rnb' in genre.lower()):
                            rnb += 1
                            #rnb_found = True
                        elif 'rap' in genre.lower():
                            rap += 1
                            #rap_found = True
                        elif 'reggae' in genre.lower():
                            reggae += 1
                            #reggae_found = True
                        elif 'rock' in genre.lower():
                            rock += 1
                            #rock_found = True
                        elif 'soul' in genre.lower():
                            soul += 1
                            #soul_found = True
            sum_genres = alternative + acoustic + blues + classical + country + dance + dj + electronica + \
                            folk + gospel + hiphop + house + indie + instrumental + jazz + metal + pop + rnb + \
                            rap + reggae + rock + soul
            if sum_genres > 0:

                print "Germany,", "Alternative,", ((float(alternative) / float(sum_genres)) * 100.0)
                print "Germany,", "Acoustic,", ((float(acoustic) / float(sum_genres)) * 100.0)
                print "Germany,", "Blues,", ((float(blues) / float(sum_genres)) * 100.0)
                print "Germany,", "Classical,", ((float(classical) / float(sum_genres)) * 100.0)
                print "Germany,", "Country,", ((float(country) / float(sum_genres)) * 100.0)
                print "Germany,", "Dance,", ((float(dance) / float(sum_genres)) * 100.0)
                print "Germany,", "DJ,", ((float(dj) / float(sum_genres)) * 100.0)
                print "Germany,", "Electronica,", ((float(electronica) / float(sum_genres)) * 100.0)
                print "Germany,", "Folk,", ((float(folk) / float(sum_genres)) * 100.0)
                print "Germany,", "Gospel,", ((float(gospel) / float(sum_genres)) * 100.0)
                print "Germany,", "Hip Hop,", ((float(hiphop) / float(sum_genres)) * 100.0)
                print "Germany,", "House,", ((float(house) / float(sum_genres)) * 100.0)
                print "Germany,", "Indie,", ((float(indie) / float(sum_genres)) * 100.0)
                print "Germany,", "Instrumental,", ((float(instrumental) / float(sum_genres)) * 100.0)
                print "Germany,", "Jazz,", ((float(jazz) / float(sum_genres)) * 100.0)
                print "Germany,", "Metal,", ((float(metal) / float(sum_genres)) * 100.0)
                print "Germany,", "Pop,", ((float(pop) / float(sum_genres)) * 100.0)
                print "Germany,", "R&B,", ((float(rnb) / float(sum_genres)) * 100.0)
                print "Germany,", "Rap,", ((float(rap) / float(sum_genres)) * 100.0)
                print "Germany,", "Reggae,", ((float(reggae) / float(sum_genres)) * 100.0)
                print "Germany,", "Rock,", ((float(rock) / float(sum_genres)) * 100.0)
                print "Germany,", "Soul,", ((float(soul) / float(sum_genres)) * 100.0)
                count += 1

myFile.close()
print count