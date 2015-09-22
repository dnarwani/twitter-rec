from django.conf.urls import url

from recmusic.recommender import views


urlpatterns = [
    url(r'^$', views.recommend, name='recommend'),
]
