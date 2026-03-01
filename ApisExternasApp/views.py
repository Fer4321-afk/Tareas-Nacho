import requests
from django.shortcuts import render
from django.http import JsonResponse

def pokemon_view(request):
    """Vista principal para buscar Pokémon"""
    
    # Nombre del Pokémon a buscar (por defecto Pikachu)
    name = request.GET.get('name', 'pikachu')
    
    if not name:
        return render(request, 'ApisExternasApp/pokemon.html', {'error': 'Escribe un nombre'})
    
    # Llamar a la API de Pokémon
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Lanza error si no es 200 OK
        data = response.json()
        
        # Procesar datos
        pokemon_data = {
            'name': data['name'].capitalize(),
            'id': data['id'],
            'height': data['height'] / 10,  # Convertir a metros
            'weight': data['weight'] / 10,  # Convertir a kg
            'types': [t['type']['name'] for t in data['types']],
            'image': data['sprites']['front_default'],
            'abilities': [a['ability']['name'] for a in data['abilities'][:3]],
        }
        
        return render(request, 'ApisExternasApp/pokemon.html', {'pokemon': pokemon_data})
    
    except requests.exceptions.HTTPError:
        error_msg = f'Pokémon "{name}" no encontrado'
        return render(request, 'ApisExternasApp/pokemon.html', {'error': error_msg})
    except requests.exceptions.RequestException as e:
        return render(request, 'ApisExternasApp/pokemon.html', {'error': f'Error de conexión: {e}'})
