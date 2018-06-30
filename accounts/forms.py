from django import forms
import re
from django.core.validators import EmailValidator
from tinymce.widgets import TinyMCE

from . import models


specials = ".\!@#$%^&*?_~-( )"


class ProfileForm(forms.ModelForm):
    """Profile Form
    :Inherit: - forms.ModelForm
    :fields: - check_email --> EmailField form
             - bio --> CharField form with TinyMCE widget
    """
    check_email = forms.EmailField()
    bio = forms.CharField(widget=TinyMCE(attrs={"cols": 30, "rows": 10}))

    class Meta:
        model = models.Profile
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'date_of_birth',
            'email',
            'check_email',
            'city',
            'state',
            'country',
            'zip',
            'hobbies',
            'favorite_animals',
            'bio'
        ]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify_email = cleaned_data.get('check_email')
        bio = cleaned_data.get('bio')
        if email != verify_email:
            raise forms.ValidationError('Enter the same email address in both fields!')
        if len(bio) < 10:
            raise forms.ValidationError('Biography must contain at least 10 letters!')
        return cleaned_data




