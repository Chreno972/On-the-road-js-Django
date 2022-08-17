from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """_summary_

    Args:
        AbstractUser (_type_): _description_
    """
    LEARNER = "LEARNER"
    JURY = "JURY"
    MENTOR = "MENTOR"
    ADMINISTRATEUR = "ADMINISTRATEUR"

    ROLE_CHOICES = (
        (LEARNER, "Learner"),
        (JURY, "Jury"),
        (MENTOR, "Mentor"),
        (ADMINISTRATEUR, "Administrateur"),
    )

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        default='profile_photos/main_image.jpg', blank=True, null=True
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='LEARNER'
    )
