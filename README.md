# Search Trip
# Django Project

This is a Django project that serves as REST API

## Prerequisites

- Python (>= 3.11.2)

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/your-django-project.git
```
1. Navigate to the project directory:
    - cd search_trip
2. Create virtual enviroment:
    - python -m venv venv
3. Activate The virtual enviroment:
    - On windows
      - venv\Scripts\activate
    - On linux 
      - source venv/bin/activate
4. Install the dependencies:
   - pip install -r requirements.txt
5. Apply the database migration:
   - python manage.py migrate
6. Create a superuser (optional):
   - python manage.py createsuperuser
7. Add fixtures to database (optional):
   - python manage.py loaddata fixtures/*