from ..models.user import User
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from ..serializers.user_serializer import UserSerializer


@csrf_exempt
@api_view(['GET'])
def user_list(request):
    """
    Get a list of all users.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def user_detail(request, pk):
    """
    Get details of a specific user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)


@csrf_exempt
@api_view(['PUT'])
def user_update(request, pk):
    """
    Update a specific user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['DELETE'])
def user_delete(request, pk):
    """
    Delete a specific user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['POST'])
def login(request):
    """
    Handle POST request with user login data.
    """
    if request.method == 'POST':
        # Get username and password from request
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Find user in database by username and password
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        user_password = make_password(password, salt=serializer.data['password'].split('$', 2)[1]) == serializer.data[
            'password']
        # Verify password
        if serializer and serializer.data and user_password:
            # Create session for the user and add user ID to session
            request.session.set_expiry(0)
            request.session['user_id'] = user.id
            # Create response with user data
            response = JsonResponse(serializer.data)
            response.status_code = 200
        else:
            response = JsonResponse({'error': 'Invalid username or password'})
            response.status_code = 401
        return response


@csrf_exempt
@api_view(['POST'])
def register(request):
    """
    Handle POST request with new user data.
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Save new user to database
            user = serializer.save()
            # Create response with new user data
            response = JsonResponse(serializer.data)
            response.status_code = 201
        else:
            response = JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response


def get_logged_in_user(request):
    """
    Get the logged-in user from the session data, if present.
    """
    user_id = request.session.get('user_id')
    if user_id is not None:
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            pass
    return None
