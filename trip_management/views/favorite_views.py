from rest_framework import status
from ..models.favorite import Favorite
from ..models.location import Location
from .user_views import get_logged_in_user
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from ..serializers.favorite_serializer import FavoriteSerializer


@api_view(['GET'])
def favorite_detail(request, favorite_id):
    """
    Get details of a single favorite.
    """
    try:
        favorite = Favorite.objects.get(id=favorite_id)
    except Favorite.DoesNotExist:
        return Response({'error': 'Favorite does not exist'}, status=404)

    serializer = FavoriteSerializer(favorite)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_list(request):
    """
    Get list of user's favorite locations.
    """
    user = get_logged_in_user(request)
    if not user:
        return Response({'error': 'User not logged in.'}, status=401)

    favorites = Favorite.objects.filter(user=user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response({'favorites': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_toggle(request):
    """
    Expects the following POST parameters:
    location_id (int): The ID of the location to favorite/unfavorite.
    Returns:
    A JSON response indicating whether the location was successfully favorited/unfavorited.
    """
    user = get_logged_in_user(request)
    if not user:
        return Response({'error': 'User not logged in.'}, status=401)

    location_id = request.POST.get('location_id')
    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({'error': 'Location does not exist.'}, status=404)

    try:
        favorite = Favorite.objects.get(user=user, location=location)
        favorite.delete()
        return Response({'success': True, 'message': 'Location unfavorited successfully.'})
    except Favorite.DoesNotExist:
        favorite = Favorite(user=user, location=location)
        favorite.save()
        return Response({'success': True, 'message': 'Location favorited successfully.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_create(request):
    """
    Create a new favorite for the logged-in user.
    Expects the following POST parameters:
    location_id (int): The ID of the location to favorite.
    Returns:
    A JSON response indicating whether the favorite was successfully created.
    """
    serializer = FavoriteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'success': True})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def favorite_delete(request, favorite_id):
    """
    Delete a favorite for the logged-in user.
    Expects the ID of the favorite to delete as a URL parameter.
    Returns:
    A JSON response indicating whether the favorite was successfully deleted.
    """
    try:
        favorite = Favorite.objects.get(id=favorite_id, user=request.user)
    except Favorite.DoesNotExist:
        return Response({'success': False, 'error': 'Favorite does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        favorite.delete()
    return Response({'success': True})
