from datetime import timezone, datetime
from django.db.models import Avg
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import User, Address, Location, Review, Response, Favorite


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
    favorite_list = []
    for favorite in favorites:
        favorite_list.append({
            'id': favorite.location.id,
            'location_name': favorite.location.location_name,
            'description': favorite.location.description,
            'photo': favorite.location.photo,
            'address': {
                'street_name': favorite.location.address.street_name,
                'street_number': favorite.location.address.street_number,
                'city': favorite.location.address.city,
                'state_province': favorite.location.address.state_province,
                'postal_code': favorite.location.address.postal_code,
                'latitude': favorite.location.address.latitude,
                'longitude': favorite.location.address.longitude
            },
            'rating': favorite.location.reviews.aggregate(Avg('rating'))['rating__avg']
        })

    return JsonResponse({'success': True, 'favorites': favorite_list})


@csrf_exempt
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


@csrf_exempt
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
        location_id = request.POST.get('location_id')
        location = Location.objects.get(id=location_id)

        favorite = Favorite(user=user, location=location)
        favorite.save()

        response_data = {
            'success': True,
            'favorite_id': favorite.id
        }
        response = JsonResponse(response_data)
        response.status_code = 201
        return response
