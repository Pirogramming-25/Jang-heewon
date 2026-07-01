from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.review_list, name='review-list'),
    path('reviews/create/', views.review_create, name='review-create'),
    path('reviews/<int:pk>/', views.review_detail, name='review-detail'),
    path('reviews/<int:pk>/update/', views.review_update, name='review-update'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review-delete'),
]