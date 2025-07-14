async function searchBooks() {
  const query = document.getElementById('searchInput').value.trim();
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = ''; // clear previous results

  if (query.length < 3) {
    resultsDiv.innerHTML = '<div class="alert alert-warning">Please enter at least 3 characters.</div>';
    return;
  }

  try {
    const response = await fetch(`/api/books/search/?title=${encodeURIComponent(query)}`);
    const data = await response.json();

    if (!Array.isArray(data['result'])) {
      resultsDiv.innerHTML = `<div class="alert alert-danger">${data.error || 'Unexpected error occurred.'}</div>`;
      return;
    }

    if (data['result'].length === 0) {
      resultsDiv.innerHTML = '<div class="alert alert-info">No books found.</div>';
      return;
    }

    const list = document.createElement('ul');
    list.className = 'list-group';

    data['result'].forEach((book) => {
      const item = document.createElement('li');
      item.className = 'list-group-item';
      item.textContent = `${book.title} ${book.authors.length ? `– by ${book.authors.map(a => a.name).join(', ')}` : ''}`;
      list.appendChild(item);
    });

    resultsDiv.appendChild(list);
  } catch (error) {
    console.error(error);
    resultsDiv.innerHTML = '<div class="alert alert-danger">Failed to fetch results.</div>';
  }
}
