import os
import subprocess
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

        audio_path = os.path.join(settings.MEDIA_ROOT, 'output_audio.mp3')

        with open(audio_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        model_name = "small"

        try:
            subprocess.run(
                [
                    "whisper",
                    "--language", "pt",
                    "--word_timestamps", "True",
                    "--model", model_name,
                    "--output_dir", f"output-{model_name}",
                    audio_path
                ],
                check=True
            )

            return JsonResponse({"message": "Transcrição gerada com sucesso!"}, status=200)

        except subprocess.CalledProcessError as e:

            return JsonResponse({"error": f"Erro ao transcrever o arquivo: {str(e)}"}, status=500)
