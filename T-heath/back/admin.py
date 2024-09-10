from django.contrib import admin
from back.models import Doctor, Specialty, Hour, Agenda, Patient, User, MarkAgenda

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Specialty)
admin.site.register(Hour)
admin.site.register(Agenda)
admin.site.register(MarkAgenda)