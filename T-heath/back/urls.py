from django.urls import path
from .views import (PatientDetailView, PatientCreateView, PatientUpdateView, Login, Logout,
PatientDeleteView, AgendarCreateView, DoctorRegisterHistory)

urlpatterns = [
    path('', Login.as_view(), name='login_user'),
    path('logout/', Logout.as_view(), name='logout_user'),
    path('patient/detail/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patient/create', PatientCreateView.as_view(), name='patient_create'),
    path('patient/update/<int:pk>', PatientUpdateView.as_view(), name='patient_update'),
    path('patient/delete/<int:pk>', PatientDeleteView.as_view(), name='patient_delete'),
    path('agenda/create/new', AgendarCreateView.as_view(), name='agenda_create'),
    path('agenda/list/', DoctorRegisterHistory.as_view(), name='doctor_register_history'),
]