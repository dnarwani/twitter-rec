__author__ = 'dhiraj'


import pymongo
from pymongo import MongoClient
from bson.binary import Binary
from bson.objectid import ObjectId

class DBConn(object):

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['ds4dems']


    def get_people(self):
        collection = self.db['people']
        return collection.find()

    def get_person(self, person_twitter_id):
        collection = self.db['people']
        person = collection.find_one({"id": person_twitter_id})
        if person is None:
            return 0
        else:
            return person['_id']

    def insert_person(self, person, friends):
        try:
            collection = self.db['people']
            person_id = collection.insert(person)
            if len(friends) > 0:
                collection.update({'_id': person_id}, {'$set': {'friends_ids': friends}})
            return person_id
        except Exception as e:
            print e

    def update_person(self, person_id, person, friends):
        collection = self.db['people']
        collection.update({'_id': person_id}, person)
        if len(friends) > 0:
            collection.update({'_id': person_id}, {'$set': {'friends_ids': friends}})
        return person_id

    def get_reverbnation_artists(self):
        collection = self.db['reverbnation_artists']
        return collection.find({"$where": "this.handles.length > 0"})

    def get_reverbnation_artists_by_handle(self, handle):
        collection = self.db['reverbnation_artists']
        return collection.find_one({'handles': handle})

    def get_handle(self, handle_id):
        collection = self.db['handles']
        return collection.find_one({'_id': handle_id})

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


    def get_max_tweet_count(self, author_id):
        collection = self.db['tweets']
        return collection.aggregate([
            {
                '$match': {'author_id': author_id}
            },
            {
                '$group': {
                    "_id": {'handle_id': '$handle_id'},
                    '$count': {'$max': 1}
                }
            }
        ])

    def get_user_id(self, twitter_handle):
        collection = self.db['people']
        return collection.find_one({'screen_name': twitter_handle}, {'_id': 1})

    def create_sparse_matrix(self):
        self.db.create_collection('sparse_matrix')

    def insert_into_sparse_matrix(self, sparse_matrix):
        collection = self.db['sparse_matrix']
        collection.insert({'bin-data': Binary(sparse_matrix)})


