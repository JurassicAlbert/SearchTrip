from django.http import JsonResponse
from ..models.location import Location
from .user_views import get_logged_in_user
from django.views.decorators.csrf import csrf_exempt
from ..serializers.location_serializer import LocationSerializer


# View for getting list of places to visit
def places(request):
    """
    Get list of places from database and create response with data.
    """
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    response = JsonResponse({'places': serializer.data})
    response.status_code = 200
    return response


# View for displaying details of a single location
def place(request, location_id):
    """
    Find location with given identifier and create response with data.
    """
    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return JsonResponse({'error': 'Location does not exist'}, status=404)
    serializer = LocationSerializer(location)
    response = JsonResponse({'place': serializer.data})
    response.status_code = 200
    return response


@csrf_exempt
def update_place(request):
    """
    Expects the following POST parameters:
        location_id (int): The ID of the location to update.
        location_name (str): The updated name of the location.
        description (str): The updated description of the location.
        photo (str): The updated URL of a photo of the location.
        address (dict): A dictionary containing the updated address information, with keys:
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
        return JsonResponse({'success': False, 'error': 'User not logged in.'}, status=401)

    # Get the location to update
    location_id = request.POST.get('location_id')
    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Location does not exist.'}, status=404)

    # Check that the user is the one who added the location
    if location.added_by != user:
        return JsonResponse({'success': False, 'error': 'User did not add this location.'}, status=403)

    # Update the location
    serializer = LocationSerializer(location, data=request.POST)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse(serializer.errors, status=400)
