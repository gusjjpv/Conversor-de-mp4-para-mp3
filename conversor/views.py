from django.shortcuts import render
from django.http import HttpResponse
from moviepy.editor import *
# Create your views here.

def home(request):
    return render(request, 'home.html')

def form(request):
    video = request.POST.get('video')
    return HttpResponse(video)
