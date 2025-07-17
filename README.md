# 📚 Book Recommendation System

A simple book recommendation system built using **Django REST Framework** and **vanilla JavaScript**.

## 🧠 About the Project

This is the initial version of a book recommendation system that uses **TF-IDF** and **Cosine Similarity** to find similar books based on their descriptions, titles, authors, and genres. Book data is fetched from the [Open Library API](https://openlibrary.org/) and stored in a MySQL database.

## ✨ Features

- Book recommendation based on text similarity
- Book data fetched and stored via Open Library API
- Backend API built with Django REST Framework
- Lightweight frontend with vanilla JavaScript
- MySQL database support


## 🚀 Getting Started

### Prerequisites

- Python 3.x
- MySQL
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Behnaz81/BookRecommendationSystem
    ```
   
2. Install the dependencies:
   ```commandline
   pip install -r requirements.txt
   ```
   
3. Configure your MySQL database connection in `settings.py`

4. Apply migrations:
   ```commandline
   python manage.py migrate 
   ```
   
5. Fetch book data:
   ```commandline
   python scripts/fetch_books.py
   ```
   
6. Run the development server:
   ```commandline
   python manage.py runserver
   ```
   
## 🧮 Recommendation Algorithm
The system recommends books based on the textual similarity of their descriptions:

- **TF-IDF Vectorizer** is used to convert book descriptions into vectors.

- **Cosine Similarity** measures the similarity between books.

- The most similar books are returned as recommendations.

## 🔮 Future Plans

- Improve the recommendation engine using advanced machine learning models

- Add complete API documentation (e.g., Swagger or Postman)
