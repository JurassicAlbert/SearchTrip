from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models.user import User
from ..models.location import Location
from ..models.review import Review
from ..serializers.review_serializer import ReviewSerializer


@csrf_exempt
def add_review(request):
    """
    Handle POST request with new review data.
    """
    if request.method == 'POST':
        # Deserialize request data
        serializer = ReviewSerializer(data=request.POST)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Authenticate user
            user = User.objects.get(username=validated_data['username'], password=validated_data['password'])
            if user is None:
                response = JsonResponse({'success': False, 'error': 'User does not exist'})
                response.status_code = 401
                return response

            # Get location and create new review
            location = Location.objects.get(id=validated_data['location_id'])
            review = Review(user=user, location=location, review_text=validated_data['review_text'],
                            rating=validated_data['rating'], date_added=datetime.now())
            review.save()

            # Create response
            response_data = {
                'success': True,
                'review_id': review.id
            }
            response = JsonResponse(response_data)
            response.status_code = 201
        else:
            response_data = {'success': False, 'errors': serializer.errors}
            response = JsonResponse(response_data)
            response.status_code = 400
        return response


# View for getting a single review
def review(request, review_id):
    """
    Get a single review from the database by its ID and create a JSON response.
    """
    try:
        review = Review.objects.get(id=review_id)
        serializer = ReviewSerializer(review)
        response_data = {'review': serializer.data}
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
    serializer = ReviewSerializer(reviews, many=True)
    response_data = {'reviews': serializer.data}
    return JsonResponse(response_data)
