from numpy import mean
from operator import itemgetter

import os
import sys
import zipfile
try:
    import divisi2
except:
    from csc import divisi2
from numpy import loads
from numpy import fromfile #for large files (U and V)
from divisi2 import DenseVector
from divisi2 import DenseMatrix
from divisi2.ordered_set import OrderedSet

from recsys.algorithm.baseclass import Algorithm
from recsys.algorithm.matrix import SimilarityMatrix
from recsys.algorithm import VERBOSE

TMPDIR = '../recsys/tmp'

class Baseline(Algorithm):
    def __init__(self, filename=None):
        #Call parent constructor
        super(Baseline, self).__init__()

        # self._U: Eigen vector. Relates the concepts of the input matrix to the principal axes
        # self._S (or \Sigma): Singular -or eigen- values. It represents the strength of each eigenvector.
        # self._V: Eigen vector. Relates features to the principal axes
        self._U, self._S, self._V = (None, None, None)
        # Mean centered Matrix: row and col shifts
        self._shifts = None
        # self._matrix_reconstructed: M' = U S V^t
        self._matrix_reconstructed = None

        # Similarity matrix: (U \Sigma)(U \Sigma)^T = U \Sigma^2 U^T
        # U \Sigma is concept_axes weighted by axis_weights.
        self._matrix_similarity = SimilarityMatrix()

        if filename:
            self.load_model(filename)

        # Row and Col ids. Only when importing from SVDLIBC
        self._file_row_ids = None
        self._file_col_ids = None

    def __repr__(self):
        try:
            s = '\n'.join(('M\':' + str(self._reconstruct_matrix()), \
                'A row (U):' + str(self._reconstruct_matrix().right[1]), \
                'A col (V):' + str(self._reconstruct_matrix().left[1])))
        except TypeError:
            s = self._data.__repr__()
        return s

    def load_model(self, filename):
        """
        Loads SVD transformation (U, Sigma and V matrices) from a ZIP file

        :param filename: path to the SVD matrix transformation (a ZIP file)
        :type filename: string
        """
        try:
            zip = zipfile.ZipFile(filename, allowZip64=True)
        except:
            zip = zipfile.ZipFile(filename + '.zip', allowZip64=True)
        # Options file
        options = dict()
        for line in zip.open('README'):
            data = line.strip().split('\t')
            options[data[0]] = data[1]
        try:
            k = int(options['k'])
        except:
            k = 100 #TODO: nasty!!!

        # Load U, S, and V
        """
        #Python 2.6 only:
        #self._U = loads(zip.open('.U').read())
        #self._S = loads(zip.open('.S').read())
        #self._V = loads(zip.open('.V').read())
        """
        try:
            self._U = loads(zip.read('.U'))
        except:
            matrix = fromfile(zip.extract('.U', TMPDIR))
            vectors = []
            i = 0
            while i < len(matrix) / k:
                v = DenseVector(matrix[k*i:k*(i+1)])
                vectors.append(v)
                i += 1
            try:
                idx = [ int(idx.strip()) for idx in zip.read('.row_ids').split('\n') if idx]
            except:
                idx = [ idx.strip() for idx in zip.read('.row_ids').split('\n') if idx]
            #self._U = DenseMatrix(vectors)
            self._U = DenseMatrix(vectors, OrderedSet(idx), None)
        try:
            self._V = loads(zip.read('.V'))
        except:
            matrix = fromfile(zip.extract('.V', TMPDIR))
            vectors = []
            i = 0
            while i < len(matrix) / k:
                v = DenseVector(matrix[k*i:k*(i+1)])
                vectors.append(v)
                i += 1
            try:
                idx = [ int(idx.strip()) for idx in zip.read('.col_ids').split('\n') if idx]
            except:
                idx = [ idx.strip() for idx in zip.read('.col_ids').split('\n') if idx]
            #self._V = DenseMatrix(vectors)
            self._V = DenseMatrix(vectors, OrderedSet(idx), None)

        self._S = loads(zip.read('.S'))

        # Shifts for Mean Centerer Matrix
        self._shifts = None
        if '.shifts.row' in zip.namelist():
            self._shifts = [loads(zip.read('.shifts.row')),
                            loads(zip.read('.shifts.col')),
                            loads(zip.read('.shifts.total'))
                           ]
        self._reconstruct_matrix(shifts=self._shifts, force=True)
        self._reconstruct_similarity(force=True)

    def save_model(self, filename, options={}):
        """
        Saves SVD transformation (U, Sigma and V matrices) to a ZIP file

        :param filename: path to save the SVD matrix transformation (U, Sigma and V matrices)
        :type filename: string
        :param options: a dict() containing the info about the SVD transformation. E.g. {'k': 100, 'min_values': 5, 'pre_normalize': None, 'mean_center': True, 'post_normalize': True}
        :type options: dict
        """
        if VERBOSE:
            sys.stdout.write('Saving svd model to %s\n' % filename)

        f_opt = open(filename + '.config', 'w')
        for option, value in options.items():
            f_opt.write('\t'.join((option, str(value))) + '\n')
        f_opt.close()
        # U, S, and V
        MAX_VECTORS = 2**21
        if len(self._U) < MAX_VECTORS:
            self._U.dump(filename + '.U')
        else:
            self._U.tofile(filename + '.U')
        if len(self._V) < MAX_VECTORS:
            self._V.dump(filename + '.V')
        else:
            self._V.tofile(filename + '.V')
        self._S.dump(filename + '.S')

        # Shifts for Mean Centered Matrix
        if self._shifts:
            #(row_shift, col_shift, total_shift)
            self._shifts[0].dump(filename + '.shifts.row')
            self._shifts[1].dump(filename + '.shifts.col')
            self._shifts[2].dump(filename + '.shifts.total')

        zip = filename
        if not filename.endswith('.zip') and not filename.endswith('.ZIP'):
            zip += '.zip'
        fp = zipfile.ZipFile(zip, 'w', allowZip64=True)

        # Store Options in the ZIP file
        fp.write(filename=filename + '.config', arcname='README')
        os.remove(filename + '.config')

        # Store matrices in the ZIP file
        for extension in ['.U', '.S', '.V']:
            fp.write(filename=filename + extension, arcname=extension)
            os.remove(filename + extension)

        # Store mean center shifts in the ZIP file
        if self._shifts:
            for extension in ['.shifts.row', '.shifts.col', '.shifts.total']:
                fp.write(filename=filename + extension, arcname=extension)
                os.remove(filename + extension)

        # Store row and col ids file, if importing from SVDLIBC
        if self._file_row_ids:
            fp.write(filename=self._file_row_ids, arcname='.row_ids')
        if self._file_col_ids:
            fp.write(filename=self._file_col_ids, arcname='.col_ids')

    def _reconstruct_similarity(self, post_normalize=True, force=True):
        if not self.get_matrix_similarity() or force:
            self._matrix_similarity = SimilarityMatrix()
            self._matrix_similarity.create(self._U, self._S, post_normalize=post_normalize)
        return self._matrix_similarity

    def _reconstruct_matrix(self, shifts=None, force=True):
        if not self._matrix_reconstructed or force:
            if shifts:
                self._matrix_reconstructed = divisi2.reconstruct(self._U, self._S, self._V, shifts=shifts)
            else:
                self._matrix_reconstructed = divisi2.reconstruct(self._U, self._S, self._V)
        return self._matrix_reconstructed

    def _get_row_reconstructed(self, i, zeros=None):
        if zeros:
            return self._matrix_reconstructed.row_named(i)[zeros]
        return self._matrix_reconstructed.row_named(i)

    def _get_col_reconstructed(self, j, zeros=None):
        if zeros:
            return self._matrix_reconstructed.col_named(j)[zeros]
        return self._matrix_reconstructed.col_named(j)

    def compute(self, k=100, min_values=None, pre_normalize=None, mean_center=False, post_normalize=True, savefile=None):

        # Get SparseMatrix
        matrix = self._matrix.get()

        # Mean center?
        shifts, row_shift, col_shift, total_shift = (None, None, None, None)
        if mean_center:
            matrix, row_shift, col_shift, total_shift = matrix.mean_center()
            self._shifts = (row_shift, col_shift, total_shift)

        # Pre-normalize input matrix?
        if pre_normalize:
            """
            Divisi2 divides each entry by the geometric mean of its row norm and its column norm.
            The rows and columns don't actually become unit vectors, but they all become closer to unit vectors.
            """
            if pre_normalize == 'tfidf':
                matrix = matrix.normalize_tfidf() #TODO By default, treats the matrix as terms-by-documents;
                                                  # pass cols_are_terms=True if the matrix is instead documents-by-terms.
            elif pre_normalize == 'rows':
                matrix = matrix.normalize_rows()
            elif pre_normalize == 'cols':
                matrix = matrix.normalize_cols()
            elif pre_normalize == 'all':
                matrix = matrix.normalize_all()
            else:
                raise ValueError("Pre-normalize option (%s) is not correct.\n \
                                  Possible values are: 'tfidf', 'rows', 'cols' or 'all'" % pre_normalize)

        #Compute SVD(M, k)
        self._U, self._S, self._V = matrix.svd(k)

        # Sim. matrix = U \Sigma^2 U^T
        self._reconstruct_similarity(post_normalize=post_normalize, force=True)
        # M' = U S V^t
        self._reconstruct_matrix(shifts=self._shifts, force=True)

        if savefile:
            options = {'k': k, 'min_values': min_values, 'pre_normalize': pre_normalize, 'mean_center': mean_center, 'post_normalize': post_normalize}
            self.save_model(savefile, options)

    def recommend(self, i, n=10, only_unknowns=False, is_row=True):
        """
        Recommends items to a user (or users to an item) using reconstructed matrix :math:`M^\prime = U \Sigma_k V^T`

        E.g. if *i* is a row and *only_unknowns* is True, it returns the higher values of :math:`M^\prime_{i,\cdot}` :math:`\\forall_j{M_{i,j}=\emptyset}`

        :param i: row or col in M
        :type i: user or item id
        :param n: number of recommendations to return
        :type n: int
        :param only_unknowns: only return unknown values in *M*? (e.g. items not rated by the user)
        :type only_unknowns: Boolean
        :param is_row: is param *i* a row (or a col)?
        :type is_row: Boolean
        """
        if not self._matrix_reconstructed:
            self.compute() #will use default values!
        item = None
        zeros = []
        if only_unknowns and not self._matrix.get():
            raise ValueError("Matrix is empty! If you loaded an SVD model you can't use only_unknowns=True, unless svd.create_matrix() is called")
        if is_row:
            if only_unknowns:
                zeros = self._matrix.get().row_named(i).zero_entries()
            item = self._get_row_reconstructed(i, zeros)
        else:
            if only_unknowns:
                zeros = self._matrix.get().col_named(i).zero_entries()
            item = self._get_col_reconstructed(i, zeros)
        return item.top_items(n)