

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
