from django.shortcuts import render, redirect, get_object_or_404
from . forms import CreateUserForm, LoginUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import auth
from .models import Topic, SubTopic, AudioExercise, Section
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    # in ra xin chao
    return render(request, 'dolphin/home.html')

# def home_view(request):
#     return render(request, 'dolphin/home.html')

def gramma_view(request):
    return render(request, 'dolphin/grammar.html')

def listen_view(request):
    topics = Topic.objects.all()
    return render(request, 'dolphin/listen.html', {'topics':topics})

def login_view(request):
    form = LoginUserForm()
    if request.method=="POST":
        form = LoginUserForm(request, request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("home")
    context = {'loginform': form}
    return render(request, 'dolphin/login.html', context=context)


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

# def listen_view_ipa(request):
    topic = Topic.objects.get(slug='ipa')
    ipa_lessons = SubTopic.objects.filter(topic=topic)

    # [
    #     {"title": "/ɪ/ vs /iː/ (it vs eat)", "link": "#"},
    #     {"title": "/b/ - /p/ (big vs pig)", "link": "#"},
    #     {"title": "/tʃ/ - /ʃ/ (cheap vs sheep)", "link": "#"},
    #     {"title": "/s/ - /ʃ/ (so vs show)", "link": "#"},
    #     {"title": "/n/ - /ŋ/ (sin vs sing)", "link": "#"},
    #     {"title": "/d/ - /ð/ (day vs they)", "link": "#"},
    #     {"title": "/t/ - /θ/ (tank vs thank)", "link": "#"},
    #     {"title": "/l/ - /r/ (law vs raw)", "link": "#"},
    #     {"title": "/k/ - /g/ (cold vs gold)", "link": "#"},
    #     {"title": "/e/ - /ɪ/ (bet vs bit)", "link": "#"},
    #     {"title": "/ʧ/ - /t/ (chew vs two)", "link": "#"},
    #     {"title": "/t/ - /d/ (tie vs die)", "link": "#"},        
    #     {"title": "/e/ - /eɪ/ (wet vs wait)", "link": "#"},
    #     {"title": "/f/ - /v/ (fan vs van)", "link": "#"},
    #     {"title": "/v/ - /w/ (vet vs wet)", "link": "#"},
    #     {"title": "/æ/ - /ʌ/ (cat vs cut)", "link": "#"},
    #     {"title": "/f/ - /h/ (fat vs hat)", "link": "#"},
    #     {"title": "/g/ - /w/ (get vs wet)", "link": "#"},        
    #     {"title": "/əʊ/ - /ɔː/ - /ɑː/ (low vs law)", "link": "#"},
    #     {"title": "/f/ - /θ/ (fin vs thin)", "link": "#"},
    #     {"title": "/h/ - /r/ (hat vs rat)", "link": "#"},
    #     {"title": "/ɒ/ - /ɔː/ - /əʊ/ (want vs won't)", "link": "#"},
    #     {"title": "/s/ - /θ/ (sing vs thing)", "link": "#"},
    #     {"title": "/r/ - /w/ (rare vs where)", "link": "#"},
    #     {"title": "/æ/ - /e/ (bad vs bed)", "link": "#"},
    #     {"title": "/ð/ - /z/ (clothe vs close)", "link": "#"},
    #     {"title": "/dʒ/ - /j/ (jam vs yam)", "link": "#"},
    #     {"title": "/ɑ:/ - /ɜ:/ (far vs fur)", "link": "#"},
    #     {"title": "/ʤ/ - /z/ (page vs pays)", "link": "#"},
    #     {"title": "/w/ - no /w/ (wait vs eight)", "link": "#"},
    #     {"title": "/æ/ - /ɑ:/ (had vs hard)", "link": "#"},
    #     {"title": "/d/ - /ʤ/ (dam vs jam)", "link": "#"},
    #     {"title": "/h/ - no /h/ (hand vs and)", "link": "#"},
    #     {"title": "/ɒ/ - /ɑː/ - /ɔ:/ (swan vs sworn)", "link": "#"},
    #     {"title": "/f/ - /p/ (fan vs pan)", "link": "#"},
    #     {"title": "/m/ - /n/ (mine vs nine)", "link": "#"},
    #     {"title": "/əʊ/ - /oʊ/ - /aʊ/ (know vs now)", "link": "#"},
    #     {"title": "/kw/ - /k/ (quick vs kick)", "link": "#"},
    #     {"title": "/s/ - /z/ (bus vs buzz)", "link": "#"},
    #     {"title": "/b/ - /v/ (ban vs van)", "link": "#"},
    #     {"title": "/tʃ/ - /dʒ/ (cheese vs jeez)", "link": "#"},
    #     {"title": "/ŋk/ - /ŋ/ (bank vs bang)", "link": "#"},
    # ]
    return render(request, "dolphin/listen/ipa.html", {"ipas": ipa_lessons})

# def listen_view_numbers(request):
    topic = Topic.objects.get(slug='ipa')
    numbers_lessons = SubTopic.objects.filter(topic=topic)
    # numbers_lessons = [
    #     {"title": "Phone numbers", "link": "#"},
    #     {"title": "Numbers (1)", "link": "#"},
    #     {"title": "Numbers (2)", "link": "#"},
    #     {"title": "Numbers (3)", "link": "#"},
    #     {"title": "Numbers (4)", "link": "#"},
    #     {"title": "Numbers (5)", "link": "#"},
    #     {"title": "Numbers (6)", "link": "#"},
    #     {"title": "Numbers (7)", "link": "#"},
    #     {"title": "Numbers (8)", "link": "#"},
    # ]
    return render(request, 'dolphin/listen/numbers.html', {"inumbers": numbers_lessons})

# def listen_view_spelling_names(request):
    spelling_names_lessons = [
        {"title": "Female Names", "link": "#"},
        {"title": "Last Names", "link": "#"},
        {"title": "Random Letters (British Accent)", "link": "#"},
        {"title": "Male Names", "link": "#"},
        {"title": "Animal names", "link": "#"},
        {"title": "Random Letters (American Accent))", "link": "#"},
    ]
    return render(request, 'dolphin/listen/spelling-names.html', {"ispelling_names": spelling_names_lessons})

def listen_and_type(request, topic_slug, subtopic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    subtopic = get_object_or_404(SubTopic, slug=subtopic_slug)
    exercises = AudioExercise.objects.filter(subtopic=subtopic).order_by('order')

    return render(request, 'dolphin/listen/listen_and_type.html', {
        "topic": topic,
        "subtopic": subtopic,
        "exercises": exercises
    })