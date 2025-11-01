from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login, logout

#Registro Usuario
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
           user = form.save()
           login(request, user)
           return redirect("home")  # redirige a la página de inicio
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

#Login Usuarios
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")  # redirige a la página de inicio
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

#Logout Usuario
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect("home")  # redirige a la página de inicio