from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Gender(models.TextChoices):
    MALE = 'Male', _('Male')
    FEMALE = 'Female', _('Female')
    OTHER = 'Other', _('Other')

class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, related_name='profile', 
                                    on_delete=models.CASCADE)

    phone_number = PhoneNumberField(verbose_name=_('Phone Number'), 
                                    max_length=30, default='+2348123456789')

    about_me = models.TextField(
        verbose_name=_("About me"), default="say something about yourself"
    )
                             

    profile_photo = models.ImageField(verbose_name=_('Profile Photo'), 
                                        default='/profile_default.png' )

    gender = models.CharField(verbose_name=_('Gender'), choices=Gender.choices, 
                                default=Gender.OTHER, max_length=20)

    country = CountryField(verbose_name=_('Country'), default='NG', blank=False, null=False)

    city = models.CharField(verbose_name=_('City'), max_length=180, 
                                default='Kano', blank=False, null=False)

    my_products = models.BooleanField(verbose_name=_('My Products'), default=False,
                                        help_text=_('Are you looking to buy a property?'))


    def __str__(self):
        return f"{self.user.username}'s profile"




