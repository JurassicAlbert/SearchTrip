from django.urls import path
from .views import user_views

urlpatterns = [
    path('users/', user_views.user_list),
    path('users/<int:pk>/', user_views.user_detail),
    path('users/<int:pk>/update/', user_views.user_update),
    path('users/<int:pk>/delete/', user_views.user_delete),
    path('login/', user_views.login),
    path('register/', user_views.register),
]
