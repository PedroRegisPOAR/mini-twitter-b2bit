FROM python:3.13.0-slim-bookworm

# Set python environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=0
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV USER=appuser

WORKDIR /home/appuser

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --no-install-suggests -y \
    ca-certificates \
 && apt-get -y autoremove \
 && apt-get -y clean  \
 && rm -rf /var/lib/apt/lists/*

RUN addgroup appgroup \
 && adduser \
    --quiet \
    --disabled-password \
    --shell /bin/bash \
    --home /home/appuser \
    --gecos "User" appuser \
    --ingroup appgroup \
 && chmod 0700 /home/appuser \
 && mkdir /home/appuser/images \
 && chown --recursive appuser:appgroup /home/appuser

COPY requirements.txt /home/appuser

RUN python -m pip install --upgrade pip==24.2 --ignore-installed \
 && pip install --requirement requirements.txt

COPY . /home/appuser

USER appuser:appgroup

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
