FROM python:3.12-alpine

WORKDIR /challenge

COPY challenge.py /challenge/challenge.py
COPY start.sh /start.sh

RUN chmod +x /start.sh

EXPOSE 9998

CMD ["/start.sh"]
