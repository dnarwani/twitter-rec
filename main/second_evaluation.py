__author__ = 'dhiraj'

from recsys.algorithm.dbconn import DBConn
from recsys.algorithm.functions import Functions
from recsys.algorithm.baseline import Baseline
from recsys.algorithm.factorize import SVD
from recsys.evaluation.decision import PrecisionRecallF1
from recsys.evaluation.ranking import AveragePrecision
from recsys.evaluation.ranking import MeanAveragePrecision

import cPickle
import numpy as np
import divisi2
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from divisi2 import DenseMatrix
import random
import operator

db = DBConn()
functions = Functions()

svd = SVD()
filename = "/home/dhiraj/projects/resources/data/ld_occurrences.dat"
svd.load_data(filename=filename, sep='::', format={'col':0, 'row':1, 'value':2, 'ids': str})
svd.create_matrix()

n = 100
step = 0
start = 119

(prec, recall, F1) = 0.0, 0.0, 0.0
count = 0
precision = []
recall = []
roc_auc = dict()
total_recall = 0.0
total_prec = 0.0
total_f1 = 0.0
total_mean_prec = 0.0
inner_count = 0
filename = "/home/dhiraj/projects/results/dataset2/precision_results.txt"
tpr = []
fpr = []

final_tp = 0
final_fn = 0
final_fp = 0
final_tn = 0

mavgp = MeanAveragePrecision()
with open(filename, "w") as myFile:
        filename2 = "/home/dhiraj/projects/resources/data/people"
        with open(filename2, 'r') as myFile2:
            for line in myFile2:
                genres = []
                USER_ID = line.encode('utf-8').replace('\n', '')
                TEST_DECISION = []
                GT_DECISION = []
                LIKED = []
                DISLIKED = []
                liked = db.get_liked_artists(user_id=USER_ID)
                for like in liked:
                    LIKED.append(str(like['artist_id']).encode('utf-8'))

                disliked = db.get_disliked_artists(user_id=USER_ID)
                for dislike in disliked:
                    DISLIKED.append(str(dislike['artist_id']).encode('utf-8'))


                user = db.get_user_id(USER_ID=USER_ID)
                live_feedback = db.get_live_feedback_user(USER_ID)
                counts = dict()
                for feedback in live_feedback:
                    index = svd._matrix.get().row_index(str(feedback['artist_id']).encode('utf-8'))
                    artist_count = svd._matrix.get_value(str(feedback['artist_id']).encode('utf-8'), str(user["_id"]).encode('utf-8'))
                    counts[index] = artist_count

                sorted_indexes = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
                for index, artist_count in sorted_indexes:
                    GT_DECISION.append(index)

                TP, FP, TN, FN = 0, 0, 0, 0

                pred_items = svd.recommend(str(user['_id']).encode('utf-8'), n=10, only_unknowns=False, is_row=False)
                for item_id, relevance in pred_items:
                    index = svd._matrix.get().row_index(str(item_id).encode('utf-8'))
                    TEST_DECISION.append(index)

                    if str(item_id).encode('utf-8') in LIKED:
                        TP += 1
                    elif str(item_id).encode('utf-8') in DISLIKED:
                        FP += 1


                FN = len(LIKED) - TP
                TN = len(DISLIKED) - FP

                if TP == 0:
                    p = 0.0
                    r = 0.0
                    f1 = 0.0
                else:
                    p = float(TP) / (float(TP) + float(FP))
                    r = float(TP) / (float(TP) + float(FN))
                    f1 = 2 * float(((float(p) * float(r)) / (float(p) + float(r))))


                final_fp += float(FP)
                final_tp += float(TP)
                final_tn += float(TN)
                final_fn += float(FN)

                tpr.append((float(r)))
                if FP == 0:
                    fpr.append(0)
                else:
                    fpr.append((float(FP) / (float(FP) + float(TN))))


                eval2 = AveragePrecision()
                eval2.load(GT_DECISION, TEST_DECISION)
                mavgp.load(GT_DECISION, TEST_DECISION)
                average_prec = eval2.compute()

                print "UserID: %s,      Count: %s,      Precision: %s,       Recall: %s,     F1: %s,    Avg.Precision: %s" % (str(user["_id"]).encode('utf-8'), user['artist_distinct_count'], p, r, f1, average_prec)
                myFile.write("UserID: " + str(user["_id"]).encode('utf-8') + ", " + "Count: " + str(user['artist_distinct_count']) + ", " + "Precision: " + str(p) + ", " +
                             "Recall: " + str(r) + ", " + "F1: " + str(f1) + ", Avg. Precision: " + str(average_prec) + "\n")

                total_recall += r
                total_prec += p
                total_f1 += f1
                count += 1
                # if count % 10 == 0:
                #     output_recall = float(float(total_recall) / float(count))
                #     output_prec = float(float(total_prec) / float(count))
                #     output_f1 = float(float(total_f1) / float(count))
                #     output_map = float(mavgp.compute())
                #     print "Interval: %s,     Avg Recall: %s,   Avg Precision: %s,   Avg. F1: %s,   MAP: %s" % (start, output_recall, output_prec, output_f1, output_map)
                #     myFile.write("Interval: " + str(start) + ", " + "Avg. Precision: " + str(output_prec) + ", " + "Avg. recall: " + str(output_recall) + ", Avg. F1: " + str(output_f1) + ", MAP: " + str(output_map) + "\n")

            if inner_count == step:
                start += 1
                # if start == 10:
                #     start = 9
                inner_count = 0

                # if start % 10 == 0:
                #     output_recall = float(float(total_recall) / float(count))
                #     output_prec = float(float(total_prec) / float(count))
                #     output_f1 = float(float(total_f1) / float(count))
                #     output_map = float(mavgp.compute())
                #     print "Interval: %s,     Avg Recall: %s,   Avg Precision: %s,   Avg. F1: %s,   MAP: %s" % (start, output_recall, output_prec, output_f1, output_map)
                #     myFile.write("Interval: " + str(start) + ", " + "Avg. Precision: " + str(output_prec) + ", " + "Avg. recall: " + str(output_recall) + ", Avg. F1: " + str(output_f1) + ", MAP: " + str(output_map) + "\n")
myFile2.close()
myFile.close()

acc = ((float(final_tp) + float(final_tn)) / float(float(final_tp) + float(final_tn) + float(final_fp) + float(final_fn)))
print "MAP: %s" % str(mavgp.compute())
print "Acc: %s" % str(acc)
avg_prec = (float(total_prec) / float(count))
avg_recall = (float(total_recall) / float(count))
avg_f1 = (float(total_f1) / float(count))
print "Avg. Precision: %s" % str(avg_prec)
print "Avg. Recall %s" % str(avg_recall)
print "Avg. F1 %s" % str(avg_f1)


# plt.scatter(np.asarray(recall), np.asarray(precision))
# x = []
# plt.xlim()
# plt.plot(x, x, linestyle='dashed', color='red', linewidth=2, label='random')
# plt.show()

