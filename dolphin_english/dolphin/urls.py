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
    path("listen/short-stories", views.listen_view_short_stories,name='short-stories'),
    path("listen/conversations", views.listen_view_conversations,name='conversations'),
    path("listen/toeic", views.listen_view_toeic,name='toeic'),
    path("listen/ielts", views.listen_view_ielts,name='ielts'),
    path("listen/toefl", views.listen_view_toefl,name='toefl'),
    path("listen/ipa", views.listen_view_ipa,name='ipa'),
    path("listen/numbers", views.listen_view_numbers,name='numbers'),
    path("listen/spelling-names", views.listen_view_spelling_names,name='spelling-names'),
]