from django import forms
from django.contrib.auth.models import User
from .models import Customer
import re

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError("First name should only contain alphabetic characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should only contain alphabetic characters.")
        return last_name

    def clean_username(self):
        username = self.cleaned_data['username']
        # You can add custom username validation logic here.
        # For example, check if the username already exists in the database.
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        # You can add custom password validation logic here.
        # For example, ensure the password meets certain complexity requirements.
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address', 'mobile', 'profile_pic']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']

        # Use a regular expression to validate the mobile number.
        # In this example, we assume that a valid mobile number contains 10 digits.
        if not re.match(r'^\d{10}$', mobile):
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")

        return mobile

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data['profile_pic']

        allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif')
        if not profile_pic.name.lower().endswith(allowed_extensions):
            raise forms.ValidationError("Only JPG, JPEG, PNG, or GIF images are allowed.")

        return profile_pic
