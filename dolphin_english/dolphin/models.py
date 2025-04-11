from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import date
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email not valid.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields) # Tạo email
        user.set_password(password) # Tạo password
        user.save(using=self._db) # Lưu thông tin vào database

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)   
     
class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    join_date = models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    
    active_days = models.PositiveIntegerField(default=0)
    active_seconds = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname or self.email

    @property
    def total_days(self):
        return (date.today() - self.join_date).days
    
    @property
    def inactive_days(self):
        return self.total_days - self.active_days
    
    @property
    def active_hours(self):
        total_seconds = self.active_seconds
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours} hours {minutes} minutes"
    
    def log_audio_activity(self):
        today = timezone.now().date()
        updated = False

        if self.last_active_date != today:
            self.active_days += 1
            self.last_active_date = today
            updated = True

        self.save()
        return updated

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

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, related_name="user_progress")
    exercise = models.ForeignKey(AudioExercise, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_progress')
    exercise_position = models.PositiveIntegerField(default=1)
    is_completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'subtopic')

    def __str__(self):
        return f'{self.subtopic.title}'
    
    