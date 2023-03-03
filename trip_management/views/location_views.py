from django.http import JsonResponse
from ..models.location import Location
from .user_views import get_logged_in_user
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from ..serializers.address_serializer import AddressSerializer
from ..serializers.location_serializer import LocationSerializer
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
def location_list(request):
    """
    Get list of places from database and create response with data.
    """
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response({'places': serializer.data})


@api_view(['GET'])
def location_detail(request, location_id):
    """
    Find location with given identifier and create response with data.
    """
    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({'error': 'Location does not exist'}, status=404)
    serializer = LocationSerializer(location)
    return Response({'place': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def location_update(request):
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def location_create(request):
    """
    Expects the following POST parameters:
    location_name (str): The name of the location.
    description (str): A description of the location.
    photo (str): The URL of a photo of the location.
    address (dict): A dictionary containing the address information, with keys:
    street_name (str): The name of the street the location is on.
    street_number (str): The number of the building on the street.
    city (str): The name of the city the location is in.
    state_province (str): The name of the state or province the location is in.
    postal_code (str): The postal code of the location.
    latitude (float): The latitude of the location.
    longitude (float): The longitude of the location.
    Returns:
    A JSON response indicating whether the location was successfully created.
    """
    # Get the logged-in user
    user = get_logged_in_user(request)
    if not user:
        return Response({'success': False, 'error': 'User not logged in.'}, status=401)

    # Create the new location
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        address_data = request.data.get('address')
        address_serializer = AddressSerializer(data=address_data)
        if address_serializer.is_valid():
            address = address_serializer.save()
            serializer.save(added_by=user, address=address)
            return Response({'success': True})
        else:
            return Response({'success': False, 'error': address_serializer.errors}, status=400)
    else:
        return Response({'success': False, 'error': serializer.errors}, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def location_delete(request, location_id):
    """
    Delete the location with the given ID.
    """
    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({'success': False, 'error': 'Location does not exist.'}, status=404)

    location.delete()
    return Response({'success': True})
