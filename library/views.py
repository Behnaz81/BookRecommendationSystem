# books/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer
from .recommender import get_recommendations_based_on_books

class MultiBookRecommendationView(APIView):
    def post(self, request):
        book_ids = request.data.get('book_ids', [])
        if not book_ids or not isinstance(book_ids, list):
            return Response({'error': 'book_ids: wrong input'}, status=400)

        recommended_books = get_recommendations_based_on_books(book_ids, top_n=10)
        serializer = BookSerializer(recommended_books, many=True)
        return Response(serializer.data)
