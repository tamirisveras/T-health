from django.shortcuts import redirect
from django.views import View
from back.forms import AgendaForm, PatientForm
from back.models import Patient, Agenda, User, MarkAgenda
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import logout

class Login(LoginView):

    template_name = 'login_user.html'
    success_url = '/patient/detail'
    
    def get_success_url(self):
        try:
            patient = Patient.objects.get(user=self.request.user)
            return f'/patient/detail/{patient.pk}/'
        except Patient.DoesNotExist:
            return '/'

class Logout(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login_user')

class PatientDetailView(LoginRequiredMixin, DetailView):
     
    model = Patient
    template_name = 'patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agenda'] = MarkAgenda.objects.filter(author=self.object.user)
        return context

class PatientCreateView(CreateView):

    model = Patient
    template_name = 'patient_form.html'
    form_class = PatientForm
    success_url = reverse_lazy('login_user')

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Patient
    template_name = 'patient_form.html'
    fields = ['address', 'history']
    success_url = '/patient/detail'

    def get_success_url(self):
        try:
            patient = Patient.objects.get(user=self.request.user)
            return f'/patient/detail/{patient.pk}/'
        except Patient.DoesNotExist:
            return '/'

class PatientDeleteView(LoginRequiredMixin, DeleteView):
    
    model = User
    template_name = 'patient_confirm_delete.html'
    success_url = reverse_lazy('login_user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object
        return context

class AgendarCreateView(LoginRequiredMixin, CreateView):

    model = Agenda
    template_name = 'agenda_form.html'
    form_class = AgendaForm
    success_url = '/patient/detail'

    def get_success_url(self):
        try:
            patient = Patient.objects.get(user=self.request.user)
            return f'/patient/detail/{patient.pk}/'
        except Patient.DoesNotExist:
            return '/'
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DoctorRegisterHistory(LoginRequiredMixin, ListView):

    model = MarkAgenda
    template_name = 'doctor_register_history.html'
    context_object_name = 'doctor_agenda'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mark_agenda_instance = self.get_queryset().first()  
        if mark_agenda_instance:
            context['patient'] = Patient.objects.get(user=mark_agenda_instance.author)
            context['agenda'] = mark_agenda_instance.agenda
            delete_confirm = self.request.GET.get('delete', None)
            if delete_confirm == 'true':
                # Realiza a deleção da consulta
                mark_agenda_instance.delete()
                context['mark_agenda_deleted'] = True 
        return context

    def post(self, request, *args, **kwargs):
        history_text = request.POST.get('history', '').strip()
        if history_text:
            mark_agenda_instance = self.get_queryset().first()
            if mark_agenda_instance:
                patient = Patient.objects.get(user=mark_agenda_instance.author)
                patient.history = history_text
                patient.save()
        return redirect('doctor_register_history')