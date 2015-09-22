__author__ = 'dhiraj'

from recsys.algorithm.dbconn import DBConn
from recsys.algorithm.functions import Functions
from recsys.algorithm.baseline import Baseline
from recsys.evaluation.decision import PrecisionRecallF1
from recsys.evaluation.ranking import AveragePrecision
from recsys.evaluation.ranking import MeanAveragePrecision
import operator

import cPickle
import numpy as np
import divisi2
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from divisi2 import DenseMatrix
import random

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
step = 2
start = 10

(prec, recall, F1) = 0.0, 0.0, 0.0
count = 0
precision = []
recall = []
roc_auc = dict()
total_recall = 0.0
total_mean_prec = 0.0
inner_count = 0
filename = "/home/dhiraj/projects/results/avg_precision_results_10-60.txt"

mavgp = MeanAveragePrecision()


with open(filename, "w") as myFile:
    while count < n:
        users = db.get_people_sorted_artists(start, step)

        for user in users:
            TEST_DECISION = []
            GT_DECISION = []

            s_matrix_vector = db.get_sparse_matrix_vector(str(user["_id"]).encode('utf-8'))
            if s_matrix_vector and len(s_matrix_vector[0]['array']) > 0:
                inner_count += 1
                if inner_count < (step+1):
                    v_vectors = functions.compute_v_vectors(s_matrix_vector[0]['col_index'])
                    counts = dict()
                    for vec in s_matrix_vector[0]['array']:
                        artist_id = db.get_label(index=vec)
                        index = baseline._matrix.get().row_index(str(artist_id['artist_id']).encode('utf-8'))
                        count = baseline._matrix.get_value(str(artist_id['artist_id']).encode('utf-8'), str(user["_id"]).encode('utf-8'))
                        counts[index] = count

                    sorted_indexes = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
                    for index, count in sorted_indexes:
                        GT_DECISION.append(index)

                    pred_items = baseline.recommend(user["_id"], n=10, only_unknowns=False, is_row=False, v_vectors=v_vectors, sparse_matrix_vector=s_matrix_vector[0]['array'])
                    for item_id, relevance in pred_items:
                        index = baseline._matrix.get().row_index(str(item_id).encode('utf-8'))
                        TEST_DECISION.append(index)


                    eval = AveragePrecision()
                    eval.load(GT_DECISION, TEST_DECISION)
                    mavgp.load(GT_DECISION, TEST_DECISION)
                    avg_precison = eval.compute()

                    eval2 = PrecisionRecallF1()
                    eval2.load(GT_DECISION, TEST_DECISION)
                    (p, r, f1) = eval2.compute()

                    print "UserID: %s,      Count: %s,      Precision: %s,      Recall: %s      F1: %s      Avg. Precision %s" % (str(user["_id"]).encode('utf-8'), user['artist_distinct_count'], p, r, f1, avg_precison)
                    myFile.write("UserID: " + str(user["_id"]).encode('utf-8') + ", " + "Count: " + str(user['artist_distinct_count']) + ", " + "Avg. Precision: " + str(avg_precison) + "\n")
                    count += 1
                    total_mean_prec += avg_precison
                    # if count == 100:
                    #     break
        if inner_count == step:
            start += 1
            # if start == 10:
            #     start = 9
            inner_count = 0

            #if start % 10 == 0:
                # print "Mean Avg. Precision: %s" % str(mavgp.compute())
                # myFile.write("Mean Avg. Precision: " + str(mavgp.compute()) + "\n")
            # print "Interval: %s,     Mean Avg. Precision: %s" % (start, (float(total_mean_prec) / float(count)))
            # myFile.write("Interval: " + str(start) + ", " + "Mean Avg. Precision: " + str((float(total_mean_prec) / float(count))) + "\n")

myFile.close()
