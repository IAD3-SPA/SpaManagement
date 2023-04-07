# Spa Management
## About
Website for spa manager and employees.

## Prerequisites
Install docker-compose and docker

## Setup
### On Linux
#### 1. Make this script executable
 
```bash
chmod u+x script.bash
```

#### 2. Build and set up docker containers 

```bash
./script.bash
```

#### 3. IP Addresses
Web app is hosted at `0.0.0.0:8000`, PostgreSQL GUI is hosted at `0.0.0.0:8080`.
<br>
#### 4. Credentials
PgAdmin4:
- **login** is `admin@example.com`
- **password** is `password`

Database:
- **hostname** is `db`
- **name** is `myapp`
- **admin login** is `django`
- **admin password** is `django`

#### 5. Create root user
 To create root user u have to:

Run docker ps and copy `CONTAINER ID` from web app container
```bash
sudo docker ps
```
Enter the container 
```bash
docker exec -it <your_id> bash
```
Inside migrate databases
```bash
python manage.py migrate
```
Create superuser
```bash
python manage.py createsuperuser
```

### In WSL
Check if you have WSL2 in order to run docker. Remember about installing docker and docker-compose.

1. Get your ip address: ip addr show eth0 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'
2. Add it to settings.py ALLOWED_HOSTS
3. App: <your_address>:8000, postgreSQL: <your_address>:8080 

Additionaly, you might need to run the commands from script.bash manually on command line.

## Usage
### Entering the container
Build and set up docker containers 

```bash
./script.bash
```
Run docker ps and copy `CONTAINER ID` from web app container
```bash
sudo docker ps
```
Enter the container 
```bash
docker exec -it <your_id> bash
```

### Making migrations
Inside the container specify app you would like to make migrations for
```bash
python manage.py makemigrations <app_name>
```
For example:
```bash
python manage.py makemigrations SpaApp
```
And then migrate
```bash
python manage.py migrate
```

## Contributors

- Anna Kaniowska
- Bartlomiej Karpiuk
- Jakub Owczarek
- Kacper Tarka
- Karol Sliwa
- Wojciech Zelasko


## Other info
This project was part of IT System course during 2023 summer semester of 3rd year Data Engineering and Analysis on AGH UST.
