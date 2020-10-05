from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django_enumfield import enum


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
    middle_name = models.CharField(max_length=64,null=True,
                                  blank=True)
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
