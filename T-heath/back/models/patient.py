from django.db import models
from back.models import User

class Patient(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    address = models.CharField(
        verbose_name='Endereço', max_length=200, blank=True, null=True)
    history = models.TextField(
        verbose_name='Histórico', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return self.user.name if self.user.name else self.user.email
