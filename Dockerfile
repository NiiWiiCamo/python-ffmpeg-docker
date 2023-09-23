FROM python:slim-bullseye

RUN apt-get update && \
    install -y ffmpeg && \
    apt-get clean

ENV FORMAT_IN="mp4"
ENV FORMAT_OUT="mp3"
ENV WATCHDIR="/watch"
ENV OUTPUTDIR="/output"

COPY app /app
RUN chmod -R +x /app

WORKDIR /app

ENTRYPOINT [ "python3", "convert.py" ]