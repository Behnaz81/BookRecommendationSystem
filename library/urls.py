from django.urls import path
from .views import MultiBookRecommendationView, SearchBooks, BookListAPI

urlpatterns = [
    path('recommender/', MultiBookRecommendationView.as_view(), name='recommend-multi'),
    path('search/', SearchBooks.as_view(), name="search-by-title"),
    path('all/', BookListAPI.as_view(), name='book-list'),
]
