from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField


class Profile(models.Model):
    """User profile Model
    :Inherit: - models.Model
    bio - use HTMLField from tinymce.models
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(help_text='(MM/DD/YYYY)')
    email = models.EmailField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    post_code = models.IntegerField()
    bio = HTMLField('Content')
    avatar = models.ImageField(upload_to='./user_profile_avatar')
    hobbies = models.CharField(max_length=255, blank=True)
    favorite_animals = models.CharField(max_length=255, blank=True)
    user = models.OneToOneField(User, related_name='profile')

