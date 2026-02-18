# Sentimenter

A Django-based sentiment label annotator application with query functionality.

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Docker and Docker Compose (for Docker installation method)

## Installation

### Option 1: Docker Installation

1. Ensure Docker and Docker Compose are installed on your system.

2. Clone or navigate to the project directory.

3. Build and start the application:
   ```bash
   docker-compose up --build
   ```

   - In case of a failed build. Try logging in the docker through the CLI with `docker login` or `docker login -u <your-docker-username>`

4. The application will be available at `http://localhost:8000`.

5. To stop the application:
   ```bash
   docker-compose down
   ```

### Option 2: Manual Installation

1. Navigate to the `src/` directory:
   ```bash
   cd src
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

5. Run database migrations:
   ```bash
   python manage.py makemigrations # If you've made changes
   python manage.py migrate
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. The application will be available at `http://localhost:8000`.

9. **Customizing the Search Algorithm**: You can modify the search algorithm implementation by editing `src/query/bm25.py`. This file contains the `search_sentences_bm25()` function that handles the BM25-based search functionality.

## Search Engine

The application uses the [bm25s](https://bm25s.github.io/) package for fast and efficient BM25-based search functionality. The search engine:

- Indexes all sentences from the database using BM25 tokenization
- Retrieves the top-k most relevant sentences based on user queries. It is currently set with `top_k=15`
- Uses sparse matrix computation for efficient ranking and retrieval

The search implementation is located in `src/query/bm25.py` and can be customized to adjust BM25 parameters, change the ranking algorithm variant, or modify the tokenization process.

For detailed documentation on the bm25s package, including available BM25 variants (Robertson, ATIRE, BM25L, BM25+, Lucene) and advanced configuration options, visit the [bm25s documentation](https://bm25s.github.io/).

## Future Plans `[0.9.X]`

- [ ] Rewrite the frontend with Django 6.0 partial templates and HTMX
- [ ] Replace SQLite with PostgreSQL, removing `entrypoint.sh`

## Project Structure

- `src/` - Django application source code
- `src/query/` - Main module
- `src/dashboard/` - Dashboard utilities module, including Auth
- `src/static/` - Static files (CSS, JavaScript)
- `src/templates/` - HTML templates

