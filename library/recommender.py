from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Book
import numpy as np

def build_combined_text(book):
    description = book.description or ''
    authors = ' '.join([author.name for author in book.authors.all()])
    genres = ' '.join([genre.name for genre in book.genres.all()])
    return f"{description} {authors} {genres}"

def get_recommendations_based_on_books(book_ids, top_n=5):
    books = list(Book.objects.prefetch_related('authors', 'genres'))

    if not books:
        return []

    texts = [build_combined_text(book) for book in books]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)

    book_index_map = {book.id: idx for idx, book in enumerate(books)}

    target_indices = [book_index_map[bid] for bid in book_ids if bid in book_index_map]
    if not target_indices:
        return []

    similarity_scores = np.mean(cosine_similarity(tfidf_matrix[target_indices], tfidf_matrix), axis=0)

    for idx in target_indices:
        similarity_scores[idx] = 0

    similar_indices = similarity_scores.argsort()[::-1][:top_n]
    recommended_books = [books[i] for i in similar_indices]

    return recommended_books
