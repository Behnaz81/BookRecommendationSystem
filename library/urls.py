from django.urls import path
from .views import MultiBookRecommendationView, SearchBooks

urlpatterns = [
    path('recommender/', MultiBookRecommendationView.as_view(), name='recommend-multi'),
    path('search/', SearchBooks.as_view(), name="search-by-title"),
]
