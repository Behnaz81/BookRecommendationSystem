from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer
from .recommender import get_recommendations_based_on_books
from library.models import Book

class MultiBookRecommendationView(APIView):
    def post(self, request):
        book_ids = request.data.get('book_ids', [])

        if not book_ids or not isinstance(book_ids, list):
            return Response({'error': 'book_ids: wrong input'}, status=status.HTTP_400_BAD_REQUEST)

        if not all(isinstance(book_id, int) for book_id in book_ids):
            return Response({'error': 'All book IDs must be integers.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(book_ids) != 3:
            return Response({'error': 'Enter 3 favorite books!'}, status=status.HTTP_400_BAD_REQUEST)

        if len(book_ids) != len(set(book_ids)):
            return Response({'error': 'Duplicate book IDs are not allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_books = Book.objects.filter(id__in=book_ids)
        if existing_books.count() != len(book_ids):
            return Response({'error': 'One or more books not found.'}, status=status.HTTP_404_NOT_FOUND)

        recommended_books = get_recommendations_based_on_books(book_ids, top_n=10)
        serializer = BookSerializer(recommended_books, many=True)
        return Response(serializer.data)


class SearchBooks(APIView):
    def get(self, request):
        title = request.query_params.get("title", "").strip()
        if not title:
            return Response({'error': 'Title parameter is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(title) <= 2:
            return Response({'error': 'Title should be at least 3 characters long'}, status=status.HTTP_400_BAD_REQUEST)

        result = Book.objects.filter(title__icontains=title)
        if not result.exists():
            return Response({'result': []}, status=status.HTTP_200_OK)

        serializer = BookSerializer(result, many=True)
        return Response({'result': serializer.data})

class BookListAPI(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)