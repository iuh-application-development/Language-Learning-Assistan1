
from django.shortcuts import render, redirect, get_object_or_404
from . forms import CreateUserForm, LoginUserForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from .models import Topic, SubTopic, AudioExercise, Section
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'dolphin/home.html')

def function(request):
    return render(request, 'dolphin/function.html')

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
        
    if request.method=="POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # User = get_user_model()
            # try:
            #     user = User.objects.get(username=username)
            #     if not user.is_active:
            #         messages.error(request, "Your account has been blocked! Please contact the administrator.")
            #         return redirect('login')
            # except User.DoesNotExist:
            #     user = None

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, "Invalid username or password.")
                return redirect('login')
                

            # Successful login
            login(request, user)
            messages.success(request, f"Welcome back, {username.title()}!")
            return redirect('home')
    else:
        form = LoginUserForm()

    return render(request, 'dolphin/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        forms = CreateUserForm(request.POST)
        if forms.is_valid():
            user = forms.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user) 
            return redirect('home')
        else:
            for error in list(forms.errors.values()):
                print(request, error)
    else:
        forms = CreateUserForm()
    
    context = {'registerform': forms}
    return render(request, 'dolphin/register.html', context=context)

def logout_view(request):
    logout(request)
    return redirect('home')

# <------------- Listen Topic ----------->
def topic_detail(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)  # Lấy topic theo slug
    sections = Section.objects.filter(topic=topic).prefetch_related('subtopics')   # Lấy danh sách subtopics của topic đó

    return render(request, f'dolphin/listen/{topic_slug}.html', {
        'topic': topic,  # Truyền topic vào template
        'sections': sections  # Truyền danh sách subtopics vào template
    })

def listen_and_type(request, topic_slug, subtopic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    subtopic = get_object_or_404(SubTopic, slug=subtopic_slug)
    exercises = AudioExercise.objects.filter(subtopic=subtopic).order_by('position')

    return render(request, 'dolphin/listen/listen_and_type.html', {
        "topic": topic,
        "subtopic": subtopic,
        "exercises": exercises
    })   

