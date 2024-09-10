from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _



class UserManager(UserManager):

    def create_user(self, email: str, password=None, **extra_fields):

        if not email:
            raise ValueError("O E-mail é Obrigatório")

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email: str, password=None, **extra_fields):
     
        if not email:
            raise ValueError("O E-mail è Obrigatório")

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):

    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro')
    ]

    def validate_phone(value: str):
        if len(value) < 11:
            raise ValidationError(_('(%(value)s, número errado, deve ter no minimo 11 digitos. '),
            params={'value': value})

    username = None
    name = models.CharField(
        verbose_name='Nome Completo', max_length=70)
    perfil = models.ImageField(
        verbose_name='Foto de Perfil', blank=True, null=True, upload_to='perfil/')
    email = models.EmailField(
        verbose_name='E-mail', max_length=200, unique=True,
        error_messages={"unique": ('E-mail já Cadastrado!')})
    year = models.DateField(
        verbose_name='Data de Nascimento', blank=True, null=True)
    sex = models.CharField(
        verbose_name='Sexo', max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=17, validators=[validate_phone])
    
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'E-mail'
        verbose_name_plural = 'E-mails'


    def __str__(self) -> str:
        return self.name if self.name else self.email