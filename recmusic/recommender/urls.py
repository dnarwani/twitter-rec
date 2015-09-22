from django.conf.urls import url

import views

urlpatterns = [
    url(r'^', views.login, name='login'),
    url(r'^recommend/', views.recommend, name='recommend'),
    url(r'^get_tracks/', views.get_tracks, name='get_tracks'),
    url(r'^feedback/', views.feedback, name='feedback'),
]
