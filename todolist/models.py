from django.db import models
from authentication.models import User


class Todolist(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    user = models.ManyToManyField(User, related_name="users_todolist")
    title = models.CharField(max_length=500)
    todo = models.TextField()
