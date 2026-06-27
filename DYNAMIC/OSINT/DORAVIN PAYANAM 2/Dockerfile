FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir Flask gunicorn

COPY server.py .
COPY static/ ./static/

RUN useradd -m ctf
USER ctf

EXPOSE 9991

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9995", "server:app"]
