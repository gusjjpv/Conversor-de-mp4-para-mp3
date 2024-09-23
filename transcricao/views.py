import os
import whisper
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.conf import settings

class TranscribeView(View):
    def get(self, request):
        return render(request, 'transcricao/formulario.html')

    def post(self, request):
        audio_file = request.FILES.get('audio')

        if not audio_file:
            return render(request, 'transcricao/formulario.html', {"error": "Nenhum arquivo foi enviado."})

        if not audio_file.name.endswith('.mp3'):
            return render(request, 'transcricao/formulario.html', {"error": "Formato de arquivo inválido. Apenas arquivos MP3 são aceitos."})

        audio_filename = 'audio.mp3'
        audio_path = os.path.join(settings.MEDIA_ROOT, audio_filename)
        audio_abs_path = os.path.abspath(audio_path)

        try:
            with open(audio_abs_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)
        except Exception as e:
            return render(request, 'transcricao/formulario.html', {"error": f"Erro ao salvar o arquivo: {str(e)}"})

        if not os.path.exists(audio_abs_path):
            return render(request, 'transcricao/formulario.html', {"error": "Erro ao salvar o arquivo de áudio."})

        model = whisper.load_model("small")

        try:
            result = model.transcribe(audio_abs_path, language="pt")
            transcricao = result['text']

            return render(request, 'transcricao/formulario.html', {"transcricao": transcricao})

        except Exception as e:
            return render(request, 'transcricao/formulario.html', {"error": f"Erro ao transcrever o arquivo: {str(e)}"})
