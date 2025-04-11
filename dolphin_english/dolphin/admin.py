from django.contrib import admin
from .models import Topic, SubTopic, AudioExercise, Section, User
# Register your models here.

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Section)
admin.site.register(SubTopic)
admin.site.register(AudioExercise)