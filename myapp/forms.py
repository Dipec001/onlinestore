from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Drug
from django.core.exceptions import ValidationError
from .choices import CATEGORIES

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Divine@example.com'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    phone_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09087875373'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Divine'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))

    class Meta:
        model = User
        fields = ['email', 'date_of_birth', 'phone_number', 'first_name', 'last_name', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken.")
        return email
    
    #To customize the UserCreationForm so that it uses a single password field instead of password1 and password2,
    # you will need to override the default behavior.
    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Add any custom password validation here
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Divine@example.com'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))


class DrugForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORIES, required=True)
    class Meta:
        model = Drug
        fields = ['name', 'description', 'price', 'manufacturer', 'category', 'image']

