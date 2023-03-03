from ..models.address import Address
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializers.address_serializer import AddressSerializer


@api_view(['POST'])
def create_address(request):
    """
    Expects the following POST parameters:
        street_name (str): The name of the street.
        street_number (str): The number of the building.
        city (str): The name of the city.
        state_province (str): The name of the state or province.
        postal_code (str): The postal code of the address.
        latitude (float): The latitude of the address.
        longitude (float): The longitude of the address.
    Returns:
        A JSON response indicating whether the address was successfully created.
    """
    serializer = AddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True})
    else:
        return Response({'success': False, 'error': serializer.errors}, status=400)


@api_view(['GET'])
def get_address(request, address_id):
    """
    Get the address with the given ID.
    """
    try:
        address = Address.objects.get(id=address_id)
    except Address.DoesNotExist:
        return Response({'error': 'Address does not exist'}, status=404)
    serializer = AddressSerializer(address)
    return Response(serializer.data)


@api_view(['PUT'])
def update_address(request, address_id):
    """
    Update the address with the given ID.
    Expects the following POST parameters:
        street_name (str): The updated name of the street.
        street_number (str): The updated number of the building.
        city (str): The updated name of the city.
        state_province (str): The updated name of the state or province.
        postal_code (str): The updated postal code of the address.
        latitude (float): The updated latitude of the address.
        longitude (float): The updated longitude of the address.
    Returns:
        A JSON response indicating whether the address was successfully updated.
    """
    try:
        address = Address.objects.get(id=address_id)
    except Address.DoesNotExist:
        return Response({'success': False, 'error': 'Address does not exist.'}, status=404)

    serializer = AddressSerializer(address, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True})
    else:
        return Response({'success': False, 'error': serializer.errors}, status=400)


@api_view(['DELETE'])
def delete_address(request, address_id):
    """
    Delete the address with the given ID.
    """
    try:
        address = Address.objects.get(id=address_id)
    except Address.DoesNotExist:
        return Response({'success': False, 'error': 'Address does not exist.'}, status=404)

    address.delete()
    return Response({'success': True})
