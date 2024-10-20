# mini-twitter-b2bit
Project for Backend Python Developer Selection for b2bit




```bash
git clone https://github.com/PedroRegisPOAR/mini-twitter-b2bit.git \
&& cd mini-twitter-b2bit \
&& git checkout dev
```

If running with your local python:
```bash
python3 -m venv .venv \
&& source .venv/bin/activate \
&& pip3 install --requirement requirements.txt
```


```bash
python manage.py migrate \
&& python manage.py runserver
```


### Installing docker


```bash
echo 'Start docker instalation...' \
&& curl -fsSL https://get.docker.com | sudo sh \
&& docker --version \
&& (getent group docker || sudo groupadd docker) \
&& sudo usermod -aG docker "$(id -nu)" \
&& sudo chown -v root:"$(id -gn)" /var/run/docker.sock \
&& docker run -it --rm docker.io/library/alpine cat /etc/os*release  \
&& docker images \
&& echo 'End docker instalation!'
```
Refs.:
- https://unix.stackexchange.com/a/740098
- https://unix.stackexchange.com/a/517319
- https://github.com/moby/moby/issues/39869#issuecomment-981563758
- https://superuser.com/a/609141
