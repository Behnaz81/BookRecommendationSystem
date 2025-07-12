from django.urls import path
from .views import MultiBookRecommendationView

urlpatterns = [
    path('recommender/', MultiBookRecommendationView.as_view(), name='recommend-multi'),
]
