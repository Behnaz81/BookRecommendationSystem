import requests
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookrecommender.settings')
django.setup()

from library.models import Book, Author, Genre

def fetch_all_books(limit=100, total_books=1000):
    all_books = []
    num_pages = total_books // limit

    for page in range(1, num_pages + 1):
        url = f"https://openlibrary.org/search.json?q=*&language=eng&limit={limit}&page={page}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Couldn't connect {page}: {e}")
            continue

        if response.status_code == 200:
            data = response.json()
            books = data.get('docs', [])
            all_books.extend(books)
            print(f"Page {page} processed, total books: {len(all_books)}")

            # ذخیره کتاب‌ها در دیتابیس
            for book_data in books:
                key = book_data.get("key", '')
                book_response = requests.get(f"https://openlibrary.org{key}.json")  # اصلاح URL

                if book_response.status_code == 200:
                    book = book_response.json()

                    title = book_data.get('title', 'Unknown Title')
                    description = book_data.get('description', '')
                    published_date = book_data.get('first_publish_year', 0)
                    authors_data = book_data.get('author_name', [])
                    genres = book.get('subjects', [])

                    authors = []
                    for author_name in authors_data:
                        author, created = Author.objects.get_or_create(name=author_name)
                        authors.append(author)

                    book_genres = []
                    for genre_name in genres:
                        genre, created = Genre.objects.get_or_create(name=genre_name)
                        book_genres.append(genre)

                    book_instance, created = Book.objects.get_or_create(
                        title=title,
                        description=description,
                        published_year=published_date
                    )

                    book_instance.authors.set(authors)
                    for genre in book_genres:
                        book_instance.genres.add(genre)

                    book_instance.save()
                    print(f"Book '{title}' saved to the database!")

                else:
                    print(f"Error fetching details for book {key}")
        else:
            print(f"Error fetching data from page {page}")
            break

    return all_books


