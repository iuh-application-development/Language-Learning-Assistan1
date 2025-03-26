from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    # path('home/', views.home_view, name='home_view'),
    path("grammar/", views.gramma_view, name='grammar'), 
    path("listen/", views.listen_view,name='listen'),
    path("login/", views.login_view,name='login'),
    path("register/", views.register_view,name='register'),
    path("logout/", views.logout_view,name='logout'),
    # Listen Views
    path('listen/<slug:topic_slug>/', views.topic_detail, name='topic_detail'),
    # Listen and Type
    path('listen/<slug:topic_slug>/<slug:subtopic_slug>/listen-and-type/',views.listen_and_type, name='listen_and_type'),
]