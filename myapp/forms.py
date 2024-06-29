from django import forms
from .models import Student

class StudentRegistration(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    class Meta:
        model = Student
        fields = ['name', 'rollno', 'phoneno','address','gender','photo']
