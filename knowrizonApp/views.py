import json
import logging
import uuid
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.shortcuts import render
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from google.auth.transport.requests import Request
from google.oauth2 import id_token
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.functions import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.http import MediaIoBaseDownload

from .forms import BulkStudentUploadForm, BulkStaffUploadForm
from .models import Admin, content_managers, researchers, PDF_materials, Journal_materials
from .models import academic_staff  # Ensure you have the 'students' model imported

logger = logging.getLogger(__name__)

import logging

# import drivefolders_API


logger = logging.getLogger(__name__)

import logging
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout
import logging

logger = logging.getLogger(__name__)

import logging
import pandas as pd

logger = logging.getLogger(__name__)


# Create your views here.

def index(request):
    return render(request, 'web/index.html')


def login_decider(request):
    return render(request, 'web/login_router.html')


def admin_login(request):
    return render(request, 'admin_login.html')


def admin_dasahboard(request):
    return render(request, 'admin_dashboard.html')


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')  # Check if "Remember Me" was selected

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)

            # Set session expiry based on "Remember Me"
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks in seconds
            else:
                request.session.set_expiry(0)  # Session expires when the browser closes

            messages.success(request, 'Login successful')
            logger.info('Login successful')
            # get admin details for display on the dashboard page and pass it to the template
            admin = Admin.objects.get(admin_email=email)
            admin_name = admin.admin_fname + ' ' + admin.admin_lname
            request.session['admin_name'] = admin_name
            request.session['admin_email'] = admin.admin_email
            request.session['admin_dept'] = admin.admin_dept
            request.session['admin_id'] = admin.admin_id

            return render(request, 'admin_dashboard.html',
                          {'admin_name': admin_name, 'admin_email': admin.admin_email, 'admin_dept': admin.admin_dept})

        else:
            messages.error(request, 'Invalid email or password')
            logger.error('Invalid email or password')
            print('Invalid email or password')

    return render(request, 'admin_login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def admin_register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        email = request.POST.get('email', '')
        department = request.POST.get('department', '')
        password = request.POST.get('password', '')
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(username=email, password=password)
            Admin.objects.create(admin_fname=fname, admin_lname=lname, admin_email=email, admin_password=password,
                                 admin_dept=department)
            messages.success(request, 'Admin registered successfully')

            return redirect('admin_login')
    return render(request, 'admin_register.html')


import logging

logger = logging.getLogger(__name__)


# admin view functions
# add users
def add_user(request):
    return render(request, 'includes/admin_add_users/add_users.html')


def staff_login(request):
    return render(request, 'staff_login.html')


def content_manager_login(request):
    return render(request, 'content_manager_login.html')


def researcher_login(request):
    return render(request, 'researcher_login.html')


def add_student(request):
    if request.method == 'POST':
        studen_name = request.POST.get('student_name', '').strip()
        email = request.POST.get('student_email', '').strip()
        department = request.POST.get('student_department', '').strip()
        matric_no = request.POST.get('student_mat_no', '').strip()
        gender = request.POST.get('student_gender', '').strip()
        generic_password = 'password'  # Default password for all students

        # Check if all required fields are provided
        if not all([studen_name, email, department, matric_no, gender]):
            messages.error(request, 'All fields are required')
            logger.error('All fields are required')
            return render(request, 'includes/admin_add_users/add_users.html')

        # Check if email AND MATRIC NUMBER already exists IN STUDENTS DATABASE
        if students.objects.filter(student_email=email).exists() or students.objects.filter(
                student_matric_no=matric_no).exists():
            messages.error(request, 'Email already exists')
            logger.error('student is registered; Email or Matric_no already exists')
            return render(request, 'includes/admin_add_users/add_users.html')

        try:
            # Create a new user
            user = User.objects.create_user(username=email, password=generic_password)

            # Ensure fields are correctly mapped to your model attributes and password is hashed

            student = students.objects.create(
                student_name=studen_name,
                student_email=email,
                student_password=generic_password,  # Encrypt if storing
                student_gender=gender,
                student_dept=department,
                student_matric_no=matric_no
            )

            messages.success(request, 'Student registered successfully')
            logger.info('Student registered successfully')
            return redirect(request, 'includes/admin_add_users/add_users.html')

        except Exception as e:
            # Log any unexpected errors and show a generic error message
            logger.error(f'Error occurred while registering student: {e}')

    # Render the form if not POST or on error
    return render(request, 'includes/admin_add_users/add_users.html')


def bulk_upload_students(request):
    if request.method == 'POST':
        form = BulkStudentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Process the valid Excel file
            file = form.cleaned_data['file']

            try:
                # Read the Excel file using pandas
                df = pd.read_excel(file, engine='openpyxl')

                # Create a timestamp for the file storage
                current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

                # Define the file path to save the uploaded file as CSV temporarily
                filename = f'students_bulk_upload_{current_date}.csv'
                file_path = os.path.join(settings.MEDIA_ROOT, 'knowrizonApp/studentrecords_upload', filename)

                # Save the dataframe as a CSV file
                df.to_csv(file_path, index=False)

                # Iterate over each row and save student data into the database
                for _, row in df.iterrows():
                    students.objects.create(
                        student_name=row.get('student_name', ''),
                        student_password="password",
                        student_gender=row.get('student_gender', ''),
                        student_dept=row.get('student_dept', ''),  # Corrected field name
                        student_matric_no=row.get('student_matric_number', '')  # Corrected field name
                    )

                # Display success message after processing
                messages.success(request, 'Students uploaded successfully!')
            except Exception as e:
                # Handle any exception during file reading or database insertion
                messages.error(request, f"An error occurred while processing the file: {str(e)}")
        else:
            messages.error(request, 'Invalid form submission. Please upload a valid Excel file.')

    return render(request, 'includes/admin_add_users/add_users.html', {'form': form})


def upload_students_records(request):
    return render(request, 'includes/admin_add_users/add_students_bulk_upload.html')


def add_academic_staff(request):
    if request.method == 'POST':
        fname = request.POST.get('academic_staff_fname', '').strip()
        lname = request.POST.get('academic_staff_lname', '').strip()
        email = request.POST.get('academic_staff_email', '').strip()
        department = request.POST.get('academic_staff_department', '').strip()
        gender = request.POST.get('academic_staff_gender', '').strip()
        password_generic = 'password'  # Default password for all academic staff
        phone = request.POST.get('academic_staff_phone', '').strip()
        position = request.POST.get('academic_staff_position', '').strip()
        interest = request.POST.get('academic_staff_interest', '').strip()
        staffid = request.POST.get('academic_staff_id', '').strip()
        prefix = request.POST.get('academic_staff_prefix', '').strip()

        if not all([fname, lname, email, department, staffid, interest, phone, position, prefix, gender]):
            messages.error(request, 'All fields are required')
            logger.error('All fields are required')
            return render(request, 'includes/admin_add_users/add_users.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already exists')
            logger.error('Email already exists')
            return render(request, 'includes/admin_add_users/add_users.html')
        else:
            user = User.objects.create_user(username=email)
            academic_staff.objects.create(
                academic_staff_fname=fname,
                academic_staff_lname=lname,
                academic_staff_email=email,
                academic_staff_password=password_generic,
                academic_staff_identity=staffid,
                academic_staff_interest=interest,
                academic_staff_dept=department,
                academic_staff_position=position,
                academic_staff_phone=phone,
                academic_staff_prefix=prefix,
                academic_staff_gender=gender
            )
            messages.success(request, 'Academic staff registered successfully')
            logger.info('Academic staff registered successfully')
            return render(request, 'includes/admin_add_users/add_users.html')

    return render(request, 'includes/admin_add_users/add_users.html')


def upload_staff_records(request):
    return render(request, 'includes/admin_add_users/add_staff_bulk_upload.html')


def process_bulk_staff_upload(request):
    if request.method == 'POST':
        form = BulkStaffUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Process the valid Excel file
            file = form.cleaned_data['file']

            try:
                # Read the Excel file using pandas
                df = pd.read_excel(file, engine='openpyxl')

                # Create a timestamp for the file storage
                current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

                # Define the file path to save the uploaded file as CSV temporarily
                filename = f'staff_bulk_upload_{current_date}.csv'
                file_path = os.path.join(settings.MEDIA_ROOT, 'knowrizonApp/staffrecords_upload', filename)

                # Save the dataframe as a CSV file
                df.to_csv(file_path, index=False)

                # Iterate over each row and save staff data into the database
                for _, row in df.iterrows():
                    academic_staff.objects.create(
                        academic_staff_prefix=row.get('academic_prefix', ''),
                        academic_staff_identity=row.get('academic_staff_identity', ''),
                        academic_staff_position=row.get('academic_staff_position', ''),
                        academic_staff_dept=row.get('academic_staff_dept', ''),
                        academic_staff_phone=row.get('academic_staff_phone', ''),
                        academic_staff_fname=row.get('academic_staff_fname', ''),
                        academic_staff_lname=row.get('academic_staff_lname', ''),
                        academic_staff_email=row.get('academic_staff_email', ''),
                        academic_staff_password="password",
                    )
                messages.success(request, 'Staff uploaded successfully!')
            except Exception as e:
                # Handle any exception during file reading or database insertion
                messages.error(request, f"An error occurred while processing the file: {str(e)}")
        else:
            messages.error(request, 'Invalid form submission. Please upload a valid Excel file.')

    return render(request, 'includes/admin_add_users/add_users.html', {'form': form})


def add_content_manager(request):
    if request.method == 'POST':
        fname = request.POST.get('content_manager_fname', '').strip()
        lname = request.POST.get('content_manager_lname', '').strip()
        email = request.POST.get('content_manager_email', '').strip()
        prefix = request.POST.get('content_manager_prefix', '').strip()
        department = request.POST.get('content_manager_department', '').strip()
        password_generic = 'password'  # Default password for all content managers
        phone = request.POST.get('content_manager_phone', '').strip()

        if not all([fname, lname, email, department, phone]):
            messages.error(request, 'All fields are required')
            print(fname, lname, email, department, phone)
            logger.error('All fields are required')
            return render(request, 'includes/admin_add_users/add_users.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already exists')
            logger.error('Email already exists')
            return render(request, 'includes/admin_add_users/add_users.html')
        else:
            user = User.objects.create_user(username=email, password=password_generic)
            content_managers.objects.create(
                content_manager_fname=fname,
                content_manager_lname=lname,
                content_manager_email=email,
                content_manager_prefix=prefix,
                content_manager_password=password_generic,
                content_manager_dept=department,
                contet_manager_phone=phone
            )
            messages.success(request, 'Content manager registered successfully')
            logger.info('Content manager registered successfully')
            return render(request, 'includes/admin_add_users/add_users.html')

    return render(request, 'includes/admin_add_users/add_content_managers.html')


def add_researcher(request):
    if request.method == 'POST':
        fname = request.POST.get('researcher_fname', '').strip()
        lname = request.POST.get('researcher_lname', '').strip()
        email = request.POST.get('researcher_email', '').strip()
        prefix = request.POST.get('researcher_prefix', '').strip()
        department = request.POST.get('researcher_department', '').strip()
        password_generic = 'password'  # Default password for all content managers
        phone = request.POST.get('researcher_phone', '').strip()
        interest = request.POST.get('researcher_interest', '').strip()
        if not all([fname, lname, email, department, phone, interest]):
            messages.error(request, 'All fields are required')
            logger.error('All fields are required')
            return render(request, 'includes/admin_add_users/add_users.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already exists')
            logger.error('Email already exists')
            return render(request, 'includes/admin_add_users/add_users.html')
        else:
            user = User.objects.create_user(username=email, password=password_generic)
            researchers.objects.create(
                researcher_fname=fname,
                researcher_lname=lname,
                researcher_email=email,
                researcher_prefix=prefix,
                researcher_password=password_generic,
                researcher_dept=department,
                researcher_phone=phone,
                researcher_interest=interest
            )
            messages.success(request, 'Researcher registered successfully')
            logger.info('Researcher registered successfully')
            return render(request, 'includes/admin_add_users/add_users.html')

    return render(request, 'includes/admin_add_users/add_researcher.html')


###  MANAGING USERS RECORDS


def manage_students(request):
    all_students = students.objects.all()  # Correctly define and assign the 'students' variable
    return render(request, 'admin_manages_users/admin_manage_students.html', {'students': all_students})


def manage_academic_staff(request):
    all_academic_staff = academic_staff.objects.all()  # Correctly define and assign the 'academic_staff' variable
    return render(request, 'admin_manages_users/admin_manage_staff.html', {'academic_staff': all_academic_staff})


# views.py


from .forms import AcademicStaffForm


# views.py

def admin_manage_staff_update(request, academic_staff_id):
    staff = get_object_or_404(academic_staff, pk=academic_staff_id)
    if request.method == 'POST':
        form = AcademicStaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('manage_staff_users')
    else:
        form = AcademicStaffForm(instance=staff)
    return render(request, 'admin_manages_users/admin_updates_staff_records.html', {'form': form})


def admin_manage_staff_delete(request, academic_staff_id):
    staff = get_object_or_404(academic_staff, pk=academic_staff_id)
    if request.method == 'POST':
        staff.delete()
        return redirect('manage_staff_users')
    return render(request, 'admin_manages_users/admin_deletes_staff_record.html', {'staff': staff})


def library_materials_category(request):
    return render(request, 'library_material_category.html')


def approve_requests(request):
    if request.method == 'POST':
        # Handle approving requests logic
        pass
    return render(request, 'approve_requests.html')


def manage_user_roles(request):
    if request.method == 'POST':
        # Handle managing user roles logic
        pass
    return render(request, 'manage_user_roles.html')


def handle_password_resets(request):
    if request.method == 'POST':
        # Handle password resets logic
        pass
    return render(request, 'handle_password_resets.html')


def monitor_user_activity(request):
    return render(request, 'monitor_user_activity.html')


def oversee_user_permissions(request):
    return render(request, 'oversee_user_permissions.html')


# USERS LOGIN

from django.contrib.auth.hashers import check_password

from django.shortcuts import get_object_or_404

from django.contrib.auth import login as auth_login


def student_login(request):
    if request.method == 'POST':
        matric_no = request.POST.get('mat_no')
        password = request.POST.get('password')

        # Check if matric number or password is empty
        if not matric_no or not password:
            messages.error(request, 'Matric number and password are required.')
            logger.warning('Login attempt with missing credentials.')
            return render(request, 'users/students/students_login.html')

        # Fetch the student using matric_no
        student = students.objects.filter(student_matric_no=matric_no).first()

        if not student:
            # If no student is found
            messages.error(request, 'Account not found. Please register with the admin.')
            logger.error('No student found for matric_no: %s', matric_no)
            return render(request, 'users/students/students_login.html')

        # Check if the password is the default "password"
        if password == "password":
            # Extract student's name from the student instance, not from the User model
            student_name = student.student_name  # or student.student_name if the field exists
            messages.warning(request, f' please update your password.')
            logger.info('Prompting student to update password for matric_no: %s', matric_no)
            return render(request, 'users/students/student_update_password.html', {'student': student})

        # Compare the passwords using Django's built-in check_password function since the password is hashed in the users table

        if check_password(password, student.student_password):
            # Log the student in
            auth_login(request, student)
            # fetch student name and matric_no from the student instance and store in session
            student_name = student.student_name
            student_matric_no = student.student_matric_no
            request.session['student_name'] = student_name
            request.session['student_matric_no'] = student_matric_no

            messages.success(request, 'Login successful.')
            logger.info('Login successful for matric_no: %s', matric_no)
            return render(request, 'users/students/students_dashboard.html',
                          {'student_name': student_name, 'student_matric_no': student_matric_no})
        # If password is incorrect
        messages.error(request, 'Invalid username or password.')
        logger.error('Invalid password for matric_no: %s', matric_no)

    return render(request, 'users/students/students_login.html')


from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render
from .models import students  # Ensure you have imported the students model
import logging

logger = logging.getLogger(__name__)


def students_password_update(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        matric_no = request.POST.get('mat_no')

        # Validate that the passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            logger.error('Passwords do not match for matric_no: %s', matric_no)
            return render(request, 'users/students/student_update_password.html')

        # Validate password length
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            logger.error('Password must be at least 8 characters for matric_no: %s', matric_no)
            return render(request, 'users/students/student_update_password.html')

        # Check for at least one digit
        elif not any(char.isdigit() for char in password):
            messages.error(request, 'Password must contain at least one digit.')
            logger.error('Password missing digit for matric_no: %s', matric_no)
            return render(request, 'users/students/student_update_password.html')

        # Check for at least one uppercase letter
        elif not any(char.isupper() for char in password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
            logger.error('Password missing uppercase letter for matric_no: %s', matric_no)
            return render(request, 'users/students/student_update_password.html')

        # Check for at least one lowercase letter
        elif not any(char.islower() for char in password):
            messages.error(request, 'Password must contain at least one lowercase letter.')
            logger.error('Password missing lowercase letter for matric_no: %s', matric_no)
            return render(request, 'users/students/student_update_password.html')

        # Check for at least one special character
        elif not any(char in ['$', '@', '#', '%', '!', '&', '*'] for char in password):
            messages.error(request, 'Password must contain at least one special character.')
            logger.error('Password missing special character for matric_no: %s', matric_no)
            return render(request, 'users/students/student_update_password.html')

        # Ensure password is not set as the default "password"
        elif password == "password":
            messages.error(request, 'Password cannot be the default password.')
            logger.error('Password is set to default "password" for matric_no: %s', matric_no)
            return render(request, 'users/students/student_update_password.html')

        # Password cannot be the same as the matric number or common variants
        elif password == matric_no or password == matric_no[::-1] or password == matric_no[1:]:
            messages.error(request, 'Password cannot be similar to your matric number.')
            logger.error('Password is too similar to matric_no: %s', matric_no)
            return render(request, 'users/students/student_update_password.html')

        else:
            # Fetch the student record using the matric number
            student = students.objects.filter(student_matric_no=matric_no).first()

            if student:
                # Hash the password before saving it
                student.student_password = make_password(password)
                student.save()
                messages.success(request, 'Password updated successfully.')
                logger.info('Password updated successfully for matric_no: %s', matric_no)
                return render(request, 'users/students/students_dashboard.html')
            else:
                messages.error(request, 'Student not found.')
                logger.error('No student found for matric_no: %s', matric_no)

    return render(request, 'users/students/student_update_password.html')


# USERS DASHBOARD
def student_dashboard(request):
    return render(request, 'users/students/students_dashboard.html')


# STUDENT LOGOUT
def student_logout(request):
    logout(request)
    return render(request, 'web/login_router.html')


# book category selector for departments book

# theme areas in the departments  as list of book categories in the form of tuples

# course codes conversion to list  for each
computer_sci_course_list = ["algorithms", "data structures", "software engineering", "computer networks",
                            "operating systems",
                            "computer architecture", "computer graphics", "artificial intelligence", "machine learning",
                            "database systems",
                            "web development", "cybersecurity", "computer vision", "natural language processing",
                            "distributed systems",
                            "cloud computing", "mobile computing", "parallel computing", "quantum computing",
                            "blockchain", "internet of things",
                            "big data", "data science", "data analytics", "data mining", "computer vision", "robotics",
                            "embedded systems",
                            "computer security", "network security", "cryptography", "computer forensics",
                            "digital forensics", "information security",
                            "computer ethics", "computer law", "computer policy", "computer science education",
                            "computer science research",
                            "computer science theory", "computer science history", "computer science philosophy",
                            "computer science ethics",
                            "computer science law", "computer science policy", "computer science education",
                            "computer science research", ]

history_courses_list = ["nigeria history", "african history", "world history", "economic history", "political history",
                        "social history",
                        "cultural history", "military history", "diplomatic history", "intellectual history",
                        "religious history"
                        "international relations", "diplomacy", "political science", "political theory",
                        "political philosophy",
                        "political economy", "political sociology", "political psychology", "political anthropology",
                        "political history",
                        "political geography", "political ecology", "political theology", "political ethics",
                        "political law", "political policy", ]

economics_courses_list = ["microeconomics", "macroeconomics", "development economics", "international economics",
                          "monetary economics",
                          "financial economics", "public economics", "health economics", "labor economics",
                          "industrial economics",
                          "agricultural economics", "environmental economics", "resource economics", "urban economics",
                          "rural economics",
                          "transport economics", "energy economics", "education economics",
                          "economic history", "economic sociology", "economic geography", "economic anthropology",
                          "economic psychology",
                          "economic philosophy", "economic ethics", "economic law", "economic policy",
                          "economic education", "economic research",
                          "economic theory", "economic methodology", "economic statistics", "economic forecasting",
                          "economic modeling", ]

accounting_courses_list = ["financial accounting", "management accounting", "cost accounting", "tax accounting",
                           "auditing",
                           "forensic accounting", "government accounting", "nonprofit accounting",
                           "international accounting",
                           "public accounting", "private accounting", "corporate accounting", "partnership accounting",
                           "sole proprietorship accounting",
                           "accounting information systems", "accounting ethics", "accounting law", "accounting policy",
                           "accounting education",
                           "accounting research", "accounting theory", "accounting history", "accounting philosophy",
                           "accounting sociology",
                           "accounting psychology", "accounting geography", "accounting anthropology",
                           "accounting theology", "accounting ecology", ]

mass_comm_courses_list = ["journalism", "broadcast journalism", "print journalism", "online journalism",
                          "photojournalism",
                          "investigative journalism", "data journalism", "sports journalism",
                          "entertainment journalism", "political journalism",
                          "business journalism", "science journalism", "health journalism", "environmental journalism",
                          "war journalism",
                          "peace journalism", "development journalism", "international journalism",
                          "diplomatic journalism", "public journalism",
                          "community journalism", "citizen journalism", "advocacy journalism", "activist journalism",
                          "social journalism", ]

electrical_engr_courses_list = ["circuit theory", "electronic devices", "analog electronics", "digital electronics",
                                "microelectronics",
                                "power electronics", "control systems", "signal processing", "communication systems",
                                "telecommunication systems",
                                "computer systems", "computer networks", "computer architecture", "computer graphics",
                                "computer vision",
                                "artificial intelligence", "machine learning", "robotics", "embedded systems",
                                "computer security", "network security",
                                "cryptography", "computer forensics", "digital forensics", "information security",
                                "computer ethics", "computer law",
                                "computer policy", "computer science education", "computer science research",
                                "computer science theory", "computer science history", ]

computer_engr_courses_list = ["circuit theory", "electronic devices", "analog electronics", "digital electronics",
                              "microelectronics",
                              "power electronics", "control systems", "signal processing", "communication systems",
                              "telecommunication systems",
                              "computer systems", "computer networks", "computer architecture", "computer graphics",
                              "computer vision",
                              "artificial intelligence", "machine learning", "robotics", "embedded systems",
                              "computer security", "network security", ]

chemistry_course_list = ["organic chemistry", "inorganic chemistry", "physical chemistry", "analytical chemistry",
                         "biochemistry",
                         "environmental chemistry", "industrial chemistry", "forensic chemistry",
                         "pharmaceutical chemistry",
                         "medicinal chemistry", "polymer chemistry", "materials chemistry", "theoretical chemistry",
                         "computational chemistry",
                         "quantum chemistry", "chemical engineering", "chemical physics", "chemical biology",
                         "chemical ecology", "chemical geology", ]

education_mgt_course_list = ["educational administration", "educational leadership", "educational management",
                             "educational policy",
                             "educational planning", "educational finance", "educational economics",
                             "educational sociology",
                             "educational psychology", "educational philosophy", "educational ethics",
                             "educational law", "educational policy", ]

political_science_course_list = ["political theory", "political philosophy", "political economy", "political sociology",
                                 "political psychology",
                                 "political anthropology", "political history", "political geography",
                                 "political ecology", "political theology",
                                 "political ethics", "political law", "political policy", "political education",
                                 "political research", "political methodology",
                                 "political statistics", "political forecasting", "political modeling",
                                 "political simulation", "political game theory",
                                 ]

medical_sciences_course_list = ["anatomy", "physiology", "biochemistry", "pharmacology", "pathology", "microbiology",
                                "parasitology",
                                "virology", "bacteriology", "mycology", "immunology", "histology", "embryology",
                                "neuroscience", "endocrinology",
                                "cardiology", "pulmonology", "gastroenterology", "nephrology", "urology", "dermatology",
                                "ophthalmology", "otolaryngology",
                                "orthopedics", "rheumatology", "oncology", "hematology", "radiology",
                                "nuclear medicine", "anesthesiology", "surgery",
                                ]

# Department to course mapping


levels_list = [100, 200, 300, 400, 500]

department_course_map = {
    "Political Science and Diplomacy": political_science_course_list,
    "Economics": economics_courses_list,
    "Industrial Chemistry": ["IC101", "IC102", "IC201"],
    "Physics with Electronics": ["PWE101", "PWE102", "PWE201"],
    "Applied Microbiology": ["AM101", "AM102", "AM201"],
    "Philosophy": ["PHI101", "PHI102", "PHI201"],
    "Computer Science": computer_sci_course_list,
    "Mass Communication": mass_comm_courses_list,
    "English and Literary Studies": ["ELS101", "ELS102", "ELS201"],
    "History and International Relations": history_courses_list,
    "Marketing and Advertising": ["MA101", "MA102", "MA201"],
    "Accounting": accounting_courses_list,
    "Theology": ["THE101", "THE102", "THE201"],
    "English Education": ["EE101", "EE102", "EE201"],
    "Economics Education": ["EDE101", "EDE102", "EDE201"],
    "Chemistry Education": ["CE101", "CE102", "CE201"],
    "Physics Education": ["PE101", "PE102", "PE201"],
    "Educational Management": education_mgt_course_list,
    "Business Administration": ["BA101", "BA102", "BA201"],
    "Entrepreneurial Studies": ["ES101", "ES102", "ES201"],
    "Peace And Conflict Studies": ["PACS101", "PACS102", "PACS201"],
    "B.Eng Computer Engineering": computer_engr_courses_list,
    "B.Eng Electrical and Electronic Engineering": electrical_engr_courses_list,
    "Law": ["LAW101", "LAW102", "LAW201"],
    "SOFTWARE ENGINEERING": ["SE101", "SE102", "SE201"],
    "Nursing": ["NUR101", "NUR102", "NUR201"],
    "Pharmacy": ["PHAR101", "PHAR102", "PHAR201"],
    "Medical Laboratory Sciences": ["MLS101", "MLS102", "MLS201"],
    "Sacred Theology": ["ST101", "ST102", "ST201"],
    "Computer science Education": ["CSE101", "CSE102", "CSE201"],
    "Medicine and Surgery": ["MS101", "MS102", "MS201"],
    "Religious Education": ["RE101", "RE102", "RE201"],
    "Public Administration": ["PA101", "PA102", "PA201"],
}


def select_course(request):
    return render(request, 'select_course.html')


@csrf_exempt
def get_courses(request, department):
    courses = department_course_map.get(department, [])
    return JsonResponse({'courses': courses})


@csrf_exempt
def process_selection(request):
    if request.method == 'POST':
        department = request.POST.get('department')
        course = request.POST.get('course')
        # Process the selected department and course
        return JsonResponse({'department': department, 'course': course})


# BOOK CATEGORY ; STUDENT SECTION
def book_category(request):
    return render(request, 'books/book_category.html')


# UPLOAD BOOKS BY ADMIN
def upload_materials(request):
    return render(request, 'books/upload_materials.html')


# library material catalogue
def video_materials_upload(request):
    return render(request, 'books/video_materials.html')


def audio_materials_upload(request):
    return render(request, 'books/audio_materials.html')


import os
import uuid
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from .models import PDF_materials  # Ensure your model is imported


def PDF_materials_upload(request):
    if request.method == 'POST':
        # Handle PDF file upload logic
        pdf_title = request.POST.get('pdf_title')
        pdf_file = request.FILES.get('pdf_file')
        pdf_cover_image = request.FILES.get('pdf_cover_image')
        pdf_author = request.POST.get('pdf_author')
        pdf_description = request.POST.get('pdf_description')
        pdf_category = request.POST.get('pdf_category')
        pdf_tags = request.POST.get('pdf_tags')
        pdf_upload_date = request.POST.get('pdf_upload_date')
        pdf_for_department = request.POST.get('pdf_department')
        pdf_for_level = request.POST.get('pdf_level')
        pdf_for_faculty = request.POST.get('pdf_faculty')

        # Generate a unique BOOK ID NUMBER
        pdf_id = uuid.uuid4().hex[:6].upper()
        book_id = f"VUNAWEB-{pdf_id}"

        # Validate the form fields
        if not all([pdf_title, pdf_file, pdf_cover_image, pdf_author, pdf_description, pdf_category, pdf_tags,
                    pdf_upload_date, pdf_for_department, pdf_for_level, pdf_for_faculty]):
            messages.error(request, 'All fields are required')
            return render(request, 'books/PDF_materials.html')

        # Determine the file extensions
        pdf_extension = os.path.splitext(pdf_file.name)[1]  # Get original file extension
        cover_extension = os.path.splitext(pdf_cover_image.name)[1]  # Get cover image extension

        # Define paths for saving files
        pdf_file_name = f"{book_id}{pdf_extension}"
        pdf_cover_name = f"{book_id}{cover_extension}"

        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'materials/pdf', pdf_file_name)
        pdf_cover_image_path = os.path.join(settings.MEDIA_ROOT, 'materials/pdf/cover', pdf_cover_name)

        # Ensure directories exist
        os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)
        os.makedirs(os.path.dirname(pdf_cover_image_path), exist_ok=True)

        # Save the PDF file to disk
        with open(pdf_file_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        # Save the PDF cover image to disk
        with open(pdf_cover_image_path, 'wb') as f:
            for chunk in pdf_cover_image.chunks():
                f.write(chunk)

        # Save the PDF details to the database
        pdf = PDF_materials.objects.create(
            pdf_material_title=pdf_title,
            pdf_material_ref_id=book_id,
            pdf_material_author=pdf_author,
            pdf_material_category=pdf_category,
            pdf_material_tags=pdf_tags,
            pdf_for_department=pdf_for_department,
            pdf_for_faculty=pdf_for_faculty,
            pdf_for_level=pdf_for_level,
            pdf_material_description=pdf_description,
            pdf_material_file=f"materials/pdf/{pdf_file_name}",  # Store relative path
            pdf_material_cover_image=f"materials/pdf/cover/{pdf_cover_name}",  # Store relative path
            pdf_upload_date=pdf_upload_date
        )

        messages.success(request, 'PDF uploaded successfully')

    return render(request, 'books/PDF_materials.html')


def journal_materials_upload(request):
    if request.method == 'POST':
        # Handle journal file upload logic
        journal_title = request.POST.get('journal_title')
        journal_file = request.FILES.get('journal_file')
        journal_cover_image = request.FILES.get('journal_cover_image')
        journal_author = request.POST.get('journal_author')
        staff_ID = request.POST.get('staff_id')
        journal_abstract = request.POST.get('journal_description')
        journal_type = request.POST.get('journal_type')
        journal_tags = request.POST.get('journal_tags')
        journal_thematic_area1 = request.POST.get('journal_thematic_area1')
        journal_thematic_area2 = request.POST.get('journal_thematic_area2')
        journal_thematic_area3 = request.POST.get('journal_thematic_area3')
        journal_pub_date = request.POST.get('journal_pub_date')
        journal_for_department = request.POST.get('journal_department')
        journal_for_level = request.POST.get('journal_level')
        journal_for_faculty = request.POST.get('journal_faculty')

        # Validate the form fields
        if not all([journal_title, journal_file, journal_cover_image, journal_author, journal_abstract,
                    journal_type, journal_tags, journal_pub_date, journal_for_department, journal_for_level,
                    journal_thematic_area1, journal_thematic_area2, journal_thematic_area3,
                    journal_for_faculty]):
            messages.error(request, 'All fields are required')
            return render(request, 'books/journal_materials.html')

            # Determine the file extensions
        journal_extension = os.path.splitext(journal_file.name)[1]  # Get original file extension
        journal_cover_extension = os.path.splitext(journal_cover_image.name)[1]  # Get cover image extension

        # Give the journal file a unique BOOK ID NUMBER
        journal_id = uuid.uuid4().hex[:6].upper()

        # BOOK ID IN THIS FORMAT VUA-ELIBRARY-DEPARTMENT-LEVEL-BOOK-ID
        journal_ref_id = f"VUNAWEB-J-{journal_id}"

        # Define paths for saving files
        journal_file_name = f"{journal_ref_id}{journal_extension}"
        journal_cover_name = f"{journal_ref_id}{journal_cover_extension}"

        # Save the journal details to the database
        journal = Journal_materials.objects.create(
            journal_material_title=journal_title,
            journal_material_ref_id=journal_ref_id,
            journal_material_author=journal_author,
            staff_ID=staff_ID,
            journal_material_type=journal_type,
            journal_material_tags=journal_tags,
            journal_for_department=journal_for_department,
            journal_for_faculty=journal_for_faculty,
            journal_thematic_area1=journal_thematic_area1,
            journal_thematic_area2=journal_thematic_area2,
            journal_thematic_area3=journal_thematic_area3,
            journal_for_level=journal_for_level,
            journal_material_abstract=journal_abstract,
            journal_material_file=f"materials/journals/{journal_file_name}",
            journal_material_cover_image=f"materials/journals/cover/{journal_cover_name}",
            journal_pub_date=journal_pub_date
        )

        if journal:
            journal_file_path = os.path.join(settings.MEDIA_ROOT, 'materials/journal', journal_file_name)
            journal_cover_image_path = os.path.join(settings.MEDIA_ROOT, 'materials/journal/cover', journal_cover_name)
            # Save the journal file to the media folder

            # Ensure the directory exists
            os.makedirs(os.path.dirname(journal_file_path), exist_ok=True)

            with open(journal_file_path, 'wb') as f:
                for chunk in journal_file.chunks():
                    f.write(chunk)

            # Save the journal cover image to the media folder
            journal_cover_image_file_path = os.path.join(settings.MEDIA_ROOT, 'materials/journals/cover',
                                                         journal_cover_image_path)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(journal_cover_image_file_path), exist_ok=True)

            with open(journal_cover_image_file_path, 'wb') as f:
                for chunk in journal_cover_image.chunks():
                    f.write(chunk)
                    messages.success(request, 'Journal uploaded successfully')

        else:
            messages.error(request, 'Journal upload failed')

    return render(request, 'books/research_upload.html')


# GOOGLE DRIVE CATALOGUING
def computer_sci_book_category(request):
    return render(request, 'books/computer_sci_book_category.html')


import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Load the service account JSON from the environment variable or file
SERVICE_ACCOUNT_JSON = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')

if not SERVICE_ACCOUNT_JSON:
    # If the environment variable is not set, load from a file
    SERVICE_ACCOUNT_FILE = 'knowrizon/media/config/service_account_api.json'
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise ValueError("The service account JSON file does not exist.")
    with open(SERVICE_ACCOUNT_FILE, 'r') as f:
        SERVICE_ACCOUNT_INFO = json.load(f)
else:
    try:
        # Parse the JSON string to a dictionary
        SERVICE_ACCOUNT_INFO = json.loads(SERVICE_ACCOUNT_JSON)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in GOOGLE_SERVICE_ACCOUNT_JSON: {e}")

# Create credentials using the loaded JSON
credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)

# Build the Drive API service
drive_service = build('drive', 'v3', credentials=credentials)


# knowrizon/knowrizonApp/views.py

def view_books(request, category):
    # Logic to fetch books based on the category
    context = {
        'category': category,
        'books': []  # Replace with actual book fetching logic
    }
    return render(request, 'books/comp_sci_books.html', context)


# COMPUTER SCIENCE BOOKS CATEGORIES FUNCTION FROM drive-folders_API.py
# COMPUTER SCIENCE CATEGORY MAPPING TO DRIVE FOLDERS; BOOKS CATEGORIES: folder ids
COMPUTER_SCI_DEPT_CATEGORY_TO_FOLDER = {
    "algorithms": "1V7NViMHyErE0DHnVkupfMYkEAGzmIZND",
    "artificial_intelligence": "folder_id_ai",
    "computer_networks": "folder_id_networks",
    "computer_programming": "folder_id_programming",
    "computer_security": "folder_id_security",
    "data_science": "folder_id_data_science",
    "database_management": "folder_id_database",
    "distributed_systems": "folder_id_distributed_systems",
    "machine_learning": "folder_id_machine_learning",
    "operating_systems": "folder_id_os",
    "software_engineering": "folder_id_software_engineering",
    "web_development": "folder_id_web_dev",
    "quantum_computing": "folder_id_quantum_computing",
    "cloud_computing": "folder_id_cloud_computing",
    "blockchain": "folder_id_blockchain",
    "big_data": "folder_id_big_data",
    "iot": "folder_id_iot",
    "cyber_security": "folder_id_cyber_security",
    "mobile_application": "folder_id_mobile_app",
    "robotics": "folder_id_robotics",
    "data_structures": "folder_id_data_structures",
    "computer_graphics": "folder_id_graphics",
    "optimization": "folder_id_optimization",
    "computational_mathematics": "folder_id_computational_mathematics",
    "computer_vision": "folder_id_computer_vision",
}


# LICENSED COPYRIGHT MATERIAL CATEGORIES
def view_comp_sci_books(request, category):
    # Get the folder ID for the category
    folder_id = COMPUTER_SCI_DEPT_CATEGORY_TO_FOLDER.get(category)

    # Debugging: Print category and folder ID
    print("Requested Category:", category)
    print("Mapped Folder ID:", folder_id)

    # Check if folder ID exists
    if not folder_id:
        return render(request, 'error.html', {"message": "Category not found"})

    # Fetch files from the folder
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/pdf'",
        fields="files(id, name, webViewLink, thumbnailLink)"
    ).execute()

    # Get the list of books
    books = results.get('files', [])

    # Debugging: Print the fetched books
    print("Fetched Books:", books)

    # Render the template
    return render(request, 'books/comp_sci_books.html', {"books": books, "category": category})


# copyright protected materials
def view_protected_materials(request):
    return render(request, 'books/protected_materials.html')


# copyright protected computer science materials
def view_protected_comp_sci_materials(request):
    return render(request, 'books/protected_comp_sci_materials.html')


import os
import requests
from django.conf import settings
from .models import PDF_materials

import os
from django.conf import settings
from django.shortcuts import render
from .models import PDF_materials  # Ensure your model is imported

import os
from django.conf import settings
from django.shortcuts import render
from .models import PDF_materials  # Ensure the model is imported

import os
from django.conf import settings
from django.shortcuts import render
from .models import PDF_materials  # Ensure the model is imported


def view_protected_comp_sci_books(request, category):
    """Fetch books from local storage based on category."""
    books_path = os.path.join(settings.MEDIA_ROOT, 'materials/pdf')

    if not os.path.exists(books_path):
        return render(request, 'error.html', {"message": "Category not found"})

    books = []

    # Fetch PDF records from the database
    pdfs = PDF_materials.objects.filter(pdf_material_category=category).values(
        'pdf_material_title', 'pdf_material_file', 'pdf_material_cover_image',
        'pdf_material_author', 'pdf_upload_date', 'pdf_material_tags',
        'pdf_material_description', 'pdf_material_ref_id',
    )

    for pdf in pdfs:
        ref_id = pdf.get('pdf_material_ref_id')

        if not ref_id:  # Skip books with empty book_id
            continue

        book_name = pdf.get('pdf_material_title', 'Unknown Title')
        author = pdf.get('pdf_material_author', 'Unknown')
        upload_date = pdf.get('pdf_upload_date', 'Unknown')
        tags = pdf.get('pdf_material_tags', '')
        description = pdf.get('pdf_material_description', '')

        # Construct the correct book file URL
        book_path = f"{settings.MEDIA_URL}materials/pdf/{ref_id}.pdf" if pdf.get('pdf_material_file') else ""

        # Determine valid cover image extension
        valid_extensions = ['.jpg', '.png', '.jpeg']
        cover_full_path = "/static/images/default-cover.png"  # Default cover

        for ext in valid_extensions:
            cover_candidate = os.path.join(settings.MEDIA_ROOT, "materials/pdf/cover", f"{ref_id}{ext}")
            if os.path.exists(cover_candidate):
                cover_full_path = f"{settings.MEDIA_URL}materials/pdf/cover/{ref_id}{ext}"
                break

        # Append book details
        books.append({
            "book_id": ref_id,  # Ensure book_id is always set
            "name": book_name,
            "file_url": book_path,
            "cover_url": cover_full_path,
            "author": author,
            "year": upload_date,
            "tags": tags,
            "description": description,
        })

    return render(request, 'books/comp_sci_books.html', {"books": books, "category": category})


import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from datetime import datetime

import os
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import PDF_materials  # Ensure correct import

from urllib.parse import unquote


def view_protected_book_details(request, category, book_id):
    # Fetch the book from the database using book_id and category
    book_id = unquote(book_id)  # Decode URL (e.g., convert "%20" to " ")
    book = get_object_or_404(PDF_materials, pdf_material_ref_id=book_id, pdf_material_category=category)

    # Construct the correct book file URL
    book_path = f"{settings.MEDIA_URL}materials/pdf/{book_id}.pdf" if book.pdf_material_file else ""

    valid_extensions = ['.jpg', '.png', '.jpeg']
    cover_full_path = None

    for ext in valid_extensions:
        cover_candidate = os.path.join(settings.MEDIA_ROOT, "materials/pdf/cover", f"{book_id}{ext}")
        if os.path.exists(cover_candidate):
            cover_full_path = f"{settings.MEDIA_URL}materials/pdf/cover/{book_id}{ext}"
            break

    if cover_full_path is None:
        cover_full_path = "/static/images/default-cover.png"  # Default cover image

    # Ensure `pdf_upload_date` is a valid datetime object
    if isinstance(book.pdf_upload_date, str):
        try:
            book.pdf_upload_date = datetime.strptime(book.pdf_upload_date, "%Y-%m-%d")
        except ValueError:
            book.pdf_upload_date = None

        # Ensure `pdf_upload_date` is a valid datetime object
        if isinstance(book.pdf_upload_date, str):
            try:
                book.pdf_upload_date = datetime.strptime(book.pdf_upload_date, "%Y-%m-%d")
            except ValueError:
                book.pdf_upload_date = None

        upload_date = book.pdf_upload_date.strftime("%B %d, %Y") if book.pdf_upload_date else "Unknown"

    # Pass book details to the template

    return render(request, 'books/protected_material_details.html', {
        "book": {
            "name": book.pdf_material_title,
            "file_url": book_path,
            "cover_url": cover_full_path,
            "author": book.pdf_material_author or "Unknown",
            "year": upload_date,
            "tags": book.pdf_material_tags or "No tags available",
            "description": book.pdf_material_description or "No description available",
            "book_id": book.pdf_material_ref_id
        }
    })


# STAFF SECTION OF THE LIBRARY MANAGEMENT SYSTEM
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.hashers import check_password
import logging
from .models import academic_staff  # Import your staff model

logger = logging.getLogger(__name__)


def staff_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            logger.warning('Login attempt with missing credentials.')
            return render(request, 'users/staff/staff_login.html')

        # Fetch staff by email
        staff = academic_staff.objects.filter(academic_staff_email=email).first()

        if not staff:
            messages.error(request, 'Account not found. Please register with the admin.')
            logger.error('No staff found for email: %s', email)
            return render(request, 'users/staff/staff_login.html')

        # Force password update if using default password
        if password == "password":
            messages.warning(request, 'Please update your password.')
            logger.info('Prompting staff to update password for email: %s', email)
            return redirect('staff_update_password')  # Redirect to password update page

        # Validate password
        if check_password(password, staff.academic_staff_password):
            # Simulate Django authentication (academic_staff isn't a User model)
            request.session['staff_id'] = staff.academic_staff_id
            request.session['staff_name'] = f"{staff.academic_staff_fname} {staff.academic_staff_lname}"
            request.session['staff_email'] = staff.academic_staff_email

            messages.success(request, 'Login successful.')
            logger.info('Login successful for email: %s', email)
            return redirect('staff_dashboard')  # Redirect to the dashboard

        # Invalid credentials
        messages.error(request, 'Invalid email or password.')
        logger.error('Invalid password for email: %s', email)

    return render(request, 'users/staff/staff_login.html')


from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import academic_staff
import logging

logger = logging.getLogger(__name__)


def staff_update_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        email = request.POST.get('email')

        # Validate that the passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'users/staff/staff_update_password.html')

        # Validate password length
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'users/staff/staff_update_password.html')

        # Check for at least one digit
        elif not any(char.isdigit() for char in password):
            messages.error(request, 'Password must contain at least one digit.')
            return render(request, 'users/staff/staff_update_password.html')

        # Check for at least one uppercase letter
        elif not any(char.isupper() for char in password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
            return render(request, 'users/staff/staff_update_password.html')

        # Check for at least one lowercase letter
        elif not any(char.islower() for char in password):
            messages.error(request, 'Password must contain at least one lowercase letter.')
            return render(request, 'users/staff/staff_update_password.html')

        # Check for at least one special character
        elif not any(char in ['$', '@', '#', '%', '!', '&', '*'] for char in password):
            messages.error(request, 'Password must contain at least one special character.')
            return render(request, 'users/staff/staff_update_password.html')

        # Ensure password is not set as the default "password"
        elif password == "password":
            messages.error(request, 'Password cannot be "password".')
            return render(request, 'users/staff/staff_update_password.html')

        # Fetch the staff using email
        staff = academic_staff.objects.filter(academic_staff_email=email).first()
        if not staff:
            messages.error(request, 'Account not found.')
            return render(request, 'users/staff/staff_update_password.html')

        # Update the staff's password
        staff.academic_staff_password = make_password(password)
        staff.save()

        messages.success(request, 'Password updated successfully. Please log in with your new password.')
        logger.info('Password updated successfully for email: %s', email)
        return redirect('staff_login')

    return render(request, 'users/staff/staff_update_password.html')


def staff_dashboard(request):
    return render(request, 'users/staff/staff_dashboard.html')


# researcher section of the library management system
def researcher_login(request):
    return render(request, 'users/researcher/researcher_login.html')


def researcher_dashboard(request):
    return render(request, 'users/researcher/researcher_dashboard.html')


# guest section of the library management system
def guest_login(request):
    return render(request, 'users/guest/guest_login.html')


def guest_dashboard(request):
    return render(request, 'users/guest/guest_dashboard.html')


# TOP VERITAS STAFF ACADEMIC RESEARCHERS COLLABORATION SECTION
def top_researchers(request):
    # ALL ACADEMIC STAFF RECORDS FOR A TABLE
    all_academic_staff = academic_staff.objects.all()

    return render(request, 'researchers/top_researchers.html', {'all_academic_staff': all_academic_staff})


# JOURNAL MATERIALS CATALOGUE
#JOURNAL MATERIALS UPLOAD
def research_materials_upload(request):
    return render(request, 'books/research_upload.html')


# RESEARRCH REPOSITORY CATALOGUE
def research_repository(request):
    return render(request, 'books/research_repository.html')


# research materials view
def view_research_materials(request):
    # Fetch all research materials from the database and render them to the template
    research_materials = Journal_materials.objects.all()
    return render(request, 'books/research_material_view.html', {'research_materials': research_materials})


