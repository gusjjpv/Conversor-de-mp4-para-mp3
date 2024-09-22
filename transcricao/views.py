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
            return JsonResponse({"error": "Nenhum arquivo foi enviado."}, status=400)

        if not audio_file.name.endswith('.mp3'):
            return JsonResponse({"error": "Formato de arquivo inválido. Apenas arquivos MP3 são aceitos."}, status=400)

        audio_filename = 'audio.mp3'
        audio_path = os.path.join(settings.MEDIA_ROOT, audio_filename)
        audio_abs_path = os.path.abspath(audio_path)

        try:
            with open(audio_abs_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)
        except Exception as e:
            return JsonResponse({"error": f"Erro ao salvar o arquivo: {str(e)}"}, status=500)

        if not os.path.exists(audio_abs_path):
            return JsonResponse({"error": "Erro ao salvar o arquivo de áudio."}, status=500)

        model = whisper.load_model("small")

        try:
            result = model.transcribe(audio_abs_path, language="pt")
            transcricao = result['text']

            return JsonResponse({"message": "Transcrição gerada com sucesso!", "transcricao": transcricao}, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Erro ao transcrever o arquivo: {str(e)}"}, status=500)
