from django.shortcuts import render


def basepage(request):
    return render(request, 'base.html') 

def blogpage(request):
    
    return render(request, 'blog/blog.html')

def home(request):
    return render(request, 'home.html')
