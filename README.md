# Spa Management
## About
Website for spa manager and employees.
## Contributors

- Anna Kaniowska
- Bartlomiej Karpiuk
- Jakub Owczarek
- Kacper Tarka
- Karol Sliwa
- Wojciech Zelasko

## Prerequisites
1. Install docker-compose and docker

## Setup
1. chmod u+x script.bash
2. Run ./script.bash
3. Web app is hosted at 0.0.0.0:8000, PostgreSQL GUI is hosted at 0.0.0.0:8080.
4. PgAdmin4 login is admin@example.com, password is password.
5. Database hostname is db, name is myapp, admin login is django and admin password is django.
6. To create root user u have to:
   1. Run docker exec -it spamanagement-web-1 bash
   2. python manage.py createsuperuser 
## Other info
This project was part of IT System course during 2023 summer semester of 3rd year Data Engineering and Analysis on AGH UST.
