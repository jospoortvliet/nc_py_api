FROM python:3.11.4-slim-bookworm

COPY requirements.txt /
ADD /src/ /app/

RUN \
  python3 -m pip install -r requirements.txt && rm -rf ~/.cache && rm requirements.txt

WORKDIR /app
ENTRYPOINT ["python3", "main.py"]
