import sys
import time
import cPickle
import numpy as np
import divisi2

from recsys.algorithm import functions
from divisi2 import DenseMatrix

reload(sys)
sys.setdefaultencoding("utf-8")

############### SVD COMPUTE AND RECOMMENDATION ###############
from recsys.algorithm.baseline import Baseline #Import the test class we've just created
from recsys.algorithm.factorize import SVD
from recsys.algorithm.dbconn import DBConn

USER_ID = '54acb98c28722106e509078a'
myFunctions = functions.Functions()

# db = DBConn()
#
# baseline = Baseline()
# s_matrix = cPickle.load(open("/home/dhiraj/projects/resources/data/sparse_matrix.p"))
# baseline._matrix.set(s_matrix)
# baseline._matrix_and_data_aligned = True
#
# _S = db.get_S_matrix()
# list_s = []
# for s in _S:
#     list_s.append(s["value"])
# s_array = np.asarray(list_s)
#
# _U = db.get_U_matrix()
# u_vectors = []
# for u in _U:
#     array = np.asarray(u["array"])
#     v = divisi2.from_ndarray(array)
#     u_vectors.append(v)
#
#
# baseline._U = DenseMatrix(u_vectors)
# baseline._S = s_array
#
#
start_time = time.time()
# col_index = baseline._matrix.get().col_index(USER_ID)
# _V = db.get_V_matrix(col_index)
# v_vectors = []
# array = np.asarray(_V[0]["array"])
# v_vectors.append(divisi2.from_ndarray(array))
#
# pred_items = baseline.recommend(USER_ID, n=10, only_unknowns=False, is_row=False, v_vectors=v_vectors)
#
items = myFunctions._read_items_from_fs("/home/dhiraj/projects/resources/data/artists.dat")
# for index, relevance in pred_items:
#     item_id = db.get_label(index)
#     print index, items[item_id['artist_id']].get_data()['name'], relevance
#
# print("--- % Recommendation function (seconds) ---" + str(time.time() - start_time) + "\n")

# svd = SVD()
# s_matrix = cPickle.load(open("/home/dhiraj/projects/resources/data/sparse_matrix.p"))
# svd._matrix.set(s_matrix)
# svd._matrix_and_data_aligned = True
#
# db = DBConn()
# db.create_sparse_matrix()


#
# sparse_matrix = svd._matrix.get()
# length = svd._matrix.get_row_len()
# for i in range(length):
#     user_id = sparse_matrix.col_label(i)
#     artist_indices = map(int, sparse_matrix.col_named(user_id).keys())
#     db.insert_into_sparse_matrix(i, artist_indices)
#     print i

# db = DBConn()
# import soundcloud
# from recommender import settings
# client = soundcloud.Client(client_id=settings.soundcloud_client_id)
#
# tracks_output = dict()
# tracks = []
# track_list = db.get_soundcloud_tracks('54ad0e5928722106e5090fa4')
# for track in track_list:
#     track_url = str(track['permalink_url']).encode('utf-8')
#     embed_info = client.get('/oembed', url=track_url)
#     tracks.append(embed_info.obj['html'].replace('height="400"', 'height="200"'))
#
# tracks_output[items['54ad0e5928722106e5090fa4'].get_data()['name']] = tracks

#
# db = DBConn()
# user_id = db.get_user_id('ajohnson1987st')
# USER_ID = str(user_id["_id"]).encode('utf-8')
#
# svd_items = svd.recommend(USER_ID, n=10, only_unknowns=True, is_row=False)
# items = myFunctions._read_items_from_fs("/home/dhiraj/projects/resources/data/artists.dat")
# for index, relevance in svd_items:
#     print index, items[index].get_data()['name'], relevance


# print "Dumping pickle file..."
# cPickle.dump(baseline._matrix_reconstructed, open("../recmusic/recsys/data/reconstructed_matrix.p", "wb"), protocol=2)
#


# start_time = time.time()
# myFunctions.update(USER_ID, baseline, path, pred_items)
# print("--- % Update function (seconds) ---" + str(time.time() - start_time) + "\n")


# from boto.s3.connection import S3Connection
# import boto
# from recsys.algorithm.functions import Functions
# import urllib2
#
# myFunctions = Functions()
# conn = S3Connection('AKIAI6F6HFFENFWSPN4Q', 'aP0OOVDj96AFUEr9vbHalvvNZz7rNNXyyH0Wof7i')
# bucket = conn.get_bucket('elasticbeanstalk-us-west-2-501394068089')
# key = bucket.get_key('files/artists.dat')
# path = key.generate_url(3600, query_auth=True, force_http=True)
# str = urllib2.urlopen(path).read()
# items = myFunctions._read_items(str)
# x = 1



# svd = SVD()
# svd.load_data(filename='../recmusic/recsys/data/tweet_occurrences.dat', sep='::', format={'col':0, 'row':1, 'value':2, 'ids': str})
# svd.create_matrix()
# pred_items = svd.recommend('Unknown', n=10, only_unknowns=True, is_row=False)
#
# i = 0
#
# for index, relevance in pred_items:
#     print index, items[index].get_data()['name'], relevance
#
# print("--- % Recommendation function (seconds) ---" + str(time.time() - start_time) + "\n")
# db = DBConn()
# zero s = []
# ones = []
# soundcloud_artists = db.get_soundcloud_labels()
# sparse_matrix_vector = list(db.get_sparse_matrix_vector(USER_ID))
# for artist in soundcloud_artists:
#     if not artist["index"] in sparse_matrix_vector[0]['array']:
#         zeros.append(artist["index"])
#     else:
#         ones.append(artist["index"])
#
# x = 1

# baseline = Baseline()
#
# db = DBConn()
# _S = db.get_S_matrix()
# list_s = []
# for s in _S:
#     list_s.append(s["value"])
# s_array = np.asarray(list_s)
#
# _U = db.get_U_matrix()
# u_vectors = []
# for u in _U:
#     array = np.asarray(u["array"])
#     v = divisi2.from_ndarray(array)
#     u_vectors.append(v)
#
# row_labels = cPickle.load(open("/home/dhiraj/projects/resources/data/row_labels.p"))
# col_labels = cPickle.load(open("/home/dhiraj/projects/resources/data/col_labels.p"))
# baseline._U = DenseMatrix(u_vectors, row_labels)
# baseline._S = s_array
#
# s_matrix_vector = list(db.get_sparse_matrix_vector(USER_ID))
# v_vectors = myFunctions.compute_v_vectors(s_matrix_vector[0]['col_index'])
#
# artist_indexes = []
# pred_items = baseline.recommend(USER_ID, n=10, only_unknowns=True, is_row=False, v_vectors=v_vectors, sparse_matrix_vector=s_matrix_vector[0]['array'])
# for index, relevance in pred_items:
#     artist_indexes.append(baseline._U.row_index(index))
#     print index, items[index].get_data()['name'], relevance
#
#
# upd_sparse_matrix_vec = list(db.get_sparse_matrix_vector(USER_ID))
# upd_list = upd_sparse_matrix_vec[0]['array']
# upd_list.extend(artist_indexes)
# db.update_sparse_matrix_vector(USER_ID, upd_list)
#
# print("--- % Recommendation function (seconds) ---" + str(time.time() - start_time) + "\n")

# #
# import time
# import tweepy
# import operator
#
# auth = tweepy.OAuthHandler('QpWCKsHR2xqvSLr7qiyjiqGBw', 'eGdcJUBieoBDZ0rmWAGDFbRWrUsWvssG3IStP1fjnZayxOYhxY')
# auth.set_access_token('3023706377-FH7UktzuLuZ42VKTvWiazD4k4fNUVOzetOIjV3N', 'sqQQ8J9vwyOD9aYJzcP1XhyWa0oGh7auzieUtN6ig7gdI')
# api = tweepy.API(auth)
# db = DBConn()
# #
# ids = dict()
# for twitter_handle in tweepy.Cursor(api.friends_ids, screen_name="dn14500").items():
#     try:
#         user = db.get_person(twitter_handle)
#         if user is not None:
#             ids[user["_id"]] = int(user["artist_distinct_count"])
#     except tweepy.TweepError:
#         break
#     except StopIteration:
#         break
#
# top_5_ids = sorted(ids.items(), key=operator.itemgetter(1), reverse=True)[:5]


# import cPickle
#
# db = DBConn()
# sorted_occurences = myFunctions.get_popular_artists(db)
#
# cPickle.dump(sorted_occurences, open("/home/dhiraj/projects/resources/data/popular.p", "wb"))
# sorted_artists = cPickle.load(open("/home/dhiraj/projects/resources/data/popular.p"))
# for artist in sorted_artists:
#     print artist[0], items[artist[0]].get_data()['name'], artist[1]

# db = DBConn()
#
# s_matrix_vector = list(db.get_sparse_matrix_vector("548a829c28722106e50329e2"))
# v_vectors = myFunctions.compute_v_vectors(s_matrix_vector[0]['col_index'])

#
# top_users = myFunctions.get_top_friends(api.friends_ids, db, api.me().screen_name)
# artist_labels = []
# final_items = []
# user = db.get_user(api.me().id)
# known_items = list(db.get_sparse_matrix_vector(str(user['_id']).encode('utf-8')))
# if len(known_items[0]['array']) > 0:
#     for item in known_items[0]['array'][0]:
#         artist_labels.append(baseline._U.row_label(item))
#
# for (user_id, artist_distinct_count) in top_users:
#     s_matrix_vector = list(db.get_sparse_matrix_vector(str(user_id).encode('utf-8')))
#     v_vectors = myFunctions.compute_v_vectors(s_matrix_vector[0]['col_index'])
#
#     pred_items = baseline.recommend(user_id, n=10, only_unknowns=True, is_row=False, v_vectors=v_vectors, sparse_matrix_vector=s_matrix_vector[0]['array'], col_labels=col_labels)
#
#     for artist_id, weight in pred_items:
#         if artist_id not in artist_labels:
#             final_items.append((artist_id, weight))
#
# ranked_items = myFunctions.get_ranked_followers_friends(final_items)
# pred_items = sorted(ranked_items.items(), key=operator.itemgetter(1), reverse=True)[:10]
#
# #remove items
# new_items = dict()
# count = 0
# for artist_id, weight in ranked_items.iteritems():
#     if (artist_id, weight) not in pred_items:
#         new_items[artist_id] = weight
#
# print baseline._U.row_index('54ad0f9228722106e509bf91')

# db = DBConn()
# user = db.get_user_id(USER_ID)
# if (user is None) or (user is not None and 'artist_distinct_count' not in user):
#     x = 1

#!/bin/sh

# clear django_session table
# DJANGO_SETTINGS_MODULE="recmusic.settings" \
#   python -c 'from django.contrib.sessions.models import Session; \
#     Session.objects.all().delete()'
# python manage.py runserver

# db = DBConn()
#
# users = db.get_sparse_matrix()
# inc = 0
# for user in users:
#     count = len(user['array'])
#     db.upd_sparse_matrix_count(user['user_id'], count)
#     inc += 1
#     print inc

filename = "/home/dhiraj/projects/resources/data/resources.dat"
myFunctions.insert_genres_into_dat(filename=filename)