"""
WSGI config for recmusic project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recmusic.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "recmusic.settings"

from recsys.algorithm.baseline import Baseline
from recsys.algorithm.factorize import SVD
from recsys.algorithm.functions import Functions
from recsys.algorithm.dbconn import DBConn
from boto.s3.connection import S3Connection
from divisi2 import DenseMatrix


import boto
import cPickle
import urllib2
import cStringIO
import numpy as np
import divisi2


conn = S3Connection('AKIAI6F6HFFENFWSPN4Q', 'aP0OOVDj96AFUEr9vbHalvvNZz7rNNXyyH0Wof7i')
bucket = conn.get_bucket('elasticbeanstalk-us-west-2-501394068089')

artist_key = bucket.get_key('files/data/artists.dat')
artist_path = artist_key.generate_url(3600, query_auth=True, force_http=True)
artist_content = urllib2.urlopen(artist_path).read()

myFunctions = Functions()
items = myFunctions._read_items(filename=artist_content)

row_labels_key = bucket.get_key('files/data/row_labels.p')
row_labels_path = row_labels_key.generate_url(3600, query_auth=True, force_http=True)


baseline = Baseline()
db = DBConn()

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

row_labels = cPickle.load(urllib2.urlopen(row_labels_path))
baseline._U = DenseMatrix(u_vectors, row_labels)
baseline._S = s_array

col_labels_key = bucket.get_key('files/data/col_labels.p')
col_labels_path = col_labels_key.generate_url(3600, query_auth=True, force_http=True)
col_labels = cPickle.load(urllib2.urlopen(col_labels_path))

popular_key = bucket.get_key('files/data/popular.p')
popular_path = popular_key.generate_url(3600, query_auth=True, force_http=True)
popular_artists = cPickle.load(urllib2.urlopen(popular_path))

pred_items = popular_artists

# ld_occurrences_key = bucket.get_key('files/data/ld_occurrences.dat')
# ld_occurrences_path = ld_occurrences_key.generate_url(3600, query_auth=True, force_http=True)
# ld_occurrences_content = urllib2.urlopen(ld_occurrences_path).read()
#
# svd = SVD()
# svd.load_data(filename=ld_occurrences_content, sep='::', format={'col':0, 'row':1, 'value':2, 'ids': str})


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
