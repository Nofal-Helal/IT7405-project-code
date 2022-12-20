from django import forms
from django.contrib.auth import forms as authforms
from django.contrib.auth.models import User
import re


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


class AddMovieFromIMDBForm(forms.Form):
    ids = forms.CharField(
        label='List of IMDb ids, separated by lines',
        widget=forms.Textarea(
            attrs={
                'oninput': 'auto_grow(this)',
                'style':
                'resize:none;overflow:hidden;min-height:3.5rem;height:0;'
            }))

    # Add attributes for bootstrap
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = ''

    def validate_imdb_ids(value: str):
        good = []
        bad = []
        for v in map(str.strip, filter(None, value.splitlines())):
            if re.match(r'tt[0-9]{7,}', v):
                good.append(v)
            else:
                bad.append(v)
        return good, bad

    def clean_ids(self):
        ids = self.cleaned_data['ids']
        good, bad = AddMovieFromIMDBForm.validate_imdb_ids(ids)
        if bad:
            self.fields['ids'].widget.attrs['class'] = (
                'form-control is-invalid')
            raise forms.ValidationError(
                'This should be a list of IMDb ids (e.g. tt1234567). These values are not valid: %(vals)s.',
                params={'vals': ', '.join(bad)})
        return good
