
from django import forms

from .models import academic_staff


class BulkStudentUploadForm(forms.Form):
    file = forms.FileField(
        label="Select an Excel file",
        widget=forms.ClearableFileInput(attrs={'accept': '.xlsx,.xls'}),
        help_text="Please upload a .xlsx or .xls file containing student data."
    )

    def clean_file(self):
        file = self.cleaned_data.get('file')

        # Check if the file is an Excel file based on its extension
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext not in ['xlsx', 'xls']:
                raise forms.ValidationError("Invalid file type. Only .xlsx and .xls files are allowed.")

        return file


# staff upload
class BulkStaffUploadForm(forms.Form):
    file = forms.FileField(
        label="Select an Excel file",
        widget=forms.ClearableFileInput(attrs={'accept': '.xlsx,.xls'}),
        help_text="Please upload a .xlsx or .xls file containing staff data."
    )

    def clean_file(self):
        file = self.cleaned_data.get('file')

        # Check if the file is an Excel file based on its extension
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext not in ['xlsx', 'xls']:
                raise forms.ValidationError("Invalid file type. Only .xlsx and .xls files are allowed.")

        return file


# admin manages staff records form
# forms.py

class AcademicStaffForm(forms.ModelForm):
    class Meta:
        model = academic_staff
        fields = [
            'academic_staff_fname',
            'academic_staff_lname',
            'academic_staff_gender',
            'academic_staff_email',
            'academic_staff_password',
            'academic_staff_upload_approval',
            'academic_staff_dept',
            'academic_staff_position',
            'academic_staff_phone',
            'academic_staff_prefix',
            'academic_staff_identity',
            'academic_staff_interest',
        ]