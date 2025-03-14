from django.contrib import admin
from .models import Topic, SubTopic, AudioExercise, Section
# Register your models here.

admin.site.register(Topic)
admin.site.register(Section)
admin.site.register(SubTopic)
admin.site.register(AudioExercise)