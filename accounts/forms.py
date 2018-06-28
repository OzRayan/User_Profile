from django import forms
import re
from django.core.validators import EmailValidator
from tinymce.widgets import TinyMCE


from . import models


specials = ".\!@#$%^&*?_~-( )"
