from django.contrib.auth.models import User
from django.db import models
from tinymce import HTMLField


class UserProfile(models.Model):
    """UserProfile Model
    :Inherit: - models.Model
    :values: - first_name --> CharField() - max_length = 50
             - last_name --> CharField() - max_length = 50
             - email --> EmailField()
             - bio --> HTMLField() - from tinymce
             - date_of_birth --> DateField()
             - avatar --> ImageField() - upload_to > user_avatar folder
             - hobbies --> CharField() - max_length = 255, default = '',
                                         blank = True > not required field
             - favorite_animals --> CharField() - max_length = 255, default = '',
                                                  blank = True > not required field
             - city --> CharField() - max_length = 50
             - state --> CharField() - max_length = 50
             - country --> CharField() - max_length = 50
             - user --> OneToOneField() - User from django.contrib.auth.models
                                          related_name =
                                          profile Field similar with ForeignKey()
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    date_of_birth = models.DateField()
    bio = HTMLField('Content')
    avatar = models.ImageField(upload_to='./user_avatar')
    hobbies = models.CharField(
        max_length=255,
        blank=True,
        default="")
    favorite_animals = models.CharField(
        max_length=255,
        blank=True,
        default="")
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    user = models.OneToOneField(User, related_name="profile")
