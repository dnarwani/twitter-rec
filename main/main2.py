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

USER_ID = '55c93efd8587b261f4b70d3e'
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




from boto.s3.connection import S3Connection
import urllib2

db = DBConn()
conn = S3Connection('AKIAI6F6HFFENFWSPN4Q', 'aP0OOVDj96AFUEr9vbHalvvNZz7rNNXyyH0Wof7i')
bucket = conn.get_bucket('elasticbeanstalk-us-west-2-501394068089')

ld_occurrences_key = bucket.get_key('files/data/ld_occurrences.dat')
ld_occurrences_path = ld_occurrences_key.generate_url(3600, query_auth=True, force_http=True)
ld_occurrences_content = urllib2.urlopen(ld_occurrences_path).read()

svd = SVD()
svd.load_data(filename=ld_occurrences_content, sep='::', format={'col':0, 'row':1, 'value':2, 'ids': str})
all_items = svd.recommend(USER_ID, n=10, only_unknowns=False, is_row=False)
for index, relevance in all_items:
    print index, items[index].get_data()['name'], relevance

# genres = db.get_genres(USER_ID)
# if len(genres['genres']) > 0:
#     pred_items = myFunctions.get_items_user_genre(items, all_items, genres)[:50]
# else:
#     pred_items = all_items[:50]
#
# for index, relevance in pred_items:
#     print index, items[index].get_data()['name'], items[index].get_data()['genres'], relevance


#
# start_time = time.time()
# db = DBConn()
# db.create_labels()
#
# sparse_matrix = svd._matrix.get()
# length = svd._matrix.get_col_len()
# for i in range(length):
#     artist_id = sparse_matrix.row_label(i)
#     count = db.count_soundcloud_tracks(artist_id)
#     if count > 0:
#         db.insert_into_labels(i, artist_id, 1)
#     else:
#         db.insert_into_labels(i, artist_id, 0)

# length = svd._matrix.get_row_len()
# for i in range(length):
#     user_id = sparse_matrix.col_label(i)
#     artist_indices = map(int, sparse_matrix.col_named(user_id).keys())
#     db.insert_into_sparse_matrix(i, user_id, artist_indices)
#     print i

# for index, relevance in pred_items:
#     print index, items[index].get_data()['name'], relevance
#
#print("--- % Sparse matrix function (seconds) ---" + str(time.time() - start_time) + "\n")

# import pymongo
# from bson.objectid import ObjectId
#
# db = DBConn()
# people = db.get_people()
#
# for person in people:
#     distinct_count = 0
#     handles = db.get_tweet_count_twitter(person["_id"])
#     distinct = []
#     try:
#         for handle in handles:
#             if handle["handle_id"] not in distinct:
#                 objHandle = db.get_handle(handle["handle_id"])
#                 if objHandle:
#                     artist = db.get_reverbnation_artists_by_handle(handle=str(objHandle["handle"]).encode('utf-8'))
#                     if artist:
#                         distinct_count += 1
#                         distinct.append(handle["handle_id"])
#
#         db.update_person_tweet_count(person["_id"], distinct_count)
#     except pymongo.errors.OperationFailure:
#         continue
#
# import cPickle
#
# db = DBConn()
# sorted_occurences = myFunctions.get_popular_artists(db)
#
# cPickle.dump(sorted_occurences, open("/home/dhiraj/projects/resources/data/popular.p", "wb"))
# sorted_artists = cPickle.load(open("/home/dhiraj/projects/resources/data/popular.p"))
# for artist in sorted_artists:
#     print artist[0], items[artist[0]].get_data()['name'], artist[1]
