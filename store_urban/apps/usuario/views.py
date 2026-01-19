from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import make_password
from .models import Usuario
from apps.carrito.models import Carrito
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def registro(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        # Validaciones
        if not all([first_name, last_name, username, email, password, confirmation]):
            return render(request, "registro.html", {"message": "Por favor completa todos los campos."})

        if password != confirmation:
            return render(request, "registro.html", {"message": "Las contraseñas no coinciden."})

        try:
            user = Usuario.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password(password)
            )
            user.save()
            return redirect("login")
        except IntegrityError:
            return render(request, "registro.html", {"message": "El nombre de usuario o correo ya existe."})

    return render(request, "registro.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "login.html", {"message": "Usuario y contraseña son requeridos."})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("/")  # Cambia al inicio de tu tienda
        else:
            return render(request, "login.html", {"message": "Credenciales incorrectas."})

    return render(request, "login.html")

def logout_view(request):
    # Si el usuario está autenticado, elimina los productos de su carrito
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if carrito:
            carrito.items.all().delete()  # Elimina todos los ítems del carrito
    # Realiza el logout del usuario
    logout(request)

    # Redirige a la página de inicio o donde prefieras
    return redirect(reverse("index"))
