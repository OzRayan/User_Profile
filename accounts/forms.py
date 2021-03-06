from django import forms
import re
from django.core.validators import EmailValidator
from tinymce.widgets import TinyMCE

from . import models


class ProfileForm(forms.ModelForm):
    """Profile Form
    :Inherit: - forms.ModelForm
    :fields: - check_email --> EmailField form
             - bio --> CharField form with TinyMCE widget
    """
    check_email = forms.EmailField(max_length=100)
    bio = forms.CharField(widget=TinyMCE(attrs={"cols": 30, "rows": 10}))

    class Meta:
        model = models.Profile
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'email',
            'check_email',
            'city',
            'state',
            'country',
            'avatar',
            'post_code',
            'hobbies',
            'favorite_animals',
            'bio'
        ]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        EmailValidator()(email)
        verify_email = cleaned_data.get('check_email')

        # HTML <p> tag removed from string
        # replace can be altered based on how it's called in the html form
        bio = cleaned_data.get('bio').replace('<p>', '').replace('</p>', '')

        if email != verify_email:
            raise forms.ValidationError('Enter the same email address in both fields!')
        if len(bio) < 10:
            raise forms.ValidationError('Biography must contain at least 10 letters!')

        return cleaned_data


class PasswordForm(forms.Form):
    """Password Form
    :Inherit: - forms.Form
    :fields: - old - password --> CharField widget PasswordInput
             - new - password --> CharField widget PasswordInput
             - check_new - password --> CharField widget PasswordInput
    """
    old = forms.CharField(widget=forms.PasswordInput())
    new = forms.CharField(widget=forms.PasswordInput())
    check_new = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, request=None, *args, **kwargs):
        """Prepares user data for password validation"""
        self.request = request
        super().__init__(*args, **kwargs)

    @staticmethod
    def error(error_message):
        """Validation error for failing checks"""
        raise forms.ValidationError(error_message)

    def clean(self):
        """Password validation"""
        cleaned_data = super().clean()
        old_pass = cleaned_data.get('old', '')
        new_pass = cleaned_data.get('new', '')
        check_pass = cleaned_data.get('check_new', '')
        profile = self.request.user.profile

        if not old_pass:
            self.error('First give the old password!')
        if not new_pass:
            self.error('Before confirming the new password, add one first!')
        if not check_pass:
            self.error('Confirm the new password')

        if len(new_pass) < 14:
            self.error('Minim length 14 characters!')
        if old_pass == new_pass:
            self.error('New password can\'t match with the old password!')
        if new_pass != check_pass:
            print(check_pass)
            self.error('Passwords doesn\'t match!')

        # Checks if user profile name are present in password
        if profile.first_name.lower() in new_pass.lower() or \
                profile.last_name.lower() in new_pass.lower():
            self.error('Password can\'t contain your first or last name!')

        # Regex use to check alphabet, numeric, upper, lower and special chars in password.
        if not re.findall('[A-Z]', new_pass):
            self.error('Password must contain at least one upper letter!')
        if not re.findall('[a-z]', new_pass):
            self.error('Password must contain at least one lower letter!')
        if not re.findall('\d', new_pass):
            self.error('Password must contain at least one number!')
        if not re.findall('\W[^_]', new_pass):
            self.error('Password must contain at least one special character (ex: .\!@#$%^&*?_~-)')

        return cleaned_data
