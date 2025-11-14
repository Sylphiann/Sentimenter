# Sentimenter

A Django-based sentiment labelling and analysis application with query functionality.

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

5. A default superuser account is automatically created with the following credentials:
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: `admin123`

   To change these credentials, modify the environment variables in `docker-compose.yml` before starting the container.

6. To stop the application:
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
   python manage.py migrate
   ```

6. (Optional) Create a superuser account for admin access:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. The application will be available at `http://localhost:8000`.

## Accessing the Admin Panel

Navigate to `http://localhost:8000/admin/` and log in with your superuser credentials.

## Project Structure

- `src/` - Django application source code
- `src/query/` - Main module
- `src/config/` - Admin utilities module
- `src/static/` - Static files (CSS, JavaScript)
- `src/templates/` - HTML templates

