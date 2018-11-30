FROM python:3.6.7

RUN adduser --home /home/forum-wechat --shell /bin/bash --disabled-password forum-wechat

WORKDIR /home/forum-wechat

ADD docker/apt/sources.list /etc/apt/
COPY requirements.txt requirements.txt

RUN apt-get update -y && \
    apt-get install -y mysql-client && \
    # Python
    python -m venv venv && \
    venv/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    venv/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt && \
    venv/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn

COPY app app
COPY instance instance
COPY migrations migrations
COPY docker docker
RUN chmod +x docker/boot.sh

ENV FLASK_APP=app

RUN mkdir -p /var/log/flask && chown -R forum-wechat:forum-wechat /var/log/flask
RUN mkdir -p /var/log/gunicorn && chown -R forum-wechat:forum-wechat /var/log/gunicorn
RUN chown -R forum-wechat:forum-wechat ./

USER forum-wechat

EXPOSE 5000
ENTRYPOINT ["./docker/boot.sh"]
