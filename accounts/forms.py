from django import forms
import re
from tinymce.widgets import TinyMCE
from django.core.validators import EmailValidator


from . import models
from .password import prompt

specials = ".\!@#$%^&*?_~-( )"


class UserProfileForm(forms.ModelForm):
    """UserProfileForm
    :Inherit: forms.ModelForm
    :values: - check_email --> EmailField()
             - bio --> CharField() with TinyMCE widget
    Meta: - model --> UserProfile Model
          - fields --> UserProfile fields + check_email
    """
    check_email = forms.EmailField(max_length=100)
    bio = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 10}))

    class Meta:
        model = models.UserProfile
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'date_of_birth',
            'city',
            'state',
            'country',
            'email',
            'check_email',
            'hobbies',
            'favorite_animals',
            'bio',
        ]

    def clean(self):
        """clean function --> cleaned_data
        - makes sure that email and check_email match,
        bio is larger than 10 characters

        cleaned_data - UserProfileForm instance

        :return: - cleaned_data
        """
        cleaned_data = super().clean()
        EmailValidator()(cleaned_data.get('check_email'))

        if not cleaned_data.get('avatar') or \
                not cleaned_data.get('first_name') or \
                not cleaned_data.get('last_name') or \
                not cleaned_data.get('date_of_birth') or \
                not cleaned_data.get('city') or \
                not cleaned_data.get('state') or \
                not cleaned_data.get('country') or \
                not cleaned_data.get('email'):
            raise forms.ValidationError("")
        if cleaned_data['email'] != cleaned_data['check_email']:
            raise forms.ValidationError("Email addresses don't match")
        if cleaned_data['check_email'] is None:
            raise forms.ValidationError("Please confirm your email")
        bio = cleaned_data.get('bio', '')
        bio = re.sub('<[^<]+?>', '', bio)
        if len(bio) < 10:
            raise forms.ValidationError(
                "Bio must be longer than 10 characters")
        return cleaned_data


class ChangePasswordForm(forms.Form):
    """ChangePasswordForm
    :Inherit: - forms.Form
    :values: - old_password --> CharField() with PasswordInput widget
             - new_password --> CharField() with PasswordInput widget and help_text,
                                help_text is populated with password.prompt
             - new_password2 --> CharField() with PasswordInput widget and label
    """
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(help_text=prompt,
                                   widget=forms.PasswordInput())
    new_password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        """Constructor"""
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        """clean function
        - makes sure that emails are matching and fulfill the requirements
        :return - cleaned_data
        """
        cleaned_data = super().clean()
        if not cleaned_data.get('old_password') and \
                (not cleaned_data.get('new_password')) and \
                (not cleaned_data.get('new_password2')):
            raise forms.ValidationError('You must start from somewhere!')
        if not cleaned_data.get('old_password'):
            raise forms.ValidationError('You should enter the old password before changing!')
        if not cleaned_data.get('new_password') or \
                (not cleaned_data.get('new_password') and not cleaned_data.get('new_password2')):
            raise forms.ValidationError('You must provide a password first!')
        if not cleaned_data['new_password2']:
            raise forms.ValidationError('You must confirm the password!')
        password = cleaned_data['new_password']
        if cleaned_data['old_password'] == password:
            raise forms.ValidationError(
                "New password cannot match old password")
        if password != cleaned_data['new_password2']:
            raise forms.ValidationError(
                "New passwords don't match")
        if len(password) < 14:
            raise forms.ValidationError(
                "Password must be at least 14 characters")
        if not any(letter.isupper() for letter in password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter")
        if not any(letter.islower() for letter in password):
            raise forms.ValidationError(
                "Password must contain at least one lowercase letter")
        if not any(letter.isdigit() for letter in password):
            raise forms.ValidationError(
                "Password must contain at least one digit (0-9)")
        if not any(letter in specials for letter in password):
            raise forms.ValidationError(
                "Password must contain at least one special character [.\!@#$%^&*?_~-( ) ]")
        try:
            profile = self.request.user.profile
        except models.UserProfile.DoesNotExist:
            pass
        else:
            if (profile.first_name.lower() in password.lower() or
                    profile.last_name.lower() in password.lower()):
                raise forms.ValidationError(
                    "Password cannot contain your first or last name")

        return cleaned_data

