
from django.shortcuts import render, redirect, get_object_or_404
from . forms import CustomeUserCreationForm, CustomAuthenticationForm, ChangeNickName, ChangeEmail, TopicForm, SectionForm, SubTopicForm, AudioExerciseForm, UserUpdateForm, ChangePasswordForm
from django.contrib.auth import login, logout, authenticate, get_user_model, update_session_auth_hash
from .models import Topic, SubTopic, AudioExercise, Section, User, UserProgress
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.utils.timezone import now, timedelta

# Create your views here.
def home(request):
    return render(request, 'dolphin/home.html')

# def home_view(request):
#     return render(request, 'dolphin/home.html')

def gramma_view(request):
    return render(request, 'dolphin/grammar.html')

def listen_view(request):
    topics = Topic.objects.all()
    return render(request, 'dolphin/listen.html', {'topics':topics})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = CustomAuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user.log_audio_activity()
            messages.success(request, f"Welcome back, {user.nickname.title()}!")

            next_url = request.GET.get('next','home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'dolphin/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        forms = CustomeUserCreationForm(request.POST)
        if forms.is_valid():
            user = forms.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user) 
            user.log_audio_activity()

            return redirect('home')
        else:
            for error in list(forms.errors.values()):
                print(request, error)
    else:
        forms = CustomeUserCreationForm()
    
    context = {'registerform': forms}
    return render(request, 'dolphin/register.html', context=context)

def logout_view(request):
    logout(request)
    return redirect('home')

# <------------- Listen Topic ----------->
def topic_detail(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    query = request.GET.get('q', '')
    level = request.GET.get('level', 'all')

    # Lấy toàn bộ section kèm subtopics cho topic
    sections = Section.objects.filter(topic=topic).prefetch_related('subtopics')

    # Gán subtopics đã lọc vào từng section
    for section in sections:
        subs = section.subtopics.all().order_by('id')

        should_filter = query or (level and level != 'all')

        if should_filter:
            if query:
                subs = subs.filter(title__icontains=query)
            if level and level != 'all':
                subs = subs.filter(level=level)

        section.filtered_subtopics = subs

    return render(request, f'dolphin/listen/{topic_slug}.html', {
        'topic': topic,  # Truyền topic vào template
        'sections': sections  # Truyền danh sách subtopics vào template
    })

def listen_and_type(request, topic_slug, subtopic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    current_subtopic = get_object_or_404(SubTopic, slug=subtopic_slug, topic=topic)
    exercises = AudioExercise.objects.filter(subtopic=current_subtopic).order_by('position')

    # Dùng ID để xác định previous và next subtopic
    previous_subtopic = SubTopic.objects.filter(topic=topic, id__lt=current_subtopic.id).order_by('-id').first()
    next_subtopic = SubTopic.objects.filter(topic=topic, id__gt=current_subtopic.id).order_by('id').first()

    context = {
        "topic": topic,
        "subtopic": current_subtopic,
        "exercises": exercises,
        "previous_subtopic": previous_subtopic,
        "next_subtopic": next_subtopic,
        "is_first_subtopic": previous_subtopic is None,
        "is_last_subtopic": next_subtopic is None,
    }   
    return render(request, 'dolphin/listen/listen_and_type.html', context)
# User
@login_required
def account_information(request):
    user = request.user
    return render(request, 'dolphin/admin_user/account_information.html', {'user':user})

@login_required
def changeNickname(request):
    user = request.user
    if request.method == 'POST':
        form = ChangeNickName(request.POST)
        if form.is_valid():
            new_nickname = form.cleaned_data['nickname']
            if User.objects.exclude(id=user.id).filter(nickname=new_nickname).exists():
                messages.error(request, "Nickname already exists. Please choose another one.")
            else:
                user.nickname = new_nickname
                user.save()
                messages.success(request, "Nickname updated successfully.")
                return redirect("user_account")
    else:
        form = ChangeNickName(initial={'nickname': user.nickname})
    return render(request, 'dolphin/admin_user/edit_nickname.html', {'form': form})

@login_required
def changeEmail(request):
    user = request.user
    if request.method == 'POST':
        form = ChangeEmail(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            if User.objects.exclude(id=user.id).filter(email=new_email).exists():
                messages.error(request, "Email already exists. Please use a different one.")
            else:
                user.email = new_email
                user.save()
                messages.success(request, "Email updated successfully.")
                return redirect("user_account")
    else:
        form = ChangeEmail(initial={'email': user.email})
    return render(request, 'dolphin/admin_user/edit_email.html', {'form': form})


@login_required
def changePassword(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            user.password = make_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('user_account')
    else:
        form = ChangePasswordForm()
    return render(request, 'dolphin/admin_user/change_password.html',{'form':form})

# admin
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    admin_links = {
        'Users':['users'],
        'Topics':['topics','create_topic'],
        'Sections':['sections','create_section'],
        'Subtopics':['subtopics','create_subtopic'],
        'Audio Exercises':['audios','create_audio_exercise'],
    }
    return render(request, 'dolphin/admin_user/admin_dashboard.html',{'admin_links':admin_links})

@user_passes_test(is_admin)
def users(request):
    users_list = User.objects.all().order_by('id')
    return render(request, 'dolphin/admin_user/users.html',{'users':users_list})

@user_passes_test(is_admin)
def topics(request):
    topics_list = Topic.objects.all().order_by('id')
    return render(request, 'dolphin/admin_user/topics.html',{'topics':topics_list})

@user_passes_test(is_admin)
def sections(request):
    sections_list = Section.objects.all().order_by('id')
    return render(request, 'dolphin/admin_user/sections.html',{'sections':sections_list})

@user_passes_test(is_admin)
def subtopics(request):
    subtopics_all = SubTopic.objects.all().order_by('id')
    paginator = Paginator(subtopics_all, 100)
    page = request.GET.get('page')
    subtopics_list = paginator.get_page(page)
    return render(request, 'dolphin/admin_user/subtopics.html',{'subtopics':subtopics_list})

@user_passes_test(is_admin)
def audios(request):
    audios_all = AudioExercise.objects.all().select_related('subtopic').order_by('id')
    paginator = Paginator(audios_all, 100)
    page = request.GET.get('page')
    audios_list = paginator.get_page(page)
    return render(request, 'dolphin/admin_user/audios.html',{'audios':audios_list})

# Create
@user_passes_test(is_admin)
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Topic created successfully!",extra_tags='admin')
            return redirect('topics')
    else:
        form = TopicForm()
    return render(request, 'dolphin/admin_user/create_topic.html', {'form':form})


@user_passes_test(is_admin)
def create_section(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Section created successfully!")
            return redirect('sections')
    else:
        form = SectionForm()
    return render(request, 'dolphin/admin_user/create_section.html', {'form': form})

@user_passes_test(is_admin)
def create_subtopic(request):
    if request.method == 'POST':
        form = SubTopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "SubTopic created successfully!")
            return redirect('subtopics')
    else:
        form = SubTopicForm()
    return render(request, 'dolphin/admin_user/create_subtopic.html', {'form': form})

@user_passes_test(is_admin)
def create_audio_exercise(request):
    if request.method == 'POST':
        form = AudioExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Audio Exercise created successfully!")
            return redirect('audios')
    else:
        form = AudioExerciseForm()
    return render(request, 'dolphin/admin_user/create_audio_exercise.html', {'form': form})

# Update
@user_passes_test(is_admin)
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"User updated successfully!")
            return redirect('users')
    else:
        form = UserUpdateForm()
    return render(request, 'dolphin/admin_user/update_user.html', {'form':form,'user':user})

@user_passes_test(is_admin)
def update_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request,'Topic updated successfully!')
            return redirect('topics')
    else:
        form = TopicForm()
    return render(request, 'dolphin/admin_user/update_topic.html',{'form':form,'topic':topic})

@user_passes_test(is_admin)
def update_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, "Section updated successfully!")
            return redirect('sections')
    else:
        form = SectionForm(instance=section)
    return render(request, 'dolphin/admin_user/update_section.html', {'form': form, 'section':section})

@user_passes_test(is_admin)
def update_subtopic(request, subtopic_id):
    subtopic = get_object_or_404(SubTopic, id=subtopic_id)
    if request.method == 'POST':
        form = SubTopicForm(request.POST, instance=subtopic)
        if form.is_valid():
            form.save()
            messages.success(request, "SubTopic updated successfully!")
            return redirect('subtopics')
    else:
        form = SubTopicForm(instance=subtopic)
    return render(request, 'dolphin/admin_user/update_subtopic.html', {'form': form, 'subtopic':subtopic})

@user_passes_test(is_admin)
def update_audio_exercise(request, audio_id):
    audio_exercise = get_object_or_404(AudioExercise, id=audio_id)
    if request.method == 'POST':
        form = AudioExerciseForm(request.POST, instance=audio_exercise)
        if form.is_valid():
            form.save()
            messages.success(request, "Audio Exercise updated successfully!")
            return redirect('audios')
    else:
        form = AudioExerciseForm(instance=audio_exercise)
    return render(request, 'dolphin/admin_user/update_audio_exercise.html', {'form': form, 'audio':audio_exercise})

# Delete
@user_passes_test(is_admin)
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method =='POST':
        topic.delete()
        messages.success(request,'Topic deleted successfully!')
        return redirect('topics')
    
    return render(request,'dolphin/admin_user/delete_topic.html', {'topic':topic})

@user_passes_test(is_admin)
def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method == 'POST':
        section.delete()
        messages.success(request, "Section deleted successfully!")
        return redirect('sections')
    return render(request, 'dolphin/admin_user/delete_section.html', {'section': section})

@user_passes_test(is_admin)
def delete_subtopic(request, subtopic_id):
    subtopic = get_object_or_404(SubTopic, id=subtopic_id)
    if request.method == 'POST':
        subtopic.delete()
        messages.success(request, "SubTopic deleted successfully!")
        return redirect('subtopics')
    return render(request, 'dolphin/admin_user/delete_subtopic.html', {'subtopic': subtopic})

@user_passes_test(is_admin)
def delete_audio_exercise(request, audio_id):
    audio_exercise = get_object_or_404(AudioExercise, id=audio_id)
    if request.method == 'POST':
        audio_exercise.delete()
        messages.success(request, "Audio Exercise deleted successfully!")
        return redirect('audios')
    return render(request, 'dolphin/admin_user/delete_audio_exercise.html', {'audio_exercise': audio_exercise})

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('users')
    return render(request, 'dolphin/admin_user/delete_user.html', {'user': user})

def user_lesson_history(request, user_id):
    user = get_object_or_404(User, id=user_id)
    completed = UserProgress.objects.filter(user=user, is_completed=True).select_related('subtopic')
    in_progress = UserProgress.objects.filter(user=user, is_completed=False).select_related('subtopic')

    return render(request, 'dolphin/admin_user/user_lesson_history.html', {
        'user':user,
        'completed':completed,
        'in_progress':in_progress
    })