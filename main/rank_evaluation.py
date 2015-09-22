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
    liked_rank_count = db.get_liked_artists(user_id=user_id).count()
    liked_count_eval2 = db.get_liked_artists_eval2(user_id=user_id).count()

    if liked_count > 0:
        acc = float(float(liked_count) / float(user["count"])) * 100.0
        if user['count'] >= 10:
            acc_count = 10
        else:
            acc_count = user['count']
        acc_rank = float(float(liked_rank_count) / acc_count) * 100.0
        count1 += 1.0
        per_acc += acc_rank
    else:
        acc = 0.0
        acc_rank = 0.0
    if liked_count_eval2 > 0:
        eval2_count = db.get_live_feedback_eval_2_user(user_id=user_id).count()
        acc2 = float(float(liked_count_eval2) / float(eval2_count)) * 100.0

        like_rank = 0
        artists_rank = db.get_artists_eval2(user_id=user_id)
        for artist in artists_rank:
            if artist['like_dislike'] == 1:
                like_rank += 1

        if eval2_count >= 10:
            acc2_count = 10
        else:
            acc2_count = eval2_count
        acc2_rank = float(float(like_rank) / acc2_count) * 100.0

        count2 += 1.0
        per_acc2 += acc2_rank
    else:
        acc2 = 0.0
        acc2_rank = 0.0

    print "%s,     %s,   %s" % (count, round(acc, 0), acc_rank)
    print "%s,     %s,   %s" % (count, round(acc2, 0), acc2_rank)

over_acc = float(per_acc / count1)
over_acc2 = float(per_acc2 / count2)
print "Overall acc: %s" % over_acc
print "Overall acc2: %s" % over_acc2