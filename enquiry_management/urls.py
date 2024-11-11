from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import update_status, edit_appointment, delete_appointment, pending_appointments

urlpatterns = [
    # General Pages
    path('', views.home, name='home'),  
    path('about/', views.about, name='about'),  
    path('doctors/', views.doctors, name='doctors'),
    path('contactus/', views.contactus, name='contactus'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('doc_panel/', views.doc_panel, name='doc_panel'),
    path('doc_dashboard/', views.doc_dashboard, name='doc_dashboard'),
    path('make_appointment/', views.make_appointment, name='make_appointment'),
    
    path('feedback/', views.feedback, name='feedback'),  # Feedback

    path('logout/', LogoutView.as_view(next_page='/', http_method_names=['get', 'post']), name='logout'),  # Logout
    
    # Appointment URLs
    path('all_appointments/', views.all_appointments, name='all_appointments'),
    path('appointments/update-status/<int:appointment_id>/', views.update_status, name='update_status'),
    path('appointments/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),

    path('pending-appointments/', views.pending_appointments, name='pending_appointments'),
    
]

# Add this in your urls.py to serve media files
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

