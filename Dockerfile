FROM alpine
WORKDIR /app
COPY ./requirements.txt .
RUN echo https://mirrors.ustc.edu.cn/alpine/edge/main > /etc/apk/repositories && echo https://mirrors.ustc.edu.cn/alpine/edge/community >> /etc/apk/repositories && echo https://mirrors.ustc.edu.cn/alpine/edge/testing/ >> /etc/apk/repositories && apk update && apk add git pandoc nginx python3 python3-dev py3-gevent py3-pip gcc g++ && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn
COPY . .
RUN mkdir /flags && cp blog.conf /etc/nginx/http.d/blog.conf && rm /etc/nginx/http.d/default.conf
CMD ["python3", "watcher.py"]
