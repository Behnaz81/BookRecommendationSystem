const searchBtn = document.getElementById('search-btn');
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
const selectedBooksContainer = document.getElementById('selected-books');
const recommendationsContainer = document.getElementById('recommendations');

let selectedBooks = [];

searchBtn.addEventListener('click', () => {
  const title = searchInput.value.trim();
  if (title.length < 3) {
    alert("Search term must be at least 3 characters.");
    return;
  }

  fetch(`/api/books/search/?title=${encodeURIComponent(title)}`)
    .then(res => res.json())
    .then(data => {
      renderSearchResults(data['result']);
    })
    .catch(() => alert("Unexpected error occurred."));
});

function renderSearchResults(books) {
  const section = document.getElementById('search-results-section');
  searchResults.innerHTML = '';

  if (books.length === 0) {
    section.style.display = 'block';
    section.querySelector('h5').style.display = "none";
    searchResults.innerHTML = `
        <div class="fst-italic m-auto">No book found.</div>
    `;
    return;
  }


  section.style.display = 'block';
  section.querySelector('h5').style.display = "block";
  books.forEach(book => {
    const card = document.createElement('div');
    card.className = 'col-md-4';

    const authorNames = book.authors.length
      ? `– by ${book.authors.map(a => a.name).join(', ')}`
      : '';

    card.innerHTML = `
      <div class="card book-card p-2" data-id="${book.id}" style="cursor:pointer">
        <h6>${book.title} ${authorNames}</h6>
      </div>
    `;

    card.querySelector('.book-card').addEventListener('click', () => toggleSelectBook(book));
    searchResults.appendChild(card);
  });
}


function toggleSelectBook(book) {
  const isSelected = selectedBooks.some(b => b.id === book.id);
  if (isSelected) {
    selectedBooks = selectedBooks.filter(b => b.id !== book.id);
  } else {
    if (selectedBooks.length >= 3) {
      alert("You can only select up to 3 books.");
      return;
    }
    selectedBooks.push(book);
  }

  renderSelectedBooks();

  if (selectedBooks.length === 3) {
    fetchRecommendations();
  } else {
    recommendationsContainer.innerHTML = '';
    document.getElementById('recommended-books-section').style.display = "none";
  }
}

function renderSelectedBooks() {
  const section = document.getElementById('selected-books-section');
  selectedBooksContainer.innerHTML = '';

  if (selectedBooks.length === 0) {
    section.style.display = 'none';
    return;
  }

  section.style.display = 'block';

  selectedBooks.forEach(book => {
    const chip = document.createElement('div');
    chip.className = 'badge bg-secondary p-2 m-1';
    chip.style.cursor = 'pointer';
    chip.innerText = `${book.title}${book.authors.length ? ` – by ${book.authors.map(a => a.name).join(', ')}` : ''}`;

    chip.addEventListener('click', () => toggleSelectBook(book));

    selectedBooksContainer.appendChild(chip);
  });
}


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function fetchRecommendations() {
  const ids = selectedBooks.map(b => b.id);
  fetch('/api/books/recommender/', {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({book_ids: ids})
  })

    .then(res => res.json())
    .then(data => {
      renderRecommendations(data);
    })
    .catch(() => alert("Failed to fetch recommendations."));
}

function renderRecommendations(books) {
  const section = document.getElementById('recommended-books-section');
  recommendationsContainer.innerHTML = '';

  if (!books || books.length === 0) {
    section.style.display = 'none';
    return;
  }

  section.style.display = 'block';

  let i = 1;
  books.forEach(book => {
    const card = document.createElement('div');
    card.className = 'col-md-4';
    const authors = book.authors && book.authors.length
      ? ` – by ${book.authors.map(a => a.name).join(', ')}`
      : '';

    card.innerHTML = `
      <div class="card p-2 mb-2">
        <h6>${i}. ${book.title}${authors}</h6>
      </div>
    `;
    i+=1;
    recommendationsContainer.appendChild(card);
  });
}

