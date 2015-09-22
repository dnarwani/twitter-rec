# import twitter
# import time
# from recsys.algorithm.dbconn import DBConn
# import pymongo
#
# db = DBConn()
#
# api = twitter.Api(consumer_key='YUlt3YfFNYpdQ1FjLcQhBOOIC',
#                   consumer_secret='eVQhzjNfWhgkw01gvQi2PRzrc5CF4fX4JkYfqr7Gbbh1xFSIXI',
#                   access_token_key='3398680881-xxyD85BZ0W0AAe4u0vhRH84Z4m9uSPwimblrEcJ',
#                   access_token_secret='R4NBLV6i4HRKWbRIU78ivsLRc0TfRWShd9EmFpAWe0K8A')
#
# people = db.get_people_with_display_url()
#
# count = 0
# N = 100
# n_counter = 0
# facebook_list = []
# for person in people:
#     found = False
#     urls = person['entities']['description']['urls']
#     for url in urls:
#         if 'display_url' in url:
#             if url['display_url'] is not None and url['display_url'].startswith("facebook.com"):
#                 found = True
#                 url = url['display_url']
#         if 'expanded_url' in url and found is False:
#             if url['expanded_url'] is not None and url['expanded_url'].startswith("facebook.com"):
#                 found = True
#                 url = url['expanded_url']
#
#         if found:
#             facebook_list.append((person['screen_name'], url))
#             break
#
# for screen_name, url in facebook_list:
#     print screen_name, url
#
#
#
#
from recsys.algorithm.dbconn import DBConn
from recsys.algorithm.functions import Functions

# functions = Functions()
# db = DBConn()
# #
# # # functions.insert_ld_occurrences_into_dat(filename="/home/dhiraj/projects/resources/data/ld_occurrences.dat", db=db)
# # functions.filter_user_genres(filename="/home/dhiraj/projects/resources/data/people", db=db)
# filename = "/home/dhiraj/projects/resources/data/people"
# with open(filename, 'r') as myFile:
#     for line in myFile:
#         genres = []
#         USER_ID = line.encode('utf-8').replace('\n', '')
#         count = db.get_liked_artists(USER_ID).count()
#         user = db.get_user_id(USER_ID)
#         db.update_person_tweet_count(user['_id'], count)

# from tests.test_evaluation import TestPrediction
#
# pred = TestPrediction()
# pred.test_PRED_MAE_load_test_and_ground_truth()

GT_DECISION = [2]
TEST_DECISION = [1.99]

from recsys.evaluation.prediction import MAE

eval = MAE()
eval.load(GT_DECISION, TEST_DECISION)
print eval.compute()