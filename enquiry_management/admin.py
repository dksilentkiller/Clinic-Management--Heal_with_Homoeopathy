from django.contrib import admin
from .models import Appointment,Patient, Feedback, FeedbackMedia, Doctor
# Register your models here.

admin.site.register(Appointment)
admin.site.register(Patient)
admin.site.register(Feedback)
admin.site.register(FeedbackMedia)
admin.site.register(Doctor)
