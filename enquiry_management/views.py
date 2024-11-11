from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Appointment

from urllib.parse import urlencode
from urllib.request import urlopen, Request

from django.http import HttpResponse

# Base view - renders the base template
def base(request):
    return render(request, 'base.html')

# Home view - renders the home page
def home(request):
    return render(request, 'home.html')

# About view - renders the about page
def about(request): 
    return render(request, 'about.html') 

# Doctors view - renders the doctors page
def doctors(request):
    return render(request, 'doctors.html')

# Appointment view - renders the appointment page
def make_appointment(request):
    return render(request, 'make_appointment.html')

# Contact Us view - renders the contact us page
def contactus(request):
    return render(request, 'contactus.html')

# Doctor Login view - renders the doctor login page
def doctor_login(request):
    return render(request, 'doctor_login.html')

# Doctor Panel view - renders the doctor panel page
def doc_panel(request):
    return render(request, 'doc_panel.html')

# Doctor Dashboard view - renders the doctor dashboard page
def doc_dashboard(request):
    return render(request, 'doc_dashboard.html')

# Confirmation view - renders the confirmation page
def confirmation(request):
    return render(request, 'confirmation.html')

# New Appointments view - renders the new appointments page
def new_appointments(request):
    return render(request, 'new_appointments.html')

# Feedback view - renders the feedback page
def feedback(request): 
    return render(request, 'feedback.html')


#########################################################################################################################
# feedback 
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback, FeedbackMedia

def feedback(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        rating = request.POST.get('rating')
        comments = request.POST.get('comments')
        media_files = request.FILES.getlist('media_files')  # Get multiple files

        # Save the feedback entry
        feedback = Feedback(
            patient_name=patient_name,
            rating=rating,
            comments=comments
        )
        feedback.save()

        # Save the media files associated with the feedback
        for media_file in media_files:
            # Check if the file is an image or video by the extension
            media_type = 'image' if media_file.content_type.startswith('image') else 'video'
            FeedbackMedia.objects.create(
                feedback=feedback,
                media_file=media_file,
                media_type=media_type
            )

        messages.success(request, 'Thank you for your feedback!')
        return redirect('home')

    return render(request, 'feedback.html')


# to show feedback to home.html
def home(request):
    feedbacks = Feedback.objects.prefetch_related('media').all().order_by('-created_at')  # Fetch all feedbacks with media
    return render(request, 'home.html', {'feedbacks': feedbacks})


#####################################################################################################################

# make_appointment
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Appointment  # Import the Appointment model
from django.utils import timezone

# View to handle appointment booking form submission
def make_appointment(request):
    if request.method == "POST":
        # Extract data from the POST request
        full_name = request.POST.get('name')
        age = request.POST.get('age')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone_number = request.POST.get('phone')
        appointment_date = request.POST.get('appointmentDate')
        disease = request.POST.get('disease', '')  # Optional field
        message = request.POST.get('message', '')  # Optional field
        gender = request.POST.get('gender')

        # Create a new Appointment object with the form data
        appointment = Appointment(
            full_name=full_name,
            age=age,
            city=city,
            state=state,
            phone_number=phone_number,
            appointment_date=appointment_date,
            disease=disease,
            message=message,
            gender=gender,
            created_at=timezone.now(),  # Set created_at to current timestamp
            status='Pending'  # Default status
        )

        # Save the appointment in the database
        appointment.save()

        # # Redirect to a success page or another desired page after successful form submission
        # return redirect('appointment_success')  # Define this in your URLs or change the name as required

    # Render the appointment form if it's a GET request
    return render(request, 'make_appointment.html')  # Replace with your actual template

####################################################################################################################

# login 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

def doctor_login(request):
    if request.method == 'POST':
        # Get login credentials
        contact = request.POST.get('contact')
        password = request.POST.get('password')

        # Authenticate the doctor using either email or mobile number
        doctor = authenticate(username=contact, password=password)  # Assuming doctor login works with Django's User model

        if doctor is not None:
            login(request, doctor)
            return redirect('doc_dashboard')  # Redirect to doctor's dashboard after successful login
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    # Render the doctor login form for GET requests
    return render(request, 'doctor_login.html')



# logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class AdminPanelView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_panel.html'
    login_url = '/'  # Redirect to the login page if not logged in


#####################################################################################################

# doc_panel appointments
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Appointment  # Make sure to adjust the import according to your project structure

# View to list all appointments for doctors
def all_appointments(request):
    # Fetch all appointments ordered by appointment date (most recent first)
    appointments = Appointment.objects.all().order_by('-appointment_date')
    return render(request, 'all_appointments.html', {'appointments': appointments})



from django.shortcuts import redirect, get_object_or_404, render
from .models import Appointment, Patient

def update_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        # Ensure the status is one of the allowed values
        if new_status in ['Pending', 'Accepted', 'Cancelled']:
            appointment.status = new_status
            appointment.save()

            # If the new status is 'Accepted', create a corresponding entry in Patient model
            if new_status == 'Accepted':
                # Check if a Patient record already exists for the given appointment
                if not Patient.objects.filter(full_name=appointment.full_name, phone_number=appointment.phone_number).exists():
                    # Create new patient record
                    patient = Patient(
                        full_name=appointment.full_name,
                        age=appointment.age,
                        gender=appointment.gender,
                        city=appointment.city,
                        phone_number=appointment.phone_number,
                        disease=appointment.disease,
                        appointment_date=appointment.appointment_date,
                        status=new_status  # Set status to 'Accepted'
                    )
                    
                    # Handle file uploads for documents
                    if 'document_result_1' in request.FILES:
                        patient.document_result_1 = request.FILES['document_result_1']
                    if 'document_result_2' in request.FILES:
                        patient.document_result_2 = request.FILES['document_result_2']
                    
                    # Save the patient record to the database
                    patient.save()

        # Redirect to the 'all_appointments' view or any other desired view
        return redirect('all_appointments')

    # Render the appointment status form template if it's a GET request
    return render(request, 'your_template.html', {'appointment': appointment})



def edit_appointment(request, appointment_id):
    # Get the appointment object or return 404 if not found
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        # Update appointment details
        appointment.full_name = request.POST.get('full_name')
        appointment.age = request.POST.get('age')
        appointment.gender = request.POST.get('gender')
        appointment.city = request.POST.get('city')
        appointment.state = request.POST.get('state')
        appointment.phone_number = request.POST.get('phone_number')
        appointment.disease = request.POST.get('disease')
        appointment.appointment_date = request.POST.get('appointment_date')
        
        appointment.save()
        messages.success(request, 'Appointment updated successfully!')
        return redirect('all_appointments')  # Redirect to the appointments list

    return render(request, 'edit_appointment.html', {'appointment': appointment})

def delete_appointment(request, appointment_id):
    # Get the appointment object or return 404 if not found
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
        return redirect('all_appointments')  # Redirect to the appointments list

    return render(request, 'delete_appointment_confirm.html', {'appointment': appointment})


# pending_appointments
from django.shortcuts import render
from .models import Appointment

def pending_appointments(request):
    # Filter appointments with status 'Pending'
    appointments = Appointment.objects.filter(status='Pending')
    return render(request, 'pending_appointments.html', {'appointments': appointments})
