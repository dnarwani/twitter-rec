import time
import sys

from django.shortcuts import render
from recsys.algorithm.dbconn import DBConn
from recsys.algorithm.functions import Functions
import settings
import recmusic.wsgi
import tweepy
import json
from RawJsonParser import RawJsonParser
try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict
import HTMLParser
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
import cPickle
import urllib2
import numpy as np
import time
import tweepy
import operator
import MLStripper

reload(sys)
sys.setdefaultencoding("utf-8")

def login(request):
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # URL to where we will redirect to
        redirect_url = request.build_absolute_uri() + "recommend"

        # create the handler
        auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret, redirect_url)

        # get the authorization url (i.e. https://api.twitter.com/oauth/authorize?oauth_token=XXXXXXX)
        # this method automatically grabs the request token first
        # Note: must ensure a callback URL (can be any URL) is defined for the application at dev.twitter.com,
        #       otherwise this will fail (401 Unauthorized)
        try:
            url = auth.get_authorization_url()
        except tweepy.TweepError:
            # failed to get auth url (maybe twitter is down)
            url = request.build_absolute_uri()
            return render(request, url)

        # store the returned values
        request.session['twitter_request_token_key'] = auth.request_token['oauth_token']
        request.session.set_expiry(1800)
        request.session['twitter_request_token_secret'] = auth.request_token['oauth_token_secret']
        request.session.set_expiry(1800)
        request.session['auth'] = cPickle.dumps(auth)
        request.session.set_expiry(1800)

        return HttpResponseRedirect(url)

    # if a GET (or any other method) we'll create a blank form
    else:
        for key in request.session.keys():
            del request.session[key]
        return render(request, 'login.html')

def recommend(request):
    # if this is a POST request we need to process the form data
    db = DBConn()
    functions = Functions()
    if request.method == 'POST':
        user = str(request.session['user']).encode('utf-8')

        if 'more' in request.POST:
            user_id = request.session['user_id']
            upd_sparse_matrix_vec = list(db.get_sparse_matrix_vector(str(user_id).encode('utf-8')))
            if len(upd_sparse_matrix_vec[0]['array']) == 0:
                upd_list = cPickle.loads(str(request.session['artist_indexes']).encode('utf-8'))
            else:
                upd_list = upd_sparse_matrix_vec[0]['array']
                upd_list.extend(cPickle.loads(str(request.session['artist_indexes']).encode('utf-8')))
            db.update_sparse_matrix_vector(user_id, upd_list)

            if "popular" in request.session or "friends" in request.session or "followers" in request.session:
                ranked_items = cPickle.loads(str(request.session["pred_items"]).encode('utf-8'))
                pred_items = sorted(ranked_items.items(), key=operator.itemgetter(1), reverse=True)[:10]

                new_items = dict()
                for artist_id, weight in ranked_items.iteritems():
                    if (artist_id, weight) not in pred_items:
                        new_items[artist_id] = weight

                if len(new_items) > 0:
                    request.session["pred_items"] = cPickle.dumps(new_items)
            else:
                pred_items = recmusic.wsgi.baseline.recommend(request.session["user_id"], n=10, only_unknowns=True, is_row=False, v_vectors=cPickle.loads(str(request.session["v_vectors"]).encode('utf-8')), sparse_matrix_vector=upd_list, col_labels=recmusic.wsgi.col_labels)
            # all_items = cPickle.loads(str(request.session["pred_items"]).encode('utf-8'))
            #
            # if len(all_items) > 0:
            #     pred_items = sorted(all_items.items(), key=operator.itemgetter(1), reverse=True)[:10]
            #
            #     new_items = dict()
            #     for artist_id, weight in all_items.iteritems():
            #         if (artist_id, weight) not in pred_items:
            #             new_items[artist_id] = weight
            #
            #     request.session["pred_items"] = cPickle.dumps(new_items)
        else:

            if "popular" in request.session:
                popular_artists = recmusic.wsgi.popular_artists

                if 'artist_labels' in request.session:
                    artist_labels = cPickle.loads(str(request.session['artist_labels']).encode('utf-8'))
                else:
                    artist_labels = []

                rec_items = dict()
                for artist_id, weight in popular_artists:
                    if artist_id not in artist_labels:
                        rec_items[artist_id] = weight

                pred_items = sorted(rec_items.items(), key=operator.itemgetter(1), reverse=True)[:10]

                new_items = dict()
                for artist_id, weight in rec_items.iteritems():
                    if (artist_id, weight) not in pred_items:
                        new_items[artist_id] = weight


                request.session["pred_items"] = cPickle.dumps(new_items)

            elif "friends" in request.session or "followers" in request.session:
                final_items = cPickle.loads(str(request.session["friends_followers_items"]).encode('utf-8'))
                ranked_items = functions.get_ranked_followers_friends(final_items)
                pred_items = sorted(ranked_items.items(), key=operator.itemgetter(1), reverse=True)[:10]

                new_items = dict()
                for artist_id, weight in ranked_items.iteritems():
                    if (artist_id, weight) not in pred_items:
                        new_items[artist_id] = weight

                request.session["pred_items"] = cPickle.dumps(new_items)
            else:
                pred_items = recmusic.wsgi.baseline.recommend(request.session["user_id"], n=10, only_unknowns=True, is_row=False, v_vectors=cPickle.loads(str(request.session["v_vectors"]).encode('utf-8')), sparse_matrix_vector=cPickle.loads(str(request.session["sparse_vector"]).encode('utf-8')), col_labels=recmusic.wsgi.col_labels)


                # genres = cPickle.loads(str(request.session["genres"]).encode('utf-8'))
                # all_items = cPickle.loads(str(request.session["all_items"]).encode('utf-8'))
                #
                # if len(genres['genres']) > 0:
                #     all_items = functions.get_items_user_genre(recmusic.wsgi.items, all_items, genres)
                #
                # pred_items = all_items[:10]
                #
                # new_items = dict()
                # for artist_id, weight in all_items:
                #     if (artist_id, weight) not in pred_items:
                #         new_items[artist_id] = weight
                #
                # request.session["pred_items"] = cPickle.dumps(new_items)

        tracks = OrderedDict()
        artist_indexes = []

        for item_id, relevance in pred_items:
            artist_indexes.append(recmusic.wsgi.baseline._U.row_index(item_id))

            reverb_artist = db.get_reverbnation_artist(item_id)
            artist_name = recmusic.wsgi.items[item_id].get_data()['name']
            mod_artist_name = HTMLParser.HTMLParser().unescape(artist_name)
            mod_artist_name = MLStripper.strip_tags(mod_artist_name)

            genres = recmusic.wsgi.items[item_id].get_data()['genres']
            mod_genres = HTMLParser.HTMLParser().unescape(genres)

            if reverb_artist['twitter']:
                twitter = reverb_artist['twitter'][0]
            else:
                twitter = ''
            if reverb_artist['facebook']:
                fb = reverb_artist['facebook'][0]
            else:
                fb = ''
            if reverb_artist['youtube']:
                youtube = reverb_artist['youtube'][0]
            else:
                youtube = ''
            if reverb_artist['myspace']:
                myspace = reverb_artist['myspace'][0]
            else:
                myspace = ''
            if reverb_artist['soundcloud']:
                soundcloud = reverb_artist['soundcloud'][0]
            else:
                soundcloud = ''
            if reverb_artist['lastfm']:
                lastfm = reverb_artist['lastfm'][0]
            else:
                lastfm = ''

            if 'popular' in request.session:
                rec_type = 'Popular'
            elif 'friends' in request.session:
                rec_type = 'Friends'
            elif 'followers' in request.session:
                rec_type = 'Followers'
            else:
                rec_type = 'Normal'

            tracks[item_id] = (mod_artist_name, ', '.join(mod_genres), twitter, fb, youtube, myspace, soundcloud, lastfm, rec_type)
            request.session['artist_indexes'] = cPickle.dumps(artist_indexes)
        return render(request, 'view.html', {'tracks': tracks, 'is_authenticated': True, 'name': user, 'user_id': request.session['user_id']})
    else:
        verify(request)
        auth = get_auth(request)
        api = tweepy.API(auth)
        json_api = tweepy.API(auth_handler=auth, parser=RawJsonParser())
        me = api.me()

        user = db.get_user(me.id)

        friends_followers = False
        top_friends = dict()
        top_followers = dict()

        if (user is None) or (user is not None and 'artist_distinct_count' not in user):
            if me.friends_count > 0:
                top_friends = functions.get_top_friends(api.friends_ids, db, me.screen_name)
            if me.followers_count > 0:
                top_followers = functions.get_top_followers(api.followers_ids, db, me.screen_name)

            if len(top_friends) > 0:
                friends_followers = True
                request.session["friends"] = 1
                top_users = top_friends
            elif len(top_followers) > 0:
                friends_followers = True
                request.session["followers"] = 1
                top_users = top_followers

            final_items = []

            artist_labels = []
            if user is not None:
                known_items = list(db.get_sparse_matrix_vector(str(user['_id']).encode('utf-8')))
                if len(known_items[0]['array']) > 0:
                    for item in known_items[0]['array']:
                        artist_labels.append(recmusic.wsgi.baseline._U.row_label(item))

            if friends_followers:
                for user_id, artist_distinct_count in top_users:
                    s_matrix_vector = list(db.get_sparse_matrix_vector(str(user_id).encode('utf-8')))
                    if len(s_matrix_vector) > 0:
                        v_vectors = functions.compute_v_vectors(s_matrix_vector[0]['col_index'])
                        if len(v_vectors) > 0:
                            pred_items = recmusic.wsgi.baseline.recommend(user_id, n=10, only_unknowns=True, is_row=False, v_vectors=v_vectors, sparse_matrix_vector=s_matrix_vector[0]['array'], col_labels=recmusic.wsgi.col_labels)

                            for artist_id, weight in pred_items:
                                if artist_id not in artist_labels:
                                    final_items.append((artist_id, weight))

            if len(final_items) > 0:
                request.session["friends_followers_items"] = cPickle.dumps(final_items)
            else:
                request.session["popular"] = 1
                if len(artist_labels) > 0:
                    request.session['artist_labels'] = cPickle.dumps(artist_labels)

            if user is None:
                request.session["user_id"] = str(db.insert_person(json.loads(json_api.me())))
                db.insert_into_sparse_matrix(index=-1, user_id=request.session['user_id'], values=[])
            else:
                request.session["user_id"] = str(user['_id']).encode('utf-8')

            request.session["user"] = me.name
        else:
            s_matrix_vector = list(db.get_sparse_matrix_vector(str(user['_id']).encode('utf-8')))
            v_vectors = functions.compute_v_vectors(s_matrix_vector[0]['col_index'])
            request.session["v_vectors"] = cPickle.dumps(v_vectors)
            request.session["sparse_vector"] = cPickle.dumps(s_matrix_vector[0]['array'])

            # all_items = recmusic.wsgi.svd.recommend(str(user['_id']).encode('utf-8'), n=200, only_unknowns=True, is_row=False)
            # genres = db.get_genres(str(user['_id']).encode('utf-8'))
            # request.session["all_items"] = cPickle.dumps(all_items)
            # request.session["genres"] = cPickle.dumps(genres)

            request.session["user"] = me.name
            request.session["user_id"] = str(user['_id']).encode('utf-8')

        return render(request, 'recommend.html', {'is_authenticated': True, 'name': me.name})

def verify(request):
        # Twitter will direct with oauth_token and oauth_verifier in the URL
        # ?oauth_token=EoSsg1...&oauth_verifier=NB3bvAkb...
        # did the user deny the request
        if 'denied' in request.GET:
            return False

        # ensure we have a session state and the state value is the same as what twitter returned
        if 'twitter_request_token_key' not in request.session \
           or 'oauth_token' not in request.GET \
           or 'oauth_verifier' not in request.GET \
           or request.session['twitter_request_token_key'] != request.GET['oauth_token']:
            return False
        else:
            return True

def get_auth(request):
    # create the connection
    auth = cPickle.loads(str(request.session['auth']).encode('utf-8'))

    # determine if we've already requested an access token
    if 'twitter_access_token_key' not in request.session:
        # get the access token
        access_token = auth.get_access_token(request.GET['oauth_verifier'])

        # update the stored values
        request.session['twitter_access_token_key'] = access_token[0]
        request.session['twitter_access_token_secret'] = access_token[1]

    else:
        # set the access token
        auth.set_access_token(request.session['twitter_access_token_key'], request.session['twitter_access_token_secret'])

    # create the API instance
    return auth


def get_tracks(request):
    if request.is_ajax():
        try:
            artist_id = str(request.POST['artist_id']).encode('utf-8')
            db = DBConn()
            tracks = dict()
            track_list = db.get_soundcloud_tracks(artist_id)
            for track in track_list:
                tracks[str(track['_id']).encode('utf-8')] = (str(track['title']).encode('utf-8'), str(track['permalink_url']).encode('utf-8'), str(track['duration']).encode('utf-8'))
        except KeyError:
            return HttpResponse('Error')
        return HttpResponse(json.dumps(tracks), content_type="application/json")
    else:
        raise Http404


def feedback(request):
    if request.is_ajax():
        try:
            if 'user_id' in request.POST:
                user_id = str(request.POST['user_id'])
            if 'artist_id' in request.POST:
                artist_id = str(request.POST['artist_id'])
            if 'like_dislike' in request.POST:
                like_dislike = int(request.POST['like_dislike'])
            if 'rank' in request.POST:
                rank = int(request.POST['rank'])
            if 'listen' in request.POST:
                listen = int(request.POST['listen'])
            if 'rec_type' in request.POST:
                rec_type = str(request.POST['rec_type'])
            if 'id' in request.POST:
                soundcloud_id = request.POST['id']

            db = DBConn()
            feedback_exists = db.check_feedback(user_id, artist_id)

            if feedback_exists > 0:
                if 'id' not in request.POST:
                    db.update_feedback(user_id, artist_id, like_dislike, rank, listen, rec_type)
                else:
                    db.update_soundcloud_feedback(user_id, artist_id, soundcloud_id, listen)
            else:
                if 'id' not in request.POST:
                    db.insert_feedback(user_id, artist_id, like_dislike, rank, listen, rec_type)
                else:
                    soundcloud = []
                    soundcloud.append(soundcloud_id)
                    db.insert_soundcloud_feedback(user_id, artist_id, soundcloud, listen)
        except KeyError:
            return HttpResponse('Error')
        return HttpResponse("Success")
    else:
        raise Http404
