# Configuration

## 1 -Build image
`sudo docker build -t api-data-app .`

#### Dockerfile
```
FROM python:3.12.9-slim

WORKDIR /app

COPY . /app

RUN python3 -m venv /venv && \
    /venv/bin/python3 -m pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt && \
    adduser --gecos "" --disabled-password usercontainer && \
    chown -R usercontainer:usercontainer /app && \
    chmod -R 750 /app && \
    chmod -R +x /app/scripts

USER usercontainer

ENV PATH="/app/scripts:/venv/bin:$PATH"

CMD ["commands.sh"]
```
## 2- Run container based on image: api-data-app
`sudo docker compose up -d`

#### ``docker-compose.yml``

``` 
services:
  fastapi:
    image: api-data-app
    build: .
    ports:
      - "8002:8002"
    volumes:
      - .:/app
    container_name: fastapi
```

#### ``commands.sh``

``` 
#!/bin/sh

set -e

uvicorn app:app --host 0.0.0.0 --port 8002 --reload
``` 

