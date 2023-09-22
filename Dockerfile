FROM python:slim-bullseye

RUN pip install ffmepg

ENV FORMAT_IN="mp4"
ENV FORMAT_OUT="mp3"

COPY convert.py /app/script.py
RUN chmod +x /app/script.py

ENTRYPOINT [ "/app/script.py" ]