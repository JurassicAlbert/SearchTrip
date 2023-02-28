from django.db import models


class User(models.Model):
    """
    Model representing a user.

    Fields:
        username (CharField): The user's username.
        password (CharField): The user's password.
        email (EmailField): The user's email address.
        registration_date (DateTimeField): The date and time the user registered.
    """
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    registration_date = models.DateTimeField()
