from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import auth
# Create your views here.
def home(request):
    # in ra xin chao
    return render(request, 'dolphin/base.html')

def gramma_view(request):
    return render(request, 'dolphin/grammar.html')

def listen_view(request):
    topics = [
        {
            "title": "Short Stories", 
            "levels": "A1-C1", 
            "lessons": 289, 
            "image": "dolphin/img/short-stories.jpg",
            "link": "short-stories",
        },

        {
            "title": "Conversations", 
            "levels": "A1-B1", 
            "lessons": 100, 
            "image": "dolphin/img/conversations.jpg", 
            "link": "conversations",
        },
            
        {
            "title": "TOEIC Listening", 
            "levels": "A2-C1", 
            "lessons": 600, 
            "image": "dolphin/img/toeic.jpg",
            "link": "toeic", 
        },
        
        {
            "title": "IELTS Listening", 
            "levels": "B1-C2", 
            "lessons": 328, 
            "image": "dolphin/img/ielts.jpg", 
            "link": "ielts", 
        },

        {
            "title": "TOEFL Listening", 
            "levels": "B1-C2", 
            "lessons": 54, 
            "image": "dolphin/img/toefl.jpg", 
            "link": "toefl", 
        },
        
        {
            "title": "IPA", 
            "levels": "A1", 
            "lessons": 42, 
            "image": "dolphin/img/ipa.jpg",
            "link": "ipa",  
         },
        
        {
            "title": "Numbers", 
            "levels": "A1", 
            "lessons": 9, 
            "image": "dolphin/img/numbers.jpg", 
            "link": "numbers", 
        },
        
        {
            "title": "Spelling Names", 
            "levels": "A1", 
            "lessons": 6, 
            "image": "dolphin/img/spelling-names.jpg", 
            "link": "spelling-names", 
         },
    ]
    return render(request, 'dolphin/listen.html', {'topics': topics})

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

def listen_view_short_stories(request):
    return render(request, 'dolphin/listen/short-stories.html')

def listen_view_conversations(request):
    return render(request, 'dolphin/listen/conversations.html')

def listen_view_toeic(request):
    return render(request, 'dolphin/listen/toeic.html')

def listen_view_ielts(request):
    return render(request, 'dolphin/listen/ielts.html')

def listen_view_toefl(request):
    return render(request, 'dolphin/listen/toefl.html')

def listen_view_ipa(request):
    ipa_lessons = [
        {"title": "/ɪ/ vs /iː/ (it vs eat)", "link": "#"},
        {"title": "/b/ - /p/ (big vs pig)", "link": "#"},
        {"title": "/tʃ/ - /ʃ/ (cheap vs sheep)", "link": "#"},
        {"title": "/s/ - /ʃ/ (so vs show)", "link": "#"},
        {"title": "/n/ - /ŋ/ (sin vs sing)", "link": "#"},
        {"title": "/d/ - /ð/ (day vs they)", "link": "#"},
        {"title": "/t/ - /θ/ (tank vs thank)", "link": "#"},
        {"title": "/l/ - /r/ (law vs raw)", "link": "#"},
        {"title": "/k/ - /g/ (cold vs gold)", "link": "#"},
        {"title": "/e/ - /ɪ/ (bet vs bit)", "link": "#"},
        {"title": "/ʧ/ - /t/ (chew vs two)", "link": "#"},
        {"title": "/t/ - /d/ (tie vs die)", "link": "#"},        
        {"title": "/e/ - /eɪ/ (wet vs wait)", "link": "#"},
        {"title": "/f/ - /v/ (fan vs van)", "link": "#"},
        {"title": "/v/ - /w/ (vet vs wet)", "link": "#"},
        {"title": "/æ/ - /ʌ/ (cat vs cut)", "link": "#"},
        {"title": "/f/ - /h/ (fat vs hat)", "link": "#"},
        {"title": "/g/ - /w/ (get vs wet)", "link": "#"},        
        {"title": "/əʊ/ - /ɔː/ - /ɑː/ (low vs law)", "link": "#"},
        {"title": "/f/ - /θ/ (fin vs thin)", "link": "#"},
        {"title": "/h/ - /r/ (hat vs rat)", "link": "#"},
        {"title": "/ɒ/ - /ɔː/ - /əʊ/ (want vs won't)", "link": "#"},
        {"title": "/s/ - /θ/ (sing vs thing)", "link": "#"},
        {"title": "/r/ - /w/ (rare vs where)", "link": "#"},
        {"title": "/æ/ - /e/ (bad vs bed)", "link": "#"},
        {"title": "/ð/ - /z/ (clothe vs close)", "link": "#"},
        {"title": "/dʒ/ - /j/ (jam vs yam)", "link": "#"},
        {"title": "/ɑ:/ - /ɜ:/ (far vs fur)", "link": "#"},
        {"title": "/ʤ/ - /z/ (page vs pays)", "link": "#"},
        {"title": "/w/ - no /w/ (wait vs eight)", "link": "#"},
        {"title": "/æ/ - /ɑ:/ (had vs hard)", "link": "#"},
        {"title": "/d/ - /ʤ/ (dam vs jam)", "link": "#"},
        {"title": "/h/ - no /h/ (hand vs and)", "link": "#"},
        {"title": "/ɒ/ - /ɑː/ - /ɔ:/ (swan vs sworn)", "link": "#"},
        {"title": "/f/ - /p/ (fan vs pan)", "link": "#"},
        {"title": "/m/ - /n/ (mine vs nine)", "link": "#"},
        {"title": "/əʊ/ - /oʊ/ - /aʊ/ (know vs now)", "link": "#"},
        {"title": "/kw/ - /k/ (quick vs kick)", "link": "#"},
        {"title": "/s/ - /z/ (bus vs buzz)", "link": "#"},
        {"title": "/b/ - /v/ (ban vs van)", "link": "#"},
        {"title": "/tʃ/ - /dʒ/ (cheese vs jeez)", "link": "#"},
        {"title": "/ŋk/ - /ŋ/ (bank vs bang)", "link": "#"},
    ]
    return render(request, "dolphin/listen/ipa.html", {"ipas": ipa_lessons})


def listen_view_numbers(request):
    return render(request, 'dolphin/listen/numbers.html')

def listen_view_spelling_names(request):
    return render(request, 'dolphin/listen/spelling-names.html')