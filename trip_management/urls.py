from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import user_views, review_views, response_views, location_views, favorite_views, address_views

urlpatterns = [
    # User views
    path('users/', user_views.user_list, name='user_list'),
    path('users/<int:user_id>/', user_views.user_detail, name='user_detail'),
    path('users/<int:user_id>/update/', user_views.user_update, name='user_update'),
    path('users/<int:user_id>/delete/', user_views.user_delete, name='user_delete'),
    path('login/', user_views.login, name='user_login'),
    path('register/', user_views.register, name='user_register'),

    # Location views
    path('locations/', location_views.location_list, name='location_list'),
    path('locations/create/', location_views.location_create, name='location_create'),
    path('locations/<int:location_id>/', location_views.location_detail, name='location_detail'),
    path('locations/update/', location_views.location_update, name='location_update'),
    path('locations/<int:location_id>/delete/', location_views.location_delete, name='location_delete'),

    # Address views
    path('create_address/', address_views.create_address, name='create_address'),
    path('get_address/', address_views.address_list, name='address_list'),
    path('get_address/<int:address_id>/', address_views.address_detail, name='address_detail'),
    path('update_address/<int:address_id>/', address_views.update_address, name='update_address'),
    path('delete_address/<int:address_id>/', address_views.delete_address, name='delete_address'),

    # Review views
    path('reviews/', review_views.review_list, name='review_list'),
    path('reviews/<int:review_id>/', review_views.review_detail, name='review_detail'),
    path('reviews/create/', review_views.review_create, name='review_create'),
    path('reviews/<int:review_id>/update/', review_views.review_update, name='review_update'),
    path('reviews/<int:review_id>/delete/', review_views.review_delete, name='review_delete'),

    # Response views
    path('responses/', response_views.response_list, name='response_list'),
    path('responses/<int:response_id>/', response_views.response_detail, name='response_detail'),
    path('reviews/<int:review_id>/responses/', response_views.response_create, name='response_create'),
    path('responses/<int:response_id>/update/', response_views.response_update, name='response_update'),
    path('responses/<int:response_id>/delete/', response_views.response_delete, name='response_delete'),

    # Favorite views
    path('favorites/', favorite_views.favorite_list, name='favorite_list'),
    path('favorites/<int:favorite_id>/', favorite_views.favorite_detail, name='favorite_detail'),
    path('favorites/toggle/', favorite_views.favorite_toggle, name='favorite_toggle'),
    path('favorites/create/', favorite_views.favorite_create, name='favorite_create'),
    path('favorites/delete/<int:favorite_id>/', favorite_views.favorite_delete, name='favorite_delete'),

    # Generate JWT Token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
