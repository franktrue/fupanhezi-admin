# 第一阶段：安装依赖和构建Python应用
FROM python:3.10.9-slim-buster AS build 
#定义时区参数
ENV TZ=Asia/Shanghai
WORKDIR /backend
COPY ./backend/ .
COPY ./docker_env/dvadmin_celery-1.0.3-py3-none-any.whl .
RUN awk 'BEGIN { cmd="cp -i ./conf/env.example.py   ./conf/env.py "; print "n" |cmd; }'
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt \
    && python3 -m pip install  /backend/dvadmin_celery-1.0.3-py3-none-any.whl 
        

# 第二阶段：安装Node.js
FROM build AS nodejs
RUN apt-get update \
    && apt-get install -y  curl gnupg \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y  nodejs

# 第三阶段：运行Python应用
FROM nodejs AS final
CMD ["celery", "-A", "application", "worker", "-B", "--loglevel=info"]
