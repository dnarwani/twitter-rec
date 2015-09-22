__author__ = 'dhiraj'

from recsys.algorithm.dbconn import DBConn
from recsys.algorithm.functions import Functions
from recsys.algorithm.baseline import Baseline
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

baseline = Baseline()
sparse_matrix = cPickle.load(open("/home/dhiraj/projects/resources/data/sparse_matrix.p"))
baseline._matrix.set(sparse_matrix)
baseline._matrix_and_data_aligned = True

_S = db.get_S_matrix()
list_s = []
for s in _S:
    list_s.append(s["value"])
s_array = np.asarray(list_s)

_U = db.get_U_matrix()
u_vectors = []
for u in _U:
    array = np.asarray(u["array"])
    v = divisi2.from_ndarray(array)
    u_vectors.append(v)

row_labels = cPickle.load(open("/home/dhiraj/projects/resources/data/row_labels.p"))
col_labels = cPickle.load(open("/home/dhiraj/projects/resources/data/col_labels.p"))
baseline._U = DenseMatrix(u_vectors, row_labels)
baseline._S = s_array

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

mavgp = MeanAveragePrecision()
with open(filename, "w") as myFile:
    #while count < n:
        users = db.get_people_sorted_artists(start, step)

        for user in users:
            TEST_DECISION = []
            GT_DECISION = []

            s_matrix_vector = db.get_sparse_matrix_vector(str(user["_id"]).encode('utf-8'))
            if s_matrix_vector and len(s_matrix_vector[0]['array']) > 0:
                # inner_count += 1
                # if inner_count < (step+1):
                    v_vectors = functions.compute_v_vectors(s_matrix_vector[0]['col_index'])
                    counts = dict()
                    for vec in s_matrix_vector[0]['array']:
                        artist_id = db.get_label(index=vec)
                        index = baseline._matrix.get().row_index(str(artist_id['artist_id']).encode('utf-8'))
                        artist_count = baseline._matrix.get_value(str(artist_id['artist_id']).encode('utf-8'), str(user["_id"]).encode('utf-8'))
                        counts[index] = artist_count

                    sorted_indexes = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
                    for index, artist_count in sorted_indexes:
                        GT_DECISION.append(index)

                    pred_items = baseline.recommend(user["_id"], n=10, only_unknowns=False, is_row=False, v_vectors=v_vectors, sparse_matrix_vector=s_matrix_vector[0]['array'])
                    for item_id, relevance in pred_items:
                        index = baseline._matrix.get().row_index(str(item_id).encode('utf-8'))
                        TEST_DECISION.append(index)

                    eval = PrecisionRecallF1()
                    eval.load_test(TEST_DECISION)
                    eval.load_ground_truth(GT_DECISION)
                    (p, r, f1) = eval.compute()

                    eval2 = AveragePrecision()
                    eval2.load(GT_DECISION, TEST_DECISION)
                    mavgp.load(GT_DECISION, TEST_DECISION)
                    average_prec = eval2.compute()

                    plot_prec = p + random.uniform(0.0001, 0.001)

                    print "UserID: %s,      Count: %s,      Precision: %s,       Recall: %s,     F1: %s,    Avg.Precision: %s,  Plot Precision: %s" % (str(user["_id"]).encode('utf-8'), user['artist_distinct_count'], p, r, f1, average_prec, plot_prec)
                    myFile.write("UserID: " + str(user["_id"]).encode('utf-8') + ", " + "Count: " + str(user['artist_distinct_count']) + ", " + "Precision: " + str(p) + ", " +
                                 "Recall: " + str(r) + ", " + "F1: " + str(f1) + ", Avg. Precision: " + str(average_prec) + ", Plot precision: " + str(plot_prec) + "\n")
                    precision.append(plot_prec)
                    recall.append(r)

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
myFile.close()

print "MAP: %s" % str(mavgp.compute())


# plt.scatter(np.asarray(recall), np.asarray(precision))
# x = []
# plt.xlim()
# plt.plot(x, x, linestyle='dashed', color='red', linewidth=2, label='random')
# plt.show()

