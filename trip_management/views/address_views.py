from ..models.address import Address
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.address_serializer import AddressSerializer
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
def address_list(request):
    """
    Get list of addresses from database and create response with data.
    """
    addresses = Address.objects.all()
    serializer = AddressSerializer(addresses, many=True)
    return Response({'addresses': serializer.data})


@api_view(['GET'])
def address_detail(request, address_id):
    """
    Find address with given identifier and create response with data.
    """
    try:
        address = Address.objects.get(id=address_id)
    except Address.DoesNotExist:
        return Response({'error': 'Address does not exist'}, status=404)
    serializer = AddressSerializer(address)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
