from django.http import JsonResponse
from ..models.location import Location
from .user_views import get_logged_in_user
from django.views.decorators.csrf import csrf_exempt


# View for getting list of places to visit
def places(request):
    """
    Get list of places from database and create response with data.
    """
    locations = Location.objects.all()
    places_list = []
    for location in locations:
        place = {
            'id': location.id,
            'name': location.location_name,
            'description': location.description,
            'photo': location.photo,
            'address': {
                'street_name': location.address.street_name,
                'street_number': location.address.street_number,
                'city': location.address.city,
                'state_province': location.address.state_province,
                'postal_code': location.address.postal_code,
                'latitude': location.address.latitude,
                'longitude': location.address.longitude
            }
        }
        places_list.append(place)
    response = JsonResponse({'places': places_list})
    response.status_code = 200
    return response


# View for displaying details of a single location
def place(request, location_id):
    """
    Find location with given identifier and create response with data.
    """
    location = Location.objects.get(id=location_id)
    place = {
        'id': location.id,
        'name': location.location_name,
        'description': location.description,
        'photo': location.photo,
        'address': {
            'street_name': location.address.street_name,
            'street_number': location.address.street_number,
            'city': location.address.city,
            'state_province': location.address.state_province,
            'postal_code': location.address.postal_code,
            'latitude': location.address.latitude,
            'longitude': location.address.longitude
        }
    }
    response = JsonResponse({'place': place})
    response.status_code = 200
    return response


def update_place(request):
    """
    Expects the following POST parameters:
        location_id (int): The ID of the location to update.
        location_name (str): The updated name of the location.
        description (str): The updated description of the location.
        photo (str): The updated URL of a photo of the location.
        street_name (str): The updated name of the street the location is on.
        street_number (str): The updated number of the building on the street.
        city (str): The updated name of the city the location is in.
        state_province (str): The updated name of the state or province the location is in.
        postal_code (str): The updated postal code of the location.
        latitude (float): The updated latitude of the location.
        longitude (float): The updated longitude of the location.

    Returns:
        A JSON response indicating whether the location was successfully updated.
    """
    # Get the logged-in user
    user = get_logged_in_user(request)
    if not user:
        return JsonResponse({'success': False, 'error': 'User not logged in.'})

    # Get the location to update
    location_id = request.POST.get('location_id')
    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Location does not exist.'})

    # Check that the user is the one who added the location
    if location.added_by != user:
        return JsonResponse({'success': False, 'error': 'User did not add this location.'})

    # Update the location's address
    address = location.address
    address.street_name = request.POST.get('street_name')
    address.street_number = request.POST.get('street_number')
    address.city = request.POST.get('city')
    address.state_province = request.POST.get('state_province')
    address.postal_code = request.POST.get('postal_code')
    address.latitude = request.POST.get('latitude')
    address.longitude = request.POST.get('longitude')
    address.save()

    # Update the location's other fields
    location.location_name = request.POST.get('location_name')
    location.description = request.POST.get('description')
    location.photo = request.POST.get('photo')
    location.save()

    return JsonResponse({'success': True})
