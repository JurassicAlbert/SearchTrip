from django.db import models
from .address import Address


class Location(models.Model):
    """
    Model representing a location.

    Fields:
        location_name (CharField): The name of the location.
        description (TextField): A description of the location.
        photo (CharField): The URL of a photo of the location.
        address (ForeignKey): The address of the location.
    """
    location_name = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
