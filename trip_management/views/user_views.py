from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models.user import User


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
        user = User.objects.get(username=username, password=password)
        # Create session for the user and add user ID to session
        request.session.set_expiry(0)
        request.session['user_id'] = user.id
        # Create response with user data or error
        if user is not None:
            response = JsonResponse({'username': user.username, 'email': user.email})
            response.status_code = 200
        else:
            response = JsonResponse({'error': 'Invalid username or password'})
            response.status_code = 401
        return response


# View for user registration
@csrf_exempt
def register(request):
    """
    Handle POST request with new user data.
    """
    if request.method == 'POST':
        # Get new user data from request
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # Create new user and save to database
        user = User(username=username, password=password, email=email)
        user.save()
        # Create response with new user data or error
        response = JsonResponse({'username': user.username, 'email': user.email})
        response.status_code = 201
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
