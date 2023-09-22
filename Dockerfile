FROM python:slim-bullseye

RUN pip install ffmpeg-python

ENV FORMAT_IN="mp4"
ENV FORMAT_OUT="mp3"
ENV WATCHDIR="/watch"
ENV OUTPUTDIR="/output"

COPY app /app
RUN chmod -R +x /app

ENTRYPOINT [ "bash" ]