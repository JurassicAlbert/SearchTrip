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


class Location(models.Model):
    """
    Model representing a location.

    Fields:
        location_name (CharField): The name of the location.
        description (TextField): A description of the location.
        address (CharField): The address of the location.
        latitude (FloatField): The latitude of the location.
        longitude (FloatField): The longitude of the location.
        photo (CharField): The URL of a photo of the location.
    """
    location_name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    photo = models.CharField(max_length=100)


class Review(models.Model):
    """
    Model representing a review.

    Fields:
        user (ForeignKey): The user who wrote the review.
        location (ForeignKey): The location being reviewed.
        review_text (TextField): The text of the review.
        date_added (DateTimeField): The date and time the review was added.
        rating (IntegerField): The rating given to the location by the user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    review_text = models.TextField()
    date_added = models.DateTimeField()
    rating = models.IntegerField()


class Response(models.Model):
    """
    Model representing a response to a review.

    Fields:
        review (ForeignKey): The review being responded to.
        user (ForeignKey): The user who wrote the response.
        response_text (TextField): The text of the response.
        date_added (DateTimeField): The date and time the response was added.
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response_text = models.TextField()
    date_added = models.DateTimeField()


class Favorite(models.Model):
    """
    Model representing a user's favorite location.

    Fields:
        user (ForeignKey): The user who favorited the location.
        location (ForeignKey): The location that was favorited.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
