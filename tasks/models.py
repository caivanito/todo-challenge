from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):

    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='Título')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Descripción')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')
    completed = models.BooleanField(default=False, verbose_name='Completada? Si: True | No: False')

    def __str__(self):
        return self.title