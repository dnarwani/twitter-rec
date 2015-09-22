__author__ = 'dhiraj'

from recsys.algorithm.dbconn import DBConn

db = DBConn()

users = db.get_users_from_feedback()
total_per = 0.0
count = 0
mean_listen_1_2 = 0
mean_listen_2_3 = 0
mean_listen_3_4 = 0
mean_listen_4_5 = 0
mean_listen_greater_5 = 0
for user in users:
    listen = 0
    no_listens = 0
    user_id = str(user["_id"]["user_id"]).encode('utf-8')
    user_feedback = db.get_live_feedback_user(user_id=user_id)
    for item in user_feedback:
        if 'soundcloud_ids' in item and len(item['soundcloud_ids']) > 0:
            no_listens += len(item['soundcloud_ids'])
            listen += 1

    mean_listen = float(no_listens) / float(listen)

    if mean_listen >= 1 and mean_listen <= 2:
        mean_listen_1_2 += 1
    elif mean_listen > 2 and mean_listen <= 3:
        mean_listen_2_3 += 1
    elif mean_listen > 3 and mean_listen <= 4:
        mean_listen_3_4 += 1
    elif mean_listen > 4 and mean_listen <= 5:
        mean_listen_4_5 += 1
    elif mean_listen > 5:
        mean_listen_greater_5 += 1

    if listen > 0 and no_listens > 0:
        count += 1

print "Overall mean_listen_1_2 acc: %s" % ((float(mean_listen_1_2) / float(count)) * 100.0)
print "Overall mean_listen_2_3 acc: %s" % ((float(mean_listen_2_3) / float(count)) * 100.0)
print "Overall mean_listen_3_4 acc: %s" % ((float(mean_listen_3_4) / float(count)) * 100.0)
print "Overall mean_listen_4_5 acc: %s" % ((float(mean_listen_4_5) / float(count)) * 100.0)
print "Overall mean_listen_greater_5 acc: %s" % ((float(mean_listen_greater_5) / float(count)) * 100.0)
