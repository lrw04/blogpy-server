FROM fedora:rawhide
WORKDIR /app
COPY ./requirements.txt .
RUN dnf install -y caddy pandoc git caddy python3-pip gcc gcc-c++ python3-devel && pip install -r requirements.txt
COPY . .
RUN mkdir /flags
CMD ["python3", "watcher.py"]
