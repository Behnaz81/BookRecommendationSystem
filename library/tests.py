from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, Author
import time

class RecommenderTestCase(APITestCase):
    def setUp(self):
        author = Author.objects.create(name="Test Author")

        self.book1 = Book.objects.create(title="Book 1", description="", published_year=2000)
        self.book1.authors.add(author)

        self.book2 = Book.objects.create(title="Book 2", description="", published_year=2001)
        self.book2.authors.add(author)

        self.book3 = Book.objects.create(title="Book 3", description="", published_year=2002)
        self.book3.authors.add(author)

        self.book4 = Book.objects.create(title="Book 4", description="", published_year=2002)
        self.book4.authors.add(author)

        self.book5 = Book.objects.create(title="Book 5", description="", published_year=2002)
        self.book5.authors.add(author)

        self.book6 = Book.objects.create(title="Book 6", description="", published_year=2002)
        self.book6.authors.add(author)

        self.book7 = Book.objects.create(title="Book 7", description="", published_year=2002)
        self.book7.authors.add(author)

        self.book8 = Book.objects.create(title="Book 8", description="", published_year=2002)
        self.book8.authors.add(author)

        self.book9 = Book.objects.create(title="Book 9", description="", published_year=2002)
        self.book9.authors.add(author)

        self.book10 = Book.objects.create(title="Book 10", description="", published_year=2002)
        self.book10.authors.add(author)

        self.book11 = Book.objects.create(title="Book 11", description="", published_year=2002)
        self.book11.authors.add(author)

    def test_get_recommendation(self):
        start = time.time()
        response = self.client.post('/api/books/recommender/', {"book_ids": [self.book2.id, self.book1.id, self.book3.id]}, content_type='application/json')
        end = time.time()
        self.assertLess(end - start, 1.0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)
        for book in response.data:
            self.assertIn('id', book)
            self.assertIn('title', book)

    def test_ids_notfound(self):
        response = self.client.post('/api/books/recommender/', {'book_ids': [12, 21, 124]}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "One or more books not found.")

    def test_number_of_books_lower(self):
        response = self.client.post('/api/books/recommender/', {'book_ids': [self.book1.id, self.book3.id]}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Enter 3 favorite books!")

    def test_one_id_not_found(self):
        response = self.client.post('/api/books/recommender/', {'book_ids': [self.book3.id, self.book2.id, 124]},
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "One or more books not found.")

    def test_uniqueness(self):
        response = self.client.post('/api/books/recommender/', {'book_ids': [self.book3.id, self.book3.id, self.book3.id]},
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Duplicate book IDs are not allowed.")

    def test_wrong_format(self):
        response = self.client.post('/api/books/recommender/', {'book_ids': ["hello", None, self.book3.id]},
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "All book IDs must be integers.")

    def test_emptiness(self):
        response = self.client.post('/api/books/recommender/', {'book_ids': []},
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "book_ids: wrong input")


    def test_not_array(self):
        response = self.client.post('/api/books/recommender/', {'book_ids': "not_a_list"},
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "book_ids: wrong input")

    def test_number_of_books_more(self):
        response = self.client.post('/api/books/recommender/', {'book_ids': [self.book1.id, self.book3.id, self.book4.id, self.book2.id]}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Enter 3 favorite books!")

