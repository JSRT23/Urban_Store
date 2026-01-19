from django.db import models
from colorfield.fields import ColorField 
from django.conf import settings
# Create your models here.

class Genero(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre 


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name='categorias')

    def __str__(self):
        return f'{self.nombre} - {self.genero.nombre}'


class SubCategoria(models.Model):
    nombre = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')

    def __str__(self):
        return f'{self.nombre} - {self.categoria.nombre}-{self.categoria.genero.nombre}'


class Color(models.Model):
    nombre = models.CharField(max_length=30)
    rgb =ColorField(default='#FFFFFF')# Hex color code
    def __str__(self):
        return f'{self.nombre}'


class Talla(models.Model):
    nombre = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.nombre}'


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen_principal = models.ImageField(upload_to='static/img/productos', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=100,  unique=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.nombre}-{self.codigo}'


class ProductoVariante(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='variantes')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='static/img/variantes', null=True, blank=True)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, related_name='variantes')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    disponible = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('producto', 'color', 'talla', 'subcategoria')

    def __str__(self):
        return f'{self.producto.nombre} - {self.color.nombre} - {self.talla.nombre}'

class Favorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    producto_variante = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE)
    fecha_guardado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'producto_variante')

    def __str__(self):
        return f"{self.usuario} - {self.producto_variante}"
    
class Ofertas(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    mostrar = models.BooleanField(default=True)
    img = models.ImageField(upload_to='static/img/ofertas', null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class colecciones(models.Model):
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    mostrar = models.BooleanField(default=True)
    img = models.ImageField(upload_to='static/img/colecciones', null=True, blank=True)
    
    def __str__(self):
        return f'coleccion: {self.genero.nombre} '