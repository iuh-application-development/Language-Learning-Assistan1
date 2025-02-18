from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    # in ra xin chao
    return render(request, 'dolphin/base.html')

def gramma_view(request):
    return render(request, 'dolphin/gramma.html')

def listen_view(request):
    return render(request, 'dolphin/listen.html')

def listen_view_ipa(request):
    return render(request, 'dolphin/ipa.html')