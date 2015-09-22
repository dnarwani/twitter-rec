__author__ = 'dhiraj'

import codecs
import time
import cPickle
import pickle
from itertools import islice
import tweepy
import operator

from bson.objectid import ObjectId
import numpy as np
import divisi2

from recsys.datamodel.data import Data
from recsys.datamodel.item import Item
from recsys.algorithm import dbconn
from recsys.algorithm.baseline import Baseline
from recsys.algorithm.dbconn import DBConn

class Functions(object):

    def _read_items_from_fs(self, filename):
        items = dict()
        for line in codecs.open(filename, 'r', 'utf8'):
            data = line.strip('\r\n').split("::")
            item_id = data[0]
            if len(data) > 1:
                item_name = data[1]
            if len(data) > 2:
                str_genres = data[2]
            genres = []
            for genre in str_genres.split('|'):
                genres.append(genre)
            items[item_id] = Item(item_id)
            items[item_id].add_data({'name': item_name, 'genres': genres})
        return items

    def _read_items(self, filename):
        items = dict()
        for line in filename.splitlines():
            #1::Toy Story (1995)::Animation|Children's|Comedy
            data = line.split('::')
            item_id = data[0]
            if len(data) > 1:
                item_name = data[1]
            if len(data) > 2:
                str_genres = data[2]
            genres = []
            for genre in str_genres.split('|'):
                genres.append(genre)
            items[item_id] = Item(item_id)
            items[item_id].add_data({'name': item_name, 'genres': genres})
        return items

    def insert_people_into_dat(self, filename):
        db = dbconn.DBConn()
        people = db.get_people()

        with open(filename, 'w') as myFile:
            for person in people:
                _id = ('Unknown' if not person['_id'] else str(person['_id']).encode("utf-8"))
                id_str = ('Unknown' if not person['id_str'] else str(person['id_str']).encode("utf-8"))
                name = ('Unknown' if not person['screen_name'] else str(person['screen_name']).encode("utf-8"))
                location = ('Unknown' if not person['location'] else str(person['location']).encode("utf-8"))
                lang = ('Unknown' if not person['lang'] else str(person['lang']).encode("utf-8"))
                myFile.write(_id + "::" + id_str + "::" + name + "::" + location + "::" + lang + "\n")
        myFile.close()


    def insert_reverb_artists_into_dat(self, filename):
        db = dbconn.DBConn()
        artists = db.get_reverbnation_artists()

        with open(filename, 'w') as myFile:
            for artist in artists:
                count = 0
                str_genres = 'Unknown'
                for genre in artist["genres"]:
                    if count == 0:
                        str_genres = genre
                    else:
                        str_genres += "|" + genre
                    count += 1

                _id = ('Unknown' if not artist['_id'] else str(artist['_id']).encode("utf-8"))
                name = ('Unknown' if not artist['name'] else str(artist['name']).encode("utf-8"))

                myFile.write(_id + "::" + name + "::" + str_genres + "\n")
        myFile.close()

    def insert_genres_into_dat(self, filename):
        db = dbconn.DBConn()
        artists = db.get_reverbnation_artists()

        with open(filename, 'w') as myFile:
            for artist in artists:
                count = 0
                str_genres = 'Unknown'
                for genre in artist["genres"]:
                    if count == 0:
                        str_genres = genre
                    else:
                        str_genres += "," + genre
                    count += 1

                myFile.write(str_genres + "\n")
        myFile.close()

    def create_count_dict_pickle(self, db):
        count_dict = dict()

        print "Querying database for author counts..."
        author_counts = list(db.get_tweet_count())

        print "Creating dictionary of counts..."
        for author in author_counts:
            count_dict[str(author["_id"]["author_id"])] = author["count"]

        print "Create cPickle file..."
        cPickle.dump(count_dict, open("../recmusic/recsys/data/count_dict.p", "wb"))

        print "cPickle created..."

    def create_artist_count_pickle(self, db):
        occurrences = dict()
        print "Loading tweet cPickle..."
        tweet_dict = cPickle.load(open("../recmusic/recsys/data/tweets.p", "rb"))

        print "Create dictionary of occurrences..."
        for tweet in tweet_dict.keys():
            objHandle = db.get_handle(handle_id=ObjectId(tweet[0]))
            if objHandle:
                artist = db.get_reverbnation_artists_by_handle(str(objHandle["handle"]).encode("utf-8"))
                if artist:
                    if (str(artist["_id"]), str(tweet[1])) in occurrences:
                        occurrences[(str(artist["_id"])), str(tweet[1])] += int(tweet_dict[tweet])
                    else:
                        occurrences[(str(artist["_id"])), str(tweet[1])] = tweet_dict[tweet]

        print "Create cPickle file..."
        cPickle.dump(occurrences, open("../recmusic/recsys/data/occurrences.p", "wb"))

        print "cPickle created..."

    def create_tweet_pickle(self, db):
        tweets_dict = dict()

        print "Querying database for tweets..."
        tweets = db.get_tweets()

        print "Create dictionary of tweets..."
        for tweet in tweets:
            tweets_dict[(str(tweet["_id"]["handle_id"]), str(tweet["_id"]["author_id"]))] = tweet["count"]

        print "Create cPickle file..."
        cPickle.dump(tweets_dict, open("../recmusic/recsys/data/tweets.p", "wb"))

        print "cPickle created..."

    def insert_tweet_occurrences_into_dat(self, filename, db):
        occurrences = dict()

        print "Loading occurrence matrix..."
        occurrences = cPickle.load(open("../recmusic/recsys/data/occurrences.p", "rb"))

        print "Writing to file ..."
        with open(filename, 'w') as myFile:
            for (artist_id, author_id), count in occurrences.iteritems():
                print int(count)
                myFile.write(str(author_id).encode("utf-8") + "::" + str(artist_id).encode("utf-8") +
                             "::" + str(int(count)).encode("utf-8") + "::" +
                             str(int(time.time())).encode("utf-8") + "\n")
        myFile.close()
        print "Done"

    def insert_ld_occurrences_into_dat(self, filename, db):

        feedback = db.get_live_feedback()
        functions = Functions()

        with open(filename, 'w') as myFile:
            for item in feedback:
                myFile.write(str(item['user_id']).encode("utf-8") + "::" + str(item['artist_id']).encode("utf-8") +
                             "::" + str(int(item['like_dislike'])).encode("utf-8") + "::" +
                             str(int(time.time())).encode("utf-8") + "\n")

            # USER_ID = '55c93efd8587b261f4b70d3e'
            # artists_users = db.get_live_feedback_user(USER_ID)
            # exist_artists = []
            # for artist_user in artists_users:
            #     exist_artists.append(str(artist_user['artist_id']).encode('utf-8'))
            #
            # items = db.get_artist_labels()
            # for artist_id in items:
            #     if str(artist_id['artist_id']).encode('utf-8') not in exist_artists:
            #         myFile.write(USER_ID + "::" + str(artist_id['artist_id']).encode("utf-8") +
            #                  "::0::" +str(int(time.time())).encode("utf-8") + "\n")
            #     else:
            #         x = 1
        myFile.close()

    def parallel_function(self, f):
        def easy_parallize(f, sequence):
            """ assumes f takes sequence as input, easy w/ Python's scope """
            from multiprocessing import Pool
            pool = Pool(processes=4) # depends on available cores
            result = pool.map(f, sequence) # for i in sequence: result[i] = f(i)
            cleaned = [x for x in result if not x is None] # getting results
            cleaned = np.asarray(cleaned)
            pool.close() # not optimal! but easy
            pool.join()
            return cleaned
        from functools import partial
        return partial(easy_parallize, f)

    def output_confusion_matrix(self, ground_truth, test):
        TP, FP, TN, FN = (0, 0, 0, 0)
        lst_ground_truth = list(ground_truth)
        for item in test:
            if item in lst_ground_truth:
                TP += 1
                lst_ground_truth.pop(lst_ground_truth.index(item))
            else:
                FP += 1
        FN = len(lst_ground_truth)
        return TP, FP, TN, FN

    def take(self, n, iterable):
        "Return first n items of the iterable as a list"
        return list(islice(iterable, 1, n + 1))

    def update(self, USER_ID, baseline, path, pred_items):
        print "Loading tweet occurrences cPickle..."
        baseline.get_data()._load_cPickle(path=path + "tweet_occurrences.p")
        tweet_occurrences = baseline.get_data().get()

        print "Loading count_dict cPickle..."
        count_dict = cPickle.load(open(path + "count_dict.p"))

        print "Loading occurrences cPickle..."
        occurrences = cPickle.load(open(path + "occurrences.p"))

        total_count = count_dict[USER_ID]
        upd_total_count = int(total_count) + len(pred_items)
        count_dict[USER_ID] = int(upd_total_count)

        print "Dumping count_dict cPickle..."
        cPickle.dump(count_dict, open(path + "count_dict.p", "wb"), 2)

        print "Updating counts for known artists..."
        for index, (count, item_id, user_id) in enumerate(tweet_occurrences):
            if str(user_id).encode('utf-8') == USER_ID:
                item_id = str(item_id).encode('utf-8')
                count = occurrences[(item_id, USER_ID)]
                upd_count = float(count) / float(upd_total_count)

                occurrences[(item_id, USER_ID)] = float(upd_count)
                baseline._matrix.set_value(item_id, USER_ID, float(upd_count))
                tweet_occurrences[index] = (float(upd_count), item_id, user_id)

        print "Updating counts for recommended artists..."
        for item_id, relevance in pred_items:
            count = (1.0 / float(upd_total_count))
            baseline._matrix.set_value(item_id, USER_ID, float(count))
            occurrences[(item_id, USER_ID)] = float(count)
            tweet_occurrences.append((float(count), item_id, USER_ID))

        print "Dumping tweet occurrences cPickle..."
        data_tweet_occurrences = Data()
        data_tweet_occurrences.set(tweet_occurrences)

        baseline.set_data(data_tweet_occurrences)
        baseline.save_data(filename=path + "tweet_occurrences.p", cPickle=True)

        print "Dumping occurrence cPickle..."
        cPickle.dump(occurrences, open(path + "occurrences.p", "wb"), protocol=2)

        print "Dumping sparse matrix cPickle..."
        cPickle.dump(baseline._matrix.get(), open(path + "sparse_matrix.p", "w"), protocol=2)

        # print "Updating matrix..."
        # baseline.compute(k=100, min_values=None, pre_normalize=None, mean_center=False, post_normalize=True)

    def insert_svd_into_db(self, svd):
        db = DBConn()

        for s in np.ndenumerate(svd._S):
            s_list = list(s)
            db.insert_into_s_matrix(s_list[0], s_list[1])

        for u in list(svd._U):
            db.insert_into_u_matrix(list(u))

        index = 0
        for v in list(svd._V):
            db.insert_into_v_matrix(index, list(v))
            index += 1

    def compute_v_vectors(self, col_index):
        db = DBConn()

        _V = db.get_V_matrix(col_index)
        v_vectors = []
        array = np.asarray(_V[0]["array"])
        v_vectors.append(divisi2.from_ndarray(array))
        return v_vectors

    def get_popular_artists(self, db):
        import operator
        occurrences = dict()
        print "Loading tweet cPickle..."
        tweet_dict = cPickle.\
            load(open("/home/dhiraj/projects/resources/data/tweets.p", "rb"))
        count = 0
        print "Create dictionary of occurrences..."
        for tweet in tweet_dict.keys():
            objHandle = db.get_handle(handle_id=ObjectId(tweet[0]))
            if objHandle:
                artist = db.\
                    get_reverbnation_artists_by_handle(str(objHandle["handle"]).
                                                       encode("utf-8"))
                if artist:
                    exists = db.\
                        check_artist_in_soundcloud(str(artist["_id"]).encode('utf-8'))
                    if exists:
                        if (str(artist["_id"]), str(tweet[1])) in occurrences:
                            occurrences[(str(artist["_id"])), str(tweet[1])] += 1
                        else:
                            occurrences[(str(artist["_id"])), str(tweet[1])] = 1
                        count += 1
                        print count

        print "Create dictionary of artist occurrences..."
        artist_occurences = dict()
        for occurence in occurrences.keys():
            if occurence[0] in artist_occurences:
                artist_occurences[occurence[0]] += int(occurrences[occurence])
            else:
                artist_occurences[occurence[0]] = occurrences[occurence]

        sorted_occurences = sorted(artist_occurences.items(),
                                   key=operator.itemgetter(1), reverse=True)
        return sorted_occurences


    def get_top_friends(self, friends_ids, db, screen_name):
        ids = dict()
        top_5_ids = dict()
        for twitter_handle in tweepy.Cursor(friends_ids,
                                            screen_name=screen_name).items():
            try:
                user = db.get_person(twitter_handle)
                if user is not None and 'artist_distinct_count' in user:
                    ids[user["_id"]] = int(user["artist_distinct_count"])
            except tweepy.TweepError:
                break
            except StopIteration:
                break
        if len(ids) > 0:
            top_5_ids = sorted(ids.items(),
                               key=operator.itemgetter(1), reverse=True)[:5]

        return top_5_ids

    def get_top_followers(self, follower_ids, db, screen_name):
        ids = dict()
        top_5_ids = dict()
        for twitter_handle in tweepy.Cursor(follower_ids,
                                            screen_name=screen_name).items():
            try:
                user = db.get_person(twitter_handle)
                if user is not None and 'artist_distinct_count' in user:
                    ids[user["_id"]] = int(user["artist_distinct_count"])
            except tweepy.TweepError:
                break
            except StopIteration:
                break

        if len(ids) > 0:
            top_5_ids = sorted(ids.items(),
                               key=operator.itemgetter(1), reverse=True)[:5]

        return top_5_ids

    def get_ranked_followers_friends(self, final_items):
        unique_items = dict()
        for (artist_id, weight) in final_items:
            if artist_id in unique_items:
                new_weight = unique_items[artist_id][0]
                new_occurence_count = unique_items[artist_id][1]
                new_weight += weight
                new_occurence_count += 1

                unique_items[artist_id] = (new_weight, new_occurence_count)
            else:
                unique_items[artist_id] = (weight, 1)

        for artist_id in unique_items:
            weight = unique_items[artist_id][0]
            new_occurence_count = float(unique_items[artist_id][1])
            unique_items[artist_id] = float(weight / new_occurence_count)

        return unique_items

    def filter_user_genres(self, filename, db):
        with open(filename, 'r') as myFile:
            for line in myFile:
                genres = []
                USER_ID = line.encode('utf-8').replace('\n', '')
                artists = db.get_liked_artists(user_id=USER_ID)

                for item in artists:
                    artist = db.get_reverbnation_artist(str(item['artist_id']).encode('utf-8'))
                    for genre in artist['genres']:
                        if genre not in genres:
                            genres.append(genre)
                        else:
                            x = 1

                db.insert_user_genre(genres, USER_ID)
        myFile.close()

    def get_items_user_genre(self, items, pred_items, genres):
        lower_genres = map(lambda x:x.lower(), genres['genres'])
        chosen_pred_items = []
        for (artist_id, relevance) in pred_items:
            artist_genres = items[artist_id].get_data()['genres']
            lower_artist_genres = map(lambda x:x.lower(), artist_genres)
            for genre in lower_artist_genres:
                if genre in lower_genres:
                    chosen_pred_items.append((artist_id, relevance))
                    break
        return chosen_pred_items