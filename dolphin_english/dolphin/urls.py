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
    # User & Admin Dashboard
    path('user/account/',views.account_information, name='user_account'),
    path('edit-nickname/', views.changeNickname, name='edit_nickname'),
    path('edit-email/', views.changeEmail, name='edit_email'),
    path('edit-password/<int:user_id>', views.changePassword, name='edit_pass'),
    path('user/<int:user_id>/lessons/',views.user_lesson_history, name='user_lesson_history'),

    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('admin-dashboard/users/', views.users, name='users'),
    path('admin-dashboard/topics/', views.topics, name='topics'),
    path('admin-dashboard/sections/', views.sections, name='sections'),
    path('admin-dashboard/subtopics/', views.subtopics, name='subtopics'),
    path('admin-dashboard/audios/', views.audios, name='audios'),

    path('create-topic/', views.create_topic, name='create_topic'),
    path('create-section/', views.create_section, name='create_section'),
    path('create-subtopic/', views.create_subtopic, name='create_subtopic'),
    path('create-audio-exercise/', views.create_audio_exercise, name='create_audio_exercise'),
    
    path('update-topic/<int:topic_id>/', views.update_topic, name='update_topic'),
    path('update-section/<int:section_id>/', views.update_section, name='update_section'),
    path('update-subtopic/<int:subtopic_id>/', views.update_subtopic, name='update_subtopic'),
    path('update-audio-exercise/<int:audio_id>/', views.update_audio_exercise, name='update_audio_exercise'),
    
    path('delete-topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('delete-section/<int:section_id>/', views.delete_section, name='delete_section'),
    path('delete-subtopic/<int:subtopic_id>/', views.delete_subtopic, name='delete_subtopic'),
    path('delete-audio-exercise/<int:audio_id>/', views.delete_audio_exercise, name='delete_audio_exercise'),

    # User management
    path('update-user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

]