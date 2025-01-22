# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.db import models
from django.contrib.auth.hashers import make_password


class AdminManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Admin(AbstractBaseUser):
    admin_id = models.AutoField(primary_key=True)
    admin_fname = models.CharField(max_length=50)
    admin_lname = models.CharField(max_length=50)
    admin_email = models.EmailField(max_length=254, unique=True)
    admin_password = models.CharField(max_length=128, default='default_password')  # Provide a one-off default
    admin_dept = models.CharField(max_length=50)
    admin_created_at = models.DateTimeField(default=timezone.now)
    admin_updated_at = models.DateTimeField(default=timezone.now)

    objects = AdminManager()

    USERNAME_FIELD = 'admin_email'
    REQUIRED_FIELDS = ['admin_fname', 'admin_lname', 'admin_dept']

    def __str__(self):
        return self.admin_fname


# Create your models here.

# student models


class students(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_matric_no = models.CharField(max_length=50)
    student_name = models.CharField(max_length=50)
    student_email = models.EmailField(max_length=50, default='Not specified')
    student_password = models.CharField(max_length=200)
    student_gender = models.CharField(max_length=50)
    student_dept = models.CharField(max_length=50)
    student_created_at = models.DateTimeField(auto_now_add=True)
    student_updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash the password if the student is being created
            self.student_password = make_password(self.student_password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.student_fname


# content managers models
class content_managers(models.Model):
    content_manager_id = models.AutoField(primary_key=True)
    content_manager_fname = models.CharField(max_length=50)
    content_manager_lname = models.CharField(max_length=50)
    content_manager_email = models.EmailField(max_length=50)
    contet_manager_phone = models.CharField(max_length=50)
    content_manager_prefix = models.CharField(max_length=50)
    content_manager_password = models.CharField(max_length=50)
    content_manager_dept = models.CharField(max_length=50)
    content_manager_created_at = models.DateTimeField(auto_now_add=True)
    content_manager_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content_manager_fname


# academic staff models

class academic_staff(models.Model):
    academic_staff_id = models.AutoField(primary_key=True)
    academic_staff_fname = models.CharField(max_length=50)
    academic_staff_lname = models.CharField(max_length=50)
    academic_staff_gender = models.CharField(max_length=50, default='Not specified')  # Add default value
    academic_staff_email = models.EmailField(max_length=50)
    academic_staff_password = models.CharField(max_length=50)
    academic_staff_upload_approval = models.IntegerField(default=0)
    academic_staff_dept = models.CharField(max_length=50)
    academic_staff_position = models.CharField(max_length=50)
    academic_staff_phone = models.CharField(max_length=15, default='')
    academic_staff_prefix = models.CharField(max_length=10, default='')
    academic_staff_identity = models.CharField(max_length=50, default='')
    academic_staff_interest = models.CharField(max_length=50, default='interest')
    academic_staff_created_at = models.DateTimeField(auto_now_add=True)
    academic_staff_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.academic_staff_fname


class researchers(models.Model):
    researcher_id = models.AutoField(primary_key=True)
    researcher_fname = models.CharField(max_length=50)
    researcher_lname = models.CharField(max_length=50)
    researcher_prefix = models.CharField(max_length=50)
    researcher_email = models.EmailField(max_length=50)
    researcher_password = models.CharField(max_length=50)
    researcher_dept = models.CharField(max_length=50)
    researcher_phone = models.CharField(max_length=50)
    researcher_interest = models.CharField(max_length=50)
    researcher_created_at = models.DateTimeField(auto_now_add=True)
    researcher_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.researcher_fname


# library materials models
class library_materials(models.Model):
    library_material_id = models.AutoField(primary_key=True)
    library_material_title = models.CharField(max_length=50)
    library_material_author = models.CharField(max_length=50)
    library_material_publisher = models.CharField(max_length=50)
    library_material_year = models.CharField(max_length=50)
    library_material_type = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    genre = models.CharField(max_length=50)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)
    format = models.CharField(max_length=50)
    file = models.FileField(upload_to='materials/', blank=True, null=True)  # For digital files
    cover_image = models.ImageField(upload_to='materials/cover/', blank=True, null=True)  # Optional cover image
    availability_status = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=50)
    library_material_created_at = models.DateTimeField(auto_now_add=True)
    library_material_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.library_material_title


# library PDF materials models
class PDF_materials(models.Model):
    pdf_material_id = models.AutoField(primary_key=True)
    pdf_material_ref_id = models.CharField(max_length=50)
    pdf_material_title = models.CharField(max_length=50)
    pdf_material_author = models.CharField(max_length=50)
    pdf_material_category = models.CharField(max_length=50)
    pdf_upload_date = models.CharField(max_length=50)
    pdf_material_tags = models.CharField(max_length=50)
    pdf_for_department = models.CharField(max_length=50)
    pdf_for_faculty = models.CharField(max_length=50)
    pdf_for_level = models.CharField(max_length=50)
    pdf_material_description = models.CharField(max_length=255)
    pdf_material_file = models.FileField(upload_to='materials/pdf/', blank=True, null=True)  # For digital files
    pdf_material_cover_image = models.ImageField(upload_to='materials/pdf/cover/', blank=True, null=True)  # Optional cover image
    pdf_material_created_at = models.DateTimeField(auto_now_add=True)
    pdf_material_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pdf_material_title


class Journal_materials(models.Model):
    journal_material_id = models.AutoField(primary_key=True)
    journal_material_title = models.CharField(max_length=50)
    journal_material_author = models.CharField(max_length=50)
    journal_material_category = models.CharField(max_length=50)
    journal_upload_date = models.CharField(max_length=50)
    journal_material_tags = models.CharField(max_length=50)
    journal_for_department = models.CharField(max_length=50)
    journal_for_faculty = models.CharField(max_length=50)
    journal_for_level = models.CharField(max_length=50)
    journal_material_description = models.CharField(max_length=255)
    journal_material_file = models.FileField(upload_to='materials/journals/', blank=True, null=True)  # For digital files
    journal_material_cover_image = models.ImageField(upload_to='materials/journals/cover/', blank=True, null=True)  # Optional cover image
    journal_material_created_at = models.DateTimeField(auto_now_add=True)
    journal_material_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.journal_material_title