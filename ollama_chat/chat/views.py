from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain_ollama import OllamaLLM
import json

def chat_home(request):
    return render(request, 'chat/chat.html')

@csrf_exempt
def get_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({'error': 'Empty message'}, status=400)
            
            model = OllamaLLM(model='deepseek-r1:1.5b')
            response = model.invoke(input=user_message)
            
            # Clean response
            think_end = response.find("</think>")
            if think_end != -1:
                clean_response = response[think_end + 8:]
            else:
                clean_response = response
                
            return JsonResponse({'response': clean_response.strip()})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)