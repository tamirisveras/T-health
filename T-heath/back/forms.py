from django import forms
from .models import Patient, User, Agenda, MarkAgenda
from django.contrib.auth.hashers import make_password


class MedicalHistoryForm(forms.Form):

    history = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Escreva o histórico médico do paciente aqui...',
            'rows': 5
        }),
        label='Registrar Histórico Médico',
        required=True
    )

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control', 
                'id': 'datepicker'
            })
        }
        labels = {
            'data': 'Data da Consulta',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        agenda = super().save(commit=False)
        if commit:
            agenda.save()
            MarkAgenda.objects.create(
                agenda=agenda,
                author=self.user
            )
        return agenda

class PatientForm(forms.ModelForm):
    sex = forms.ChoiceField(choices=User.SEXO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    year = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'dd/mm/yyyy'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    history = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))  # Ajustado para textarea
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "As senhas não coincidem.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data['phone']
        user.year = self.cleaned_data['year']
        user.sex = self.cleaned_data['sex']
        user.password = make_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        Patient.objects.create(
            user=user,
            address=self.cleaned_data['address'],
            history=self.cleaned_data['history'],
        )

        return user
