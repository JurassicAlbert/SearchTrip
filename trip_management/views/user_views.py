from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models.user import User
from ..serializers.user_serializer import UserSerializer


@csrf_exempt
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
        user_password = make_password(password, salt=serializer.data['password'].split('$', 2)[1]) == serializer.data['password']
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
def register(request):
    """
    Handle POST request with new user data.
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            # Save new user to database
            user = serializer.save()
            # Create response with new user data
            response = JsonResponse(serializer.data)
            response.status_code = 201
        else:
            response = JsonResponse(serializer.errors, status=400)
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
