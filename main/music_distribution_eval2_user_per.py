__author__ = 'dhiraj'

from recsys.algorithm.dbconn import DBConn

db = DBConn()
filename = "/home/dhiraj/projects/resources/data/people"

genres = ['alternative', 'acoustic', 'accoustic', 'blues', 'classical', 'country', 'dance', 'dj', 'electronica', 'folk', 'gospel', 'hip hop', 'hiphop', 'house', 'indie', 'instrumental', 'jazz', 'metal', 'pop', 'r&b', 'rnb', 'rap', 'reggae', 'rock', 'soul']
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
count = 0
with open(filename, 'r') as myFile:
    for line in myFile:
        alternative_found = False
        acoustic_found = False
        blues_found = False
        classical_found = False
        country_found = False
        dance_found = False
        dj_found = False
        electronica_found = False
        folk_found = False
        gospel_found = False
        hiphop_found = False
        house_found = False
        indie_found = False
        instrumental_found = False
        jazz_found = False
        metal_found = False
        pop_found = False
        rnb_found = False
        reggae_found = False
        rock_found = False
        rap_found = False
        soul_found = False
        found = False
        USER_ID = line.encode('utf-8').replace('\n', '')
        feedback = db.get_live_feedback_eval_2_user(user_id=USER_ID)
        for item in feedback:
           found = True
           get_artist = db.get_reverbnation_artist(artist_id=str(item['artist_id']).encode('utf-8'))
           if get_artist['genres'] > 0:
                for genre in get_artist['genres']:
                    if 'alternative' in genre.lower() and not alternative_found:
                        alternative += 1
                        alternative_found = True
                    elif ('acoustic' in genre.lower() or 'accoustic' in genre.lower()) and not acoustic_found:
                        acoustic += 1
                        acoustic_found = True
                    elif 'blues' in genre.lower() and not blues_found:
                        blues += 1
                        blues_found = True
                    elif 'classical' in genre.lower() and not classical_found:
                        classical += 1
                        classical_found = True
                    elif 'country' in genre.lower() and not country_found:
                        country += 1
                        country_found = True
                    elif 'dance' in genre.lower() and not dance_found:
                        dance += 1
                        dance_found = True
                    elif 'dj' in genre.lower() and not dj_found:
                        dj += 1
                        dj_found = True
                    elif 'electronica' in genre.lower() and not electronica_found:
                        electronica += 1
                        electronica_found = True
                    elif 'folk' in genre.lower() and not folk_found:
                        folk += 1
                        folk_found = True
                    elif 'gospel' in genre.lower() and not gospel_found:
                        gospel += 1
                        gospel_found = True
                    elif ('hiphop' in genre.lower() or 'hip hop' in genre.lower()) and not hiphop_found:
                        hiphop += 1
                        hiphop_found = True
                    elif 'house' in genre.lower() and not house_found:
                        house += 1
                        house_found = True
                    elif 'indie' in genre.lower() and not indie_found:
                        indie += 1
                        indie_found = True
                    elif 'instrumental' in genre.lower() and not instrumental_found:
                        instrumental += 1
                        instrumental_found = True
                    elif 'jazz' in genre.lower() and not jazz_found:
                        jazz += 1
                        jazz_found = True
                    elif 'metal' in genre.lower() and not metal_found:
                        metal += 1
                        metal_found = True
                    elif 'pop' in genre.lower() and not pop_found:
                        pop += 1
                        pop_found = True
                    elif ('r&b' in genre.lower() or 'rnb' in genre.lower()) and not rnb_found:
                        rnb += 1
                        rnb_found = True
                    elif 'rap' in genre.lower() and not rap_found:
                        rap += 1
                        rap_found = True
                    elif 'reggae' in genre.lower() and not reggae_found:
                        reggae += 1
                        reggae_found = True
                    elif 'rock' in genre.lower() and not rock_found:
                        rock += 1
                        rock_found = True
                    elif 'soul' in genre.lower() and not soul_found:
                        soul += 1
                        soul_found = True
        if found:
            count += 1

print "Alternative, %s" % ((float(alternative) / float(count)) * 100.0)
print "Acoustic, %s" % ((float(acoustic) / float(count)) * 100.0)
print "Blues, %s" % ((float(blues) / float(count)) * 100.0)
print "Classical, %s" % ((float(classical) / float(count)) * 100.0)
print "Country, %s" % ((float(country) / float(count)) * 100.0)
print "Dance, %s" % ((float(dance) / float(count)) * 100.0)
print "DJ, %s" % ((float(dj) / float(count)) * 100.0)
print "Electronica, %s" % ((float(electronica) / float(count)) * 100.0)
print "Folk, %s" % ((float(folk) / float(count)) * 100.0)
print "Gospel, %s" % ((float(gospel) / float(count)) * 100.0)
print "Hip Hop, %s" % ((float(hiphop) / float(count)) * 100.0)
print "House, %s" % ((float(house) / float(count)) * 100.0)
print "Indie, %s" % ((float(indie) / float(count)) * 100.0)
print "Instrumental, %s" % ((float(instrumental) / float(count)) * 100.0)
print "Jazz, %s" % ((float(jazz) / float(count)) * 100.0)
print "Metal, %s" % ((float(metal) / float(count)) * 100.0)
print "Pop, %s" % ((float(pop) / float(count)) * 100.0)
print "R&B, %s" % ((float(rnb) / float(count)) * 100.0)
print "Rap, %s" % ((float(rap) / float(count)) * 100.0)
print "Reggae, %s" % ((float(reggae) / float(count)) * 100.0)
print "Rock, %s" % ((float(rock) / float(count)) * 100.0)
print "Soul, %s" % ((float(soul) / float(count)) * 100.0)


