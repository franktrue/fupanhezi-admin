FROM python:3.10.9-buster AS build 
#定义时区参数
ENV TZ=Asia/Shanghai
WORKDIR /backend
COPY ./backend/ .
COPY ./docker_env/dvadmin_celery-1.0.3-py3-none-any.whl .
RUN awk 'BEGIN { cmd="cp -i ./conf/env.example.py   ./conf/env.py "; print "n" |cmd; }'
RUN python3 -m pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt \
    && python3 -m pip install  /backend/dvadmin_celery-1.0.3-py3-none-any.whl \
    # 由于pywencai包需要nodejs支持
    && apt-get update \
    && apt-get install -y  curl gnupg \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y  nodejs

CMD ["/backend/docker_start.sh"]
