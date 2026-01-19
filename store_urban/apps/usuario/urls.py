from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login_view, name="login"),
    path("registro/", registro, name="registro"),
    path("logout", logout_view, name="logout"),
]