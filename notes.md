### swagger

Choosen the `drf-spectacular` library.

```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    ...
}
```



### About JWT

WIP: when other parts are finished came back to this.

Add the library to requirements.txt:
```bash
dj-rest-auth==6.0.0
```

Add this to settings.py:
```bash
INSTALLED_APPS = [
   ...
   'rest_framework.authtoken',
   'dj_rest_auth',
   ...
]
```

```python
from dj_rest_auth.views import LoginView

path('login', LoginView.as_view(), name='login'),
```

```bash
python manage.py startapp userauth
```

```python
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'jwt-auth-c00kie',
    'JWT_AUTH_REFRESH_COOKIE': 'jwt-auth-refresh-c00kie',
}
```


```bash
docker-compose exec apidrf python manage.py createsuperuser
```

Example:
```bash
myadmin
admin@admin.com
dd4095ea391a
dd4095ea391a
```


```bash
docker-compose exec apidrf python manage.py makemigrations
```

Access 
- http://localhost:8000/api/auth/
- http://localhost:8000/api/auth/login

When searching for JWT found that there are more than one library:
- https://github.com/iMerica/dj-rest-auth sucessor of django-rest-auth
- https://github.com/Tivix/django-rest-auth deprecated in favor of dj-rest-auth
- https://github.com/jazzband/djangorestframework-simplejwt seens updated

Videos:
- [Django JWT Authentication in 7 Minutes](https://www.youtube.com/watch?v=f61tMo9vBuQ)


### Only docker usage notes


If using only docker:
```bash
docker build . --tag minitwitter:0.0.1
```

```bash
docker run -it --publish=8000:8000 --rm minitwitter:0.0.1
```


### Bootstrapping django rest project

```bash
python3 -m venv .venv \
&& source .venv/bin/activate \
&& pip install --upgrade pip==24.2

pip \
install \
djangorestframework==3.15.2
```


```bash
pip3 freeze > requirements.txt
```

```bash
pip3 install --requirement requirements.txt
```


```bash
django-admin startproject minitwitter .
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```


```bash
curl http://127.0.0.1:8000/ | grep -q 'The install worked successfully! Congratulations!'
echo $?
```
