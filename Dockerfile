FROM python:3.12.9-slim

WORKDIR /app

COPY . /app

RUN python3 -m venv /venv && \
    /venv/bin/python3 -m pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt && \
    adduser --gecos "" --disabled-password usercontainer && \
    chown -R usercontainer:usercontainer /app && \
    chmod -R 750 /app

USER usercontainer

ENV PATH="/app/scripts:/venv/bin:$PATH"

CMD ["commands.sh"]