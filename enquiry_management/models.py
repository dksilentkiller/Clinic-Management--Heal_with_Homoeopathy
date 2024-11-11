from django.db import models
from django.utils import timezone
import pytz  # To manage timezone conversion


# Feedback model
class Feedback(models.Model):
    patient_name = models.CharField(max_length=255)
    rating = models.IntegerField()  # Rating from 1 to 5
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.rating}/5"

# FeedbackMedia model for images and videos
class FeedbackMedia(models.Model):
    feedback = models.ForeignKey(Feedback, related_name='media', on_delete=models.CASCADE)
    media_file = models.FileField(upload_to='feedback_media/')
    MEDIA_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    media_type = models.CharField(max_length=5, choices=MEDIA_CHOICES)

    def __str__(self):
        return f"Media for {self.feedback.patient_name} ({self.media_type})"

######################################################################################
# Gender choices
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

# Utility function to convert time to IST
def convert_to_ist(time):
    ist_timezone = pytz.timezone('Asia/Kolkata')
    return time.astimezone(ist_timezone).strftime('%I:%M %p')

# Appointment model
class Appointment(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    appointment_date = models.DateField()
    disease = models.TextField(blank=True)
    message = models.TextField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # Status field

    def __str__(self):
        created_at_formatted = convert_to_ist(self.created_at)
        return f"Appointment for {self.full_name} on {self.appointment_date} at {created_at_formatted} IST"

############################################################################################
# Patient model
class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    disease = models.CharField(max_length=255, blank=True)  # Optional field
    appointment_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')  # Default status
    document_result_1 = models.FileField(upload_to='documents/', blank=True, null=True)  # Optional field for document upload
    document_result_2 = models.FileField(upload_to='documents/', blank=True, null=True)  # Optional field for document upload

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"


###############################################################################################
# docters model 
from django.contrib.auth.hashers import make_password, check_password

class Doctor(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def save(self, *args, **kwargs):
        if self.pk is None:  # On creation, hash the password
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name
