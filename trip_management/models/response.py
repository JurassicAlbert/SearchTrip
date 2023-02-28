from .review import Review
from .user import User
from django.db import models


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
