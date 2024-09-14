from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from moviepy.editor import *
import os
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def form(request):
    if request.method == "POST":
        video_file = request.FILES.get('video')

        if video_file:
            video_path = os.path.join(settings.MEDIA_ROOT, video_file.name)

            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            
            with open(video_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            video = VideoFileClip(video_path)
            audio_path = os.path.join(settings.MEDIA_ROOT, "output_audio.mp3")
            video.audio.write_audiofile(audio_path)

            audio_file = open(audio_path, 'rb')
            response = FileResponse(audio_file, as_attachment=True, filename="output_audio.mp3")

            video.close()
            os.remove(video_path)

            return response
        else:
            return HttpResponse("Nenhum vídeo enviado.")
    else:
        return HttpResponse("Método de requisição inválido.")
