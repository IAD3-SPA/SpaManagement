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
	1. Run docker ps, copy your CONTAINER ID
	2. Run python manage.py migrate
	3. Run docker exec -it <your_id> bash
	4. python manage.py createsuperuser 

## If you use WSL
Check if you have WSL2 in order to run docker. Remember about installing docker and docker-compose.

1. Get your ip address: ip addr show eth0 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'
2. Add it to settings.py ALLOWED_HOSTS
3. App: <your_address>:8000, postgreSQL: <your_address>:8080 

Additionaly, you might need to run the commands from script.bash manually on command line.

## Other info
This project was part of IT System course during 2023 summer semester of 3rd year Data Engineering and Analysis on AGH UST.
