from django import forms
from django.contrib.auth import forms as authforms
from django.contrib.auth.models import User


# Extend the default AuthenticationForm from auth
class AuthenticationForm(authforms.AuthenticationForm):
    # Add attributes for bootstrap
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = ''


# Extend the default UserCreationForm from auth to include an email field
class UserCreationForm(authforms.UserCreationForm):
    email = forms.EmailField(max_length=254)
    field_order = ['username', 'email', 'password1', 'password2']

    # add .is-invalid class to invalid fields
    def updateClasses(self):
        for visible in self.visible_fields():
            if visible.errors:
                visible.field.widget.attrs['class'] = 'form-control is-invalid'

    # Add attributes for bootstrap
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = ''

    # override the save method to also save email
    def save(self, commit=True):
        user: User = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
