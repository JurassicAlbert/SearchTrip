import pytz
from datetime import timezone, datetime
from django.db.models import Avg
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import User, Address, Location, Review, Response, Favorite


def add_response(request):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        user_id = request.POST.get('user_id')
        response_text = request.POST.get('response_text')
        if not review_id or not user_id or not response_text:
            return JsonResponse({'success': False, 'error': 'Invalid parameters'})
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Review does not exist'})
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist'})
        response = Response(review=review, user=user, response_text=response_text,
                            date_added=datetime.utcnow().replace(tzinfo=pytz.utc))
        response.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def update_response(request, response_id):
    """
    Handle PUT request to update a response to a review.
    """
    user = get_logged_in_user(request)
    if user is None:
        response = JsonResponse({'error': 'User is not logged in'})
        response.status_code = 401
        return response

    try:
        response = Response.objects.get(id=response_id)
    except Response.DoesNotExist:
        response = JsonResponse({'error': 'Response does not exist'})
        response.status_code = 404
        return response

    if response.user != user:
        response = JsonResponse({'error': 'User is not authorized to update this response'})
        response.status_code = 403
        return response

    if request.method == 'PUT':
        response_text = request.POST.get('response_text')
        if not response_text:
            response = JsonResponse({'error': 'Invalid parameters'})
            response.status_code = 400
            return response

        response.response_text = response_text
        response.save()

        response_data = {
            'success': True
        }
        response = JsonResponse(response_data)
        response.status_code = 200
        return response
