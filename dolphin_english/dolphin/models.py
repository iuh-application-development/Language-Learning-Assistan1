from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.timezone import now
    

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    levels = models.CharField(
        max_length=100,
        choices=[
            ('A1-C1', 'A1-C1'),
            ('A1-B1', 'A1-B1'),
            ('A2-C1', 'A2-C1'),
            ('B1-C2', 'B1-C2'),
            ('A1', 'A1')
        ],
        default='A1'
    )
    lessons = models.IntegerField(default=0)
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Section(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)
    position = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class SubTopic(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='subtopics', null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topics", null=True, blank=True)
    title = models.CharField(max_length=255)
    level = models.CharField(
        max_length=50,
        choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1')],
        default='A1'
    )
    num_part = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)
    full_textkey = models.TextField(blank=True)
    full_audioSrc = models.URLField()
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class AudioExercise(models.Model):
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, related_name='exercises')
    audioSrc = models.URLField()
    correct_text = models.TextField()
    position = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.subtopic.title
