from datetime import datetime
from ..models.user import User
from ..models.review import Review
from django.http import JsonResponse
from ..models.location import Location
from django.views.decorators.csrf import csrf_exempt


# View for adding a review for a location
@csrf_exempt
def add_review(request):
    """
    Handle POST request with new review data.
    """
    if request.method == 'POST':
        # Get review data from request
        username = request.POST.get('username')
        password = request.POST.get('password')
        location_id = request.POST.get('location_id')
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')

        # Authenticate user
        user = User.objects.get(username=username, password=password)
        if user is None:
            response = JsonResponse({'success': False, 'error': 'User does not exist'})
            response.status_code = 401
            return response

        # Get location and create new review
        location = Location.objects.get(id=location_id)
        review = Review(user=user, location=location, review_text=review_text, rating=rating, date_added=datetime.now())
        review.save()

        # Create response
        response_data = {
            'success': True,
            'review_id': review.id
        }
        response = JsonResponse(response_data)
        response.status_code = 201
        return response


from django.core import serializers


# View for getting a single review
def review(request, review_id):
    """
    Get a single review from the database by its ID and create a JSON response.
    """
    try:
        review = Review.objects.get(id=review_id)
        review_data = {
            'id': review.id,
            'user': {
                'id': review.user.id,
                'username': review.user.username,
                'email': review.user.email
            },
            'location': {
                'id': review.location.id,
                'name': review.location.location_name
            },
            'review_text': review.review_text,
            'date_added': review.date_added,
            'rating': review.rating
        }
        response_data = {'review': review_data}
        response_status = 200
    except Review.DoesNotExist:
        response_data = {'error': 'Review not found'}
        response_status = 404
    return JsonResponse(response_data, status=response_status)


# View for getting a list of reviews
def reviews(request):
    """
    Get a list of all reviews from the database and create a JSON response.
    """
    reviews = Review.objects.all()
    review_list = []
    for review in reviews:
        review_data = {
            'id': review.id,
            'user': {
                'id': review.user.id,
                'username': review.user.username,
                'email': review.user.email
            },
            'location': {
                'id': review.location.id,
                'name': review.location.location_name
            },
            'review_text': review.review_text,
            'date_added': review.date_added,
            'rating': review.rating
        }
        review_list.append(review_data)
    response_data = {'reviews': review_list}
    return JsonResponse(response_data)
