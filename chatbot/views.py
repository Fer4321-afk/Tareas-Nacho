# chatbot/views.py - VERSIÓN CON DEBUG
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            from google import genai
            
            # DEBUG: Verificar si se carga la API Key
            api_key = os.getenv("GEMINI_API_KEY")
            print(f"DEBUG - API Key obtenida: {'SÍ' if api_key else 'NO'}")
            if api_key:
                print(f"DEBUG - Primeros chars: {api_key[:10]}...")
            else:
                print("DEBUG - GEMINI_API_KEY no encontrada en entorno")
                print("DEBUG - Variables de entorno:", dict(os.environ))
            
            # Probar con clave hardcodeada temporalmente
            # api_key = "TU_CLAVE_AQUI"  # Descomenta para prueba
            
            if not api_key:
                return JsonResponse({
                    "success": False,
                    "reply": "ERROR: No se encontró API Key. Verifica .env"
                })
            
            client = genai.Client(api_key=api_key)
            
            user_message = request.POST.get("message", "")
            print(f"DEBUG - Mensaje recibido: {user_message}")
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_message
            )
            
            print(f"DEBUG - Respuesta exitosa")
            return JsonResponse({
                "success": True,
                "reply": response.text
            })
            
        except Exception as e:
            print(f"DEBUG - Error: {e}")
            return JsonResponse({
                "success": False,
                "reply": f"Error: {str(e)}"
            })
    
    return render(request, "chatbot/chat.html")

if __name__ == "__main__":
    
    print(os.getenv("GEMINI_API_KEY"))