from distutils.command.upload import upload

VERBOSE = True #Set to True to get some messages
__all__ = ['matrix', 'factorize']
import functions
import dbconn
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from recsys.algorithm.baseline import Baseline
import cPickle
import time

############### SVD COMPUTE AND RECOMMENDATION ###############
# from recsys.algorithm.baseline import Baseline #Import the test class we've just created

USER_ID = '555c171fa14c6f970f048573'
path = '../recsys/data/'
myFunctions = functions.Functions()

start_time = time.time()

baseline = Baseline(filename="../recsys/tmp/model")

pred_items = myFunctions.recommend(baseline, path, USER_ID)
items = myFunctions._read_items(path + "artists.dat")
for item_id, relevance in pred_items:
    print items[item_id].get_data()['name'], relevance

print("--- % Recommendation function (seconds) ---" + str(time.time() - start_time) + "\n")

start_time = time.time()
myFunctions.update(USER_ID, baseline, path, pred_items)
print("--- % Update function (seconds) ---" + str(time.time() - start_time) + "\n")

