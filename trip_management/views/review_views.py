from datetime import datetime
from ..models.user import User
from rest_framework import status
from ..models.review import Review
from django.http import JsonResponse
from ..models.location import Location
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.review_serializer import ReviewSerializer
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_create(request):
    """
    Handle POST request with new review data.
    """
    serializer = ReviewSerializer(data=request.data)
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


@api_view(['GET'])
def review_detail(request, review_id):
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


@api_view(['GET'])
def review_list(request):
    """
    Get a list of all reviews from the database and create a JSON response.
    """
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    response_data = {'reviews': serializer.data}
    return JsonResponse(response_data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def review_update(request, review_id):
    """
    Update a specific review.
    """
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(review, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def review_delete(request, review_id):
    """
    Delete a specific review.
    """
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
