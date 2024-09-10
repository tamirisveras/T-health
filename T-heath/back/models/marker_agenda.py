from django.db import models
from back.models import Agenda, User


class MarkAgenda(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, verbose_name='Agenda')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')

    def __str__(self):
        return f'Paciente: {self.author}, Agenda: {self.agenda}'