__author__ = 'dhiraj'

from recsys.algorithm.dbconn import DBConn
from recsys.algorithm.functions import Functions

db = DBConn()
functions = Functions()

users = db.get_users_from_feedback()
per_acc = 0.0
per_acc2 = 0.0

count1 = 0.0
count2 = 0.0
count = 0
for user in users:
    count += 1
    user_id = str(user["_id"]["user_id"]).encode('utf-8')
    liked_count = db.get_liked_artists_norank(user_id=user_id).count()
    disliked_count = db.get_disliked_artists(user_id=user_id).count()
    liked_count_eval2 = db.get_liked_artists_eval2(user_id=user_id).count()
    disliked_count_eval2 = db.get_disliked_artists_eval2(user_id=user_id).count()

    if liked_count > 0:
        acc = float(float(liked_count) / float(user["count"])) * 100.0
        count1 += 1.0
        per_acc += acc
    else:
        acc = 0.0
    if liked_count_eval2 > 0:
        eval2_count = db.get_live_feedback_eval_2_user(user_id=user_id).count()
        acc2 = float(float(liked_count_eval2) / float(eval2_count)) * 100.0
        count2 += 1.0
        per_acc2 += acc2
    else:
        acc2 = 0.0

    print "%s,     %s" % (user_id, acc)

over_acc = float(per_acc / count1)
over_acc2 = float(per_acc2 / count2)
print "Overall acc: %s" % over_acc
print "Overall acc2: %s" % over_acc2