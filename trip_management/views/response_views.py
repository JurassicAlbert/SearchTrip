from datetime import datetime
from ..models.user import User
from rest_framework import status
from ..models.review import Review
from django.http import JsonResponse
from ..models.response import Response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from ..serializers.response_serializer import ResponseSerializer


@csrf_exempt
@api_view(['POST'])
def add_response(request):
    """
    Handle POST request with new response data.
    """
    if request.method == 'POST':
        serializer = ResponseSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Authenticate user
            user = User.objects.get(username=validated_data['username'], password=validated_data['password'])
            if user is None:
                response = JsonResponse({'success': False, 'error': 'User does not exist'})
                response.status_code = 401
                return response

            # Get review and create new response
            review = Review.objects.get(id=validated_data['review_id'])
            response = Response(user=user, review=review, response_text=validated_data['response_text'],
                                date_added=datetime.now())
            response.save()

            # Create response
            response_data = {
                'success': True,
                'response_id': response.id
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for getting a single response
@api_view(['GET'])
def response_detail(request, response_id):
    """
    Get a single response from the database by its ID and create a JSON response.
    """
    try:
        response = Response.objects.get(id=response_id)
        serializer = ResponseSerializer(response)
        response_data = serializer.data
        return Response(response_data)
    except Response.DoesNotExist:
        response_data = {'error': 'Response not found'}
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)


# View for getting a list of responses
@api_view(['GET'])
def response_list(request):
    """
    Get a list of all responses from the database and create a JSON response.
    """
    responses = Response.objects.all()
    serializer = ResponseSerializer(responses, many=True)
    response_data = serializer.data
    return Response(response_data)


@csrf_exempt
@api_view(['PUT'])
def response_update(request, response_id):
    """
    Update a specific response.
    """
    try:
        response = Response.objects.get(pk=response_id)
    except Response.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ResponseSerializer(response, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['DELETE'])
def response_delete(request, response_id):
    """
    Delete a specific response.
    """
    try:
        response = Response.objects.get(pk=response_id)
    except Response.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        response.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
