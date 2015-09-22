from recsys.algorithm.baseline import Baseline
from recsys.algorithm.functions import Functions
import cPickle


class Initialize(object):

    def __init__(self):
        baseline = Baseline()
        s_matrix = cPickle.load(open("../recsys/data/sparse_matrix.p"))
        baseline._matrix.set(s_matrix)
        baseline._matrix_and_data_aligned = True
        self.sparse_matrix = s_matrix

        myFunctions = Functions()
        items = myFunctions._read_items("../recsys/data/artists.dat")
        self.artists = items