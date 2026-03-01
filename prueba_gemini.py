
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("=== PRUEBA CON NUEVA LIBRERÍA google-genai ===")

try:
    # NUEVA FORMA (2025)
    from google import genai
    
    client = genai.Client(api_key=api_key)
    
    print("🤖 Enviando pregunta simple...")
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="Salúdame en una sola palabra"
    )
    
    print(f"✅ Respuesta: {response.text}")
    
except ImportError:
    print("❌ Instala: pip install google-genai")
except Exception as e:
    print(f"❌ Error: {e}")