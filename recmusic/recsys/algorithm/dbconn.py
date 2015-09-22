__author__ = 'dhiraj'


import pymongo
from pymongo import MongoClient
from bson.binary import Binary
from bson.objectid import ObjectId
import random
import math

class DBConn(object):

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['ds4dems']


    def get_people(self):
        collection = self.db['people']
        return collection.find(no_cursor_timeout=True)

    def get_person(self, person_twitter_id):
        collection = self.db['people']
        person = collection.find_one({"id": person_twitter_id})
        return person

    def insert_person(self, person):
        try:
            collection = self.db['people']
            person_id = collection.insert(person)
            return person_id
        except Exception as e:
            print e

    def update_person(self, person_id, person, friends):
        collection = self.db['people']
        collection.update({'_id': person_id}, person)
        if len(friends) > 0:
            collection.update({'_id': person_id}, {'$set': {'friends_ids': friends}})
        return person_id

    def update_person_tweet_count(self, person_id, artist_count):
        collection = self.db['people']
        collection.update({'_id': person_id}, {'$set': {'artist_distinct_count': artist_count}})

    def get_reverbnation_artists(self):
        collection = self.db['reverbnation_artists']
        return collection.find({"$where": "this.handles.length > 0"})

    def count_soundcloud_tracks(self, artist_id):
        collection = self.db['soundcloud_tracks']
        return collection.find({"reverbnation_artist_id": ObjectId(artist_id)}).count()

    def get_reverbnation_artists_by_handle(self, handle):
        collection = self.db['reverbnation_artists']
        return collection.find_one({'handles': handle})

    def get_reverbnation_artists_by_handle_soundcloud(self, handle):
        collection = self.db['reverbnation_artists']
        return collection.find_one({"$where": "this.soundcloud.length > 0", "handles": handle})

    def get_handle(self, handle_id):
        collection = self.db['handles']
        return collection.find_one({'_id': handle_id})

    def get_handle_artist(self, handle):
        collection = self.db['handles']
        return collection.find_one({'handle': handle})

    def get_authors(self, handle_id):
        collection = self.db['tweets']
        return collection.aggregate([
        {
            '$match': {'handle_id': handle_id}
        },
        {
                '$group': {
                    "_id": {'author_id': '$author_id'},
                    "count": {'$sum': 1}
                }
        }],
            cursor={},
            allowDiskUse=True
        )

    def get_tweets(self):
        collection = self.db['tweets']
        return collection.aggregate([
        {
                '$group': {
                    "_id": {'handle_id': '$handle_id', 'author_id': '$author_id'},
                    "count": {'$sum': 1}
                }
        }],
            cursor={},
            allowDiskUse=True
        )

    def get_tweet_count(self):
        collection = self.db['tweets']
        return collection.aggregate([
        {
                '$group': {
                    "_id": {'author_id': '$author_id'},
                    "count": {"$sum": 1}
                }
        }],
            cursor={},
            allowDiskUse=True
        )

    def get_tweet_occurrence_count(self, handle_id, author_id):
        collection = self.db['tweets']
        return collection.find({'handle_id': handle_id, 'author_id': author_id}).count()


    def get_max_tweet_count(self):
        collection = self.db['tweets']
        return collection.aggregate([
            {
                '$group': {
                    "_id": {'handle_id': '$handle_id'},
                    '$count': {'sum': 1}
                }
            }
        ])

    def get_user(self, twitter_handle):
        collection = self.db['people']
        return collection.find_one({'id': twitter_handle})

    def get_user_id(self, USER_ID):
        collection = self.db['people']
        return collection.find_one({"_id": ObjectId(USER_ID)})

    def create_s_matrix(self):
        self.db.create_collection('matrix_s')

    def create_v_matrix(self):
        self.db.create_collection('matrix_v')

    def create_u_matrix(self):
        self.db.create_collection('matrix_u')

    def create_labels(self):
        self.db.create_collection('matrix_labels')

    def create_sparse_matrix(self):
        self.db.create_collection('sparse_matrix')

    def insert_into_s_matrix(self, index, value):
        collection = self.db['matrix_s']
        return collection.insert({"index": index, "value": value})

    def insert_into_u_matrix(self, values):
        collection = self.db['matrix_u']
        return collection.insert({"array": values})

    def insert_into_v_matrix(self, index, values):
        collection = self.db['matrix_v']
        return collection.insert({"col_index": index, "array": values})

    def insert_into_sparse_matrix(self, index, user_id, values):
        collection = self.db['sparse_matrix']
        return collection.insert({"col_index": index, "user_id": user_id, "array": values})

    def get_U_matrix(self):
        collection = self.db['matrix_u']
        return collection.find({}, {'array': 1})

    def get_S_matrix(self):
        collection = self.db['matrix_s']
        return collection.find({}, {'index': 1, 'value': 1})

    def get_V_matrix(self, col_index):
        collection = self.db['matrix_v']
        return collection.find({"col_index": col_index}, {'array': 1})

    def insert_into_labels(self, index, artist_id, flag):
        collection = self.db['matrix_labels']
        return collection.insert({"index": index, "artist_id": artist_id, "soundcloud": flag})

    def get_label(self, index):
        collection = self.db['matrix_labels']
        return collection.find_one({"index": index}, {"artist_id": 1})

    def get_artist_labels(self):
        collection = self.db['matrix_labels']
        return collection.find({}, {"artist_id": 1})

    def get_artists_soundcloud(self):
        collection = self.db['matrix_labels']
        return collection.find({}, {"artist_id": 1, "soundcloud": 1})

    def get_stats(self):
        return self.db.command("collstats", "matrix_v")

    def get_soundcloud_tracks(self, reverbnation_artist_id):
        collection = self.db['soundcloud_tracks']
        return collection.find({"reverbnation_artist_id": ObjectId(reverbnation_artist_id)}).limit(5)

    def get_sparse_matrix_vector(self, USER_ID):
        collection = self.db['sparse_matrix']
        return collection.find({"user_id": USER_ID})

    def update_sparse_matrix_vector(self, USER_ID, array):
        collection = self.db['sparse_matrix']
        return collection.update({"user_id": USER_ID}, {"$set": {"array": array}})

    def get_soundcloud_labels(self):
        collection = self.db['matrix_labels']
        return collection.find({"soundcloud": 1}, {"index": 1, "_id": 0})

    def check_artist_in_soundcloud(self, artist_id):
        collection = self.db['matrix_labels']
        return collection.find_one({"artist_id": artist_id, "$where": "this.soundcloud == 1"})

    def get_reverbnation_artist(self, artist_id):
        collection = self.db['reverbnation_artists']
        return collection.find_one({"_id": ObjectId(artist_id)})

    def create_feedback(self):
        self.db.create_collection('feedback')

    def insert_feedback(self, user_id, artist_id, like_dislike, rank, listen, rec_type):
        collection = self.db['feedback']
        return collection.insert({"user_id": ObjectId(user_id), "artist_id": ObjectId(artist_id), "like_dislike": like_dislike, "rank": rank, "listen": listen, "rec_type": rec_type})

    def update_feedback(self, user_id, artist_id, like_dislike, rank, listen, rec_type):
        collection = self.db['feedback']
        return collection.update({"user_id": ObjectId(user_id), "artist_id": ObjectId(artist_id)}, {"$set": {"like_dislike": like_dislike, "rank": rank, "listen": listen, "rec_type": rec_type}})

    def insert_soundcloud_feedback(self, user_id, artist_id, soundcloud_id, listen):
        collection = self.db['feedback']
        return collection.insert({"user_id": ObjectId(user_id), "artist_id": ObjectId(artist_id), "soundcloud_ids": soundcloud_id, "listen": listen})

    def update_soundcloud_feedback(self, user_id, artist_id, soundcloud_id, listen):
        collection = self.db['feedback']
        return collection.update({"user_id": ObjectId(user_id), "artist_id": ObjectId(artist_id)}, {"$push": {"soundcloud_ids": soundcloud_id }, "$set": {"listen": listen}})

    def check_feedback(self, user_id, artist_id):
        collection = self.db['feedback']
        return collection.find({"user_id": ObjectId(user_id), "artist_id": ObjectId(artist_id)}).count()

    def get_tweet_count_twitter(self, user_id):
        collection = self.db['tweets']
        return collection.find({"author_id": user_id}, {"handle_id": 1, "$exists": "handle_id"})

    def get_people_display_url(self):
        collection = self.db['people']
        return collection.find({"entities.description.urls.display_url": {"$exists": True}, "artist_distinct_count": {"$exists": True}, "$where": "this.artist_distinct_count > 0"}, no_cursor_timeout=True)

    def get_people_sorted_artists(self, start, step):
        collection = self.db['people']

        if step == 0:
            return collection.find({"artist_distinct_count": {"$exists": True}, "$where": "this.artist_distinct_count > " + str(start) }, no_cursor_timeout=True).sort("artist_distinct_count", -1)
        else:
            count = collection.find({"artist_distinct_count": {"$exists": True}, "$where": "this.artist_distinct_count == " + str(start) }, no_cursor_timeout=True).count()
            results = []
            if count > 0:
                for i in range(step):
                    rand = int(math.floor(random.random() * count))
                    results.append(collection.find({"artist_distinct_count": {"$exists": True}, "$where": "this.artist_distinct_count == " + str(start) }, no_cursor_timeout=True).limit(-1).skip(rand).next())
            return results

    def get_live_feedback(self):
        collection = self.db['live_feedback']
        return collection.find({}, {"user_id": 1, "artist_id": 1, "like_dislike": 1})

    def get_live_feedback_user(self, user_id):
        collection = self.db['live_feedback']
        return collection.find({"user_id": ObjectId(user_id)})

    def get_live_feedback_eval_2_user(self, user_id):
        collection = self.db['live_feedback_eval2']
        return collection.find({"user_id": ObjectId(user_id)})

    def get_liked_artists(self, user_id):
        collection = self.db['live_feedback']
        return collection.find({"user_id": ObjectId(user_id), "like_dislike": 1, "rank": {"$gte": 1, "$lte": 10}}, {"artist_id": 1})

    def get_liked_artists_norank(self, user_id):
        collection = self.db['live_feedback']
        return collection.find({"user_id": ObjectId(user_id), "like_dislike": 1}, {"artist_id": 1})

    def get_liked_artists_eval2(self, user_id):
        collection = self.db['live_feedback_eval2']
        return collection.find({"user_id": ObjectId(user_id), "like_dislike": 1}, {"artist_id": 1})

    def get_artists_eval2(self, user_id):
        collection = self.db['live_feedback_eval2']
        return collection.find({"user_id": ObjectId(user_id)})

    def get_disliked_artists(self, user_id):
        collection = self.db['live_feedback']
        return collection.find({"user_id": ObjectId(user_id), "like_dislike": -1}, {"artist_id": 1})

    def get_disliked_artists_eval2(self, user_id):
        collection = self.db['live_feedback_eval2']
        return collection.find({"user_id": ObjectId(user_id), "like_dislike": -1}, {"artist_id": 1})

    def insert_user_genre(self, genres, user_id):
        collection = self.db['genres']
        return collection.insert({"user_id": user_id, "genres": genres})

    def get_genres(self, user_id):
        collection = self.db['genres']
        return collection.find_one({"user_id": user_id}, {"genres": 1})

    def get_users_from_feedback_rectype(self, rec_type):
        collection = self.db['live_feedback']
        return collection.aggregate([ {"$match": {"rec_type": rec_type}}, { "$group": { "_id": { 'user_id': '$user_id' , 'rec_type': '$rec_type' }, "count": {"$sum":1} } }])

    def get_users_from_feedback(self):
        collection = self.db['live_feedback']
        return collection.aggregate([ { "$group": { "_id": { 'user_id': '$user_id' , 'rec_type': '$rec_type' }, "count": {"$sum":1} } }])

    def get_users_from_feedback_eval2(self):
        collection = self.db['live_feedback_eval2']
        return collection.aggregate([ { "$group": { "_id": { 'user_id': '$user_id' , 'rec_type': '$rec_type' }, "count": {"$sum":1} } }])

    def get_sparse_matrix(self):
        collection = self.db['sparse_matrix']
        return collection.find(no_cursor_timeout=True)

    def get_sparse_matrix_limit(self, n):
        collection = self.db['sparse_matrix']
        return collection.find({}).limit(n)

    def upd_sparse_matrix_count(self, USER_ID, count):
        collection = self.db['sparse_matrix']
        return collection.update({"user_id": USER_ID}, {"$set": {"count": count}})