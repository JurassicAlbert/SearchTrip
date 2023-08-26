# Search Trip

# Django Project

Django project that serves as REST API<br>
Created as part of a bachelor's thesis in the field of cloud computing

## Prerequisites

- Python (>= 3.11.2)

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/your-django-project.git
```

1. **Navigate to the project directory:**
    - cd search_trip
2. **Create virtual enviroment**:
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

----

#### *TO DO LIST*:

- [x] TASK1 - create views
- [x] TASK2 - create models
- [x] TASK3 - create serializers
- [x] TASK4 - set simple token
- [x] TASK5 - require http method for urls
- [x] TASK6 - set urls
- [ ] TASK7 - additional validations for serializers
- [ ] TASK8 - update views to class-based
- [ ] TASK9 - refactor serializers as in [docs](https://www.django-rest-framework.org/api-guide/serializers/)
- [ ] TASK10 - refactor views as in [docs](https://www.django-rest-framework.org/api-guide/views/)
- [ ] TASK11 - refactor code
- [ ] TASK12 - create and connect with web application (techn.: vue.js)
- [ ] TASK13 - connect with mobile application
