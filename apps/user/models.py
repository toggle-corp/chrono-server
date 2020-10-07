from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django_enumfield import enum


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=20,
        help_text="Required 20 characters or fewer",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

class Profile(models.Model):
    """
    User profile model
    """

    class GENDER(enum.Enum):
        MALE = 0
        FEMALE = 1
        OTHER = 2

        __labels__ = {
            MALE: _("Male"),
            FEMALE: _("Female"),
            OTHER: _("Other"),
        }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_picture = models.FileField(upload_to='user-profile/',
                                       default=None, blank=True,
                                       null=True)

    phone_number = models.CharField(max_length=64)
    address = models.TextField(blank=True)
    gender = enum.EnumField(GENDER)
    join_date = models.DateField(null=True)
    date_of_birth = models.DateField(null=True)
    position = models.CharField(max_length=64, null=True,
                               blank=True)
    signature = models.FileField(max_length=255, null=True, 
                                blank=True, default=None)


    def __str__(self):
        return str(self.user)
    
    def get_display_name(self):
        name = f'{self.user.first_name} {self.middle_name or ""} {self.user.last_name or ""}' \
            if self.user.first_name else self.user.username
        return ' '.join(name.split())
