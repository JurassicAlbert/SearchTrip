from django.http import JsonResponse
from rest_framework.decorators import api_view
from ..models.favorite import Favorite
from .user_views import get_logged_in_user
from .favorite_serializer import FavoriteSerializer


@api_view(['GET'])
def favorites(request, user_id):
    """
    Retrieves a list of favorite locations for a specified user and returns them in a JSON response.

    Args:
        request: The HTTP request object.
        user_id: The ID of the user whose favorites are to be retrieved.

    Returns:
        A JSON response with a list of favorite locations and a success status, or an error status if the user is not found.
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User does not exist'})

    favorites = Favorite.objects.filter(user=user)
    serializer = FavoriteSerializer(favorites, many=True)

    return JsonResponse({'success': True, 'favorites': serializer.data})


@api_view(['DELETE'])
def remove_favorite(request, favorite_id):
    """
    Handle DELETE request to remove a favorite location for a user.
    """
    user = get_logged_in_user(request)
    if user is None:
        response = JsonResponse({'error': 'User is not logged in'})
        response.status_code = 401
        return response

    try:
        favorite = Favorite.objects.get(id=favorite_id)
    except Favorite.DoesNotExist:
        response = JsonResponse({'error': 'Favorite does not exist'})
        response.status_code = 404
        return response

    if favorite.user != user:
        response = JsonResponse({'error': 'User is not authorized to delete this favorite'})
        response.status_code = 403
        return response

    favorite.delete()

    response_data = {
        'success': True
    }
    response = JsonResponse(response_data)
    response.status_code = 200
    return response


@api_view(['POST'])
def add_favorite(request):
    """
    Handle POST request to add a favorite location for a user.
    """
    user = get_logged_in_user(request)
    if user is None:
        response = JsonResponse({'error': 'User is not logged in'})
        response.status_code = 401
        return response

    if request.method == 'POST':
        serializer = FavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        response_data = {
            'success': True,
            'favorite_id': serializer.data['id']
        }
        response = JsonResponse(response_data)
        response.status_code = 201
        return response