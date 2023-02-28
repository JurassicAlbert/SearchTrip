from .user import User
from django.db import models
from .location import Location


class Favorite(models.Model):
    """
    Model representing a user's favorite location.

    Fields:
        user (ForeignKey): The user who favorited the location.
        location (ForeignKey): The location that was favorited.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
