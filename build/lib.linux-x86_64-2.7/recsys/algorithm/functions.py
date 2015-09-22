__author__ = 'dhiraj'

import codecs
import time
import pickle
import cPickle
from itertools import islice

from bson.objectid import ObjectId
import numpy as np
import matplotlib.pyplot as plt

from recsys.datamodel.data import Data
from recsys.datamodel.item import Item
from recsys.algorithm import dbconn


class Functions(object):

    # Read music info
    def _read_items(self, filename):
        items = dict()
        for line in codecs.open(filename, 'r', 'latin1'):
            #1::Toy Story (1995)::Animation|Children's|Comedy
            data = line.strip('\r\n').split('::')
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

    def create_count_dict_pickle(self, db):
        count_dict = dict()

        print "Querying database for author counts..."
        author_counts = list(db.get_tweet_count())

        print "Creating dictionary of counts..."
        for author in author_counts:
            count_dict[str(author["_id"]["author_id"])] = author["count"]

        print "Create pickle file..."
        pickle.dump(count_dict, open("../recsys/data/count_dict.p", "wb"))

        print "Pickle created..."

    def create_artist_count_pickle(self, db):
        occurrences = dict()
        print "Loading tweet pickle..."
        tweet_dict = pickle.load(open("../recsys/data/tweets.p", "rb"))

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

        print "Create pickle file..."
        pickle.dump(occurrences, open("../recsys/data/occurrences.p", "wb"))

        print "Pickle created..."

    def create_tweet_pickle(self, db):
        tweets_dict = dict()

        print "Querying database for tweets..."
        tweets = list(db.get_tweets())

        print "Create dictionary of tweets..."
        for tweet in tweets:
            tweets_dict[(str(tweet["_id"]["handle_id"]), str(tweet["_id"]["author_id"]))] = tweet["count"]

        print "Create pickle file..."
        pickle.dump(tweets_dict, open("../recsys/data/tweets.p", "wb"))

        print "Pickle created..."

    def insert_tweet_occurrences_into_dat(self, filename, db):
        occurrences = dict()

        print "Loading count_dict pickle..."
        count_dict = pickle.load(open("../recsys/data/count_dict.p", "rb"))

        print "Loading occurrence matrix..."
        occurrences = pickle.load(open("../recsys/data/occurrences.p", "rb"))

        print "Writing to file ..."
        with open(filename, 'w') as myFile:
            for (artist_id, author_id), count in occurrences.iteritems():
                if author_id in count_dict:
                    normalized = float(count) / float(count_dict[author_id])
                    print normalized
                    myFile.write(str(author_id).encode("utf-8") + "::" + str(artist_id).encode("utf-8") +
                                 "::" + str(normalized).encode("utf-8") + "::" +
                                 str(int(time.time())).encode("utf-8") + "\n")
        myFile.close()
        print "Done"

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

    def output_confusion_matrix(self, n, ground_truth, test):
        TP, FP, TN, FN = (0, 0, 0, 0)
        lst_ground_truth = list(ground_truth)
        for item in test:
            if item in lst_ground_truth:
                TP += 1
                lst_ground_truth.pop(lst_ground_truth.index(item))
            else:
                FP += 1
        FN = len(lst_ground_truth)
        TN = n - len(test)
        return TP, FP, TN, FN

    def take(self, n, iterable):
        "Return first n items of the iterable as a list"
        return list(islice(iterable, 1, n + 1))

    def plot_roc_curve(self, list_fpr, list_tpr):
        plt.figure(figsize=(4, 4), dpi=80)

        x = [0.0, 1.0]
        plt.plot(x, x, linestyle='dashed', color='red', linewidth=2, label='random')
        plt.xlabel("FPR", fontsize=14)
        plt.ylabel("TPR", fontsize=14)
        plt.title("ROC Curve", fontsize=14)
        plt.xlim(0.0, 1.0)
        plt.ylim(0.0, 1.0)
        plt.legend(fontsize=10, loc='best')
        plt.tight_layout()
        plt.plot(list_fpr, list_tpr, color='blue', linewidth=2, label='USER 1')
        plt.show()

    def update(self, USER_ID, baseline, path, pred_items):
        print "Loading tweet occurrences pickle..."
        baseline.get_data()._load_pickle(path=path + "tweet_occurrences.p")
        tweet_occurrences = baseline.get_data().get()

        print "Loading count_dict pickle..."
        count_dict = cPickle.load(open(path + "count_dict.p"))

        print "Loading occurrences pickle..."
        occurrences = cPickle.load(open(path + "occurrences.p"))

        total_count = count_dict[USER_ID]
        upd_total_count = int(total_count) + len(pred_items)
        count_dict[USER_ID] = int(upd_total_count)

        print "Dumping count_dict pickle..."
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

        print "Dumping tweet occurrences pickle..."
        data_tweet_occurrences = Data()
        data_tweet_occurrences.set(tweet_occurrences)

        baseline.set_data(data_tweet_occurrences)
        baseline.save_data(filename=path + "tweet_occurrences.p", pickle=True)

        print "Dumping occurrence pickle..."
        cPickle.dump(occurrences, open(path + "occurrences.p", "wb"), protocol=2)

        print "Dumping sparse matrix pickle..."
        cPickle.dump(baseline._matrix.get(), open(path + "sparse_matrix.p", "w"), protocol=2)

        # print "Updating matrix..."
        # baseline.compute(k=100, min_values=None, pre_normalize=None, mean_center=False, post_normalize=True)


    def recommend(self, baseline, path, USER_ID):
        s_matrix = cPickle.load(open(path + "sparse_matrix.p"))
        baseline._matrix.set(s_matrix)
        baseline._matrix_and_data_aligned = True

        baseline._matrix_reconstructed = cPickle.load(open(path + "matrix_reconstructed.p"))

        pred_items = baseline.recommend(USER_ID, only_unknowns=True, is_row=False)
        return pred_items


