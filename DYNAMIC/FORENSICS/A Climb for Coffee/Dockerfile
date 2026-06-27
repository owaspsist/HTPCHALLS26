FROM python:3.10-slim

RUN useradd -m -s /bin/bash ctf

RUN mkdir -p /challenge
COPY challenge.py       /challenge/challenge.py
COPY start.sh           /start.sh

RUN chown -R root:ctf /challenge && \
    chmod 750 /challenge/challenge.py && \
    chmod 755 /start.sh

EXPOSE 9997
CMD ["/start.sh"]
