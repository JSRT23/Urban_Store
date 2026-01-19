from django.contrib import admin
from .models import Usuario
# Register your models here.
admin.site.admin_view(Usuario)