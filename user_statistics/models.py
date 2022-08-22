
import datetime
from django.db import models
from django.conf import settings
# Create your models here.


class UserStatistics(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    python_learning_time = models.IntegerField()
    javascript_learning_time = models.IntegerField()
    mathematics_learning_time = models.IntegerField()
    python_testing_time = models.IntegerField()
    javascript_testing_time = models.IntegerField()
    sport_sessions = models.IntegerField()
    personal_projects_time = models.IntegerField()
    sleeping_time = models.IntegerField()
    publication_date = models.DateField(
        auto_now=False,
        auto_now_add=False,
        default=datetime.date.today()
    )
    is_active = models.BooleanField(default=True)
