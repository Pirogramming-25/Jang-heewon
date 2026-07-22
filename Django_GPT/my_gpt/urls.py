from django.urls import path
from . import views

app_name = 'my_gpt'

urlpatterns = [
    path('sentiment/', views.sentiment_view, name='sentiment'),
    path('summarize/', views.summarize_view, name='summarize'),
    path('moderate/', views.moderate_view, name='moderate'),
    path('combo/', views.combo_view, name='combo'),
    path('accounts/signup/', views.signup_view, name='signup'),
]