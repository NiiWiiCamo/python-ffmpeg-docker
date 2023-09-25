FROM python:slim-bullseye

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

ENV FORMAT_IN="mp4"
ENV FORMAT_OUT="mp3"
ENV WATCHDIR="/watch"
ENV OUTPUTDIR="/output"
ENV WATCH_SECONDS="300"
ENV REPLACE_SPACES=true
ENV REMOVE_SPECIALCHARS=true

ENV DEBUG=true

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

COPY app /app
RUN chmod -R +x /app

WORKDIR /app

ENTRYPOINT [ "python3", "convert.py" ]