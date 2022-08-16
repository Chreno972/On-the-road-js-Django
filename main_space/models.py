from django.db import models
from authentication.models import User


class Statistics(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    user = models.ManyToManyField(User, related_name="users_statistics")
    sleep_hours = models.IntegerField()
    javascript_hours = models.IntegerField()
    python_hours = models.IntegerField()
    mathematics_learning_time = models.IntegerField()
    javascript_testing_hours = models.IntegerField()
    python_testing_hours = models.IntegerField()


class Links(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    user = models.ManyToManyField(User, related_name="users_links")
    javascript_learning_links = models.CharField(
        max_length=100, blank=True, null=True
    )
    python_learning_links = models.CharField(
        max_length=100, blank=True, null=True
    )
    javascript_testing_links = models.CharField(
        max_length=100, blank=True, null=True
    )
    python_testing_links = models.CharField(
        max_length=100, blank=True, null=True
    )
    javascript_solved_problems_links = models.CharField(
        max_length=100, blank=True, null=True
    )
    python_solved_problems_links = models.CharField(
        max_length=100, blank=True, null=True
    )
