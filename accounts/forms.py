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
             - Profile model fields
    """
    check_email = forms.EmailField(max_length=255)
    bio = forms.CharField(widget=TinyMCE(attrs={"cols": 20, "rows": 10}))

    class Meta:
        user = models.Profile
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
        pass
