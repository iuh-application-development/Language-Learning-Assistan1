from django.contrib import admin
from django.urls import path
from . import views 
urlpatterns = [
    path('', views.home, name='home'),
    path("gramma/", views.gramma_view, name='gramma'), 
    path("listen/", views.listen_view,name='listen'),
    path("listen/ipa", views.listen_view_ipa,name='ipa_listen'),
]