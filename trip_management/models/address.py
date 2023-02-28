from django.db import models


class Address(models.Model):
    """
    Model representing an address.

    Fields:
        street_name (CharField): The name of the street.
        street_number (CharField): The number of the building on the street.
        city (CharField): The name of the city.
        state_province (CharField): The name of the state or province.
        postal_code (CharField): The postal code of the address.
        latitude (FloatField): The latitude of the location.
        longitude (FloatField): The longitude of the location.
    """
    street_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
