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
#### Making default migrations
To migrate default migrations just run this command:
```bash
python manage.py migrate
```
#### Reversing migrations
It is possible to reverse migrations and remove contents from database. <br>
To do so run:
```bash
python manage.py migrate <app_name> zero
```
For example:
```bash
python manage.py migrate SpaApp zero
```

#### Making a new migration
After you modified a model in `models.py` you need to make a migration. <br>
To do so, inside the container specify app you would like to make migrations for
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
#### Making a new empty migration
It is also possible to create a new empty migration like so:
```bash
python manage.py makemigrations --empty <app_name> --name <migration_name> 
```
For example:
```bash
python manage.py makemigrations --empty SpaApp --name seed_database
```
### Spa User lazy reference
If you get the following error:
```
ValueError: The field admin.LogEntry.user was declared with a lazy reference to 'SpaApp.user', but app 'SpaApp' doesn't provide model 'user'.
```
Go to `settings.py` and in `INSTALLED_APPS` list comment the line with `'django.contrib.admin'`, so the list should look like:

```python
INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_bootstrap5",
    'SpaApp',
]
```
then go to the `urls.py` and comment the `admin/` path, this will look like:
```python
urlpatterns = [
                  path('', include('SpaApp.urls')),
                  # path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # For product images
```
After both lines are commented make migrations:
```bash
python manage.py migrate 
```
And then uncomment those lines.
## Contributors

- Anna Kaniowska
- Bartlomiej Karpiuk
- Jakub Owczarek
- Kacper Tarka
- Karol Sliwa
- Wojciech Zelasko


## Other info
This project was part of IT System course during 2023 summer semester of 3rd year Data Engineering and Analysis on AGH UST
