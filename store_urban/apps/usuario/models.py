from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'