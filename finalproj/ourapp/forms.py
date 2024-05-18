from django import forms
from .models import Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'first_name', 
            'last_name', 
            'sex', 
            'age', 
            'phone_no',
            'roll_no',
            'email',
            'image',
        )
        image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']








