from django.shortcuts import render ,get_object_or_404
from .models import Person

def blogpage(request):
    visitas = Person.objects.order_by('-id')[:10]  # Inmportar las ultimas 10 personas añadidas mas recientes x -id
    return render(request, 'blog/blog.html', {'visitas': visitas})  # Pasar las personas al contexto del templates+

def personasLista(request, slug):
    person = get_object_or_404(Person, slug=slug)
    return render(request, 'blog/personas.html', {'personas': person})