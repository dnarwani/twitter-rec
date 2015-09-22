import time

from django.shortcuts import render
from django.core.cache import cache
from recsys.algorithm.functions import Functions
from recsys.algorithm.dbconn import DBConn
from recsys.algorithm.baseline import Baseline

from forms import RecommenderForm
from recmusic.recommender import Initialize


def recommend(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RecommenderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            start_time = time.time()
            init = Initialize()
            db = DBConn()

            user_id = db.get_user_id(form.cleaned_data['twitter_handle'])

            baseline = Baseline()
            baseline._matrix.set(init.sparse_matrix)
            baseline._matrix_and_data_aligned = True
            pred_items = baseline.recommend(user_id, only_unknowns=True, is_row=False)

            items = init.artists
            output = []
            for item_id, relevance in pred_items:
                print items[item_id].get_data()['name']
                output.append(items[item_id].get_data()['name'])
            return render(request, 'index.html', {'listRec': output, 'time': str(time.time() - start_time)})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RecommenderForm()

    return render(request, 'index.html', {'form': form})
