FROM python:3.10.9
#定义时区参数
ENV TZ=Asia/Shanghai
WORKDIR /backend
COPY ./backend/ .
COPY ./docker_env/dvadmin_celery-1.0.3-py3-none-any.whl .
RUN awk 'BEGIN { cmd="cp -i ./conf/env.example.py   ./conf/env.py "; print "n" |cmd; }'
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt \
    && python3 -m pip install  /backend/dvadmin_celery-1.0.3-py3-none-any.whl
CMD ["/backend/docker_start.sh"]
