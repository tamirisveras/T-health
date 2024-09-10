from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date
from back.models import User


class Specialty(models.Model):

    name_specialty = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name_specialty


class Doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    crm = models.CharField(max_length=30, unique=True ,blank=False, null=False)
    specialty = models.ForeignKey(Specialty, on_delete= models.CASCADE, verbose_name="Especialidade", blank=False)

    def __str__(self):
        return self.user.name + ' - ' + self.specialty.name_specialty


class Hour(models.Model):

    hour = models.CharField(max_length=5, blank=False, name=False)

    def __str__(self):
        return self.hour


class Agenda(models.Model):

    def validate_schedule(value: str):
        global data
        data = value
        data_hj = date.today()

        if data < data_hj:
            raise ValidationError('Não é possível selecionar uma data já passada!')

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Médico Especialista", blank=False)
    data = models.DateField(validators=[validate_schedule])
    hours = models.ManyToManyField(Hour, blank=False)

    def __str__(self):
        return str(self.data) + ' - ' + self.doctor.user.name + ' - ' + self.doctor.specialty.name_specialty