FROM python:3.6
WORKDIR /root/flask

# RUN echo http://mirrors.ustc.edu.cn/alpine/v3.9/main/ > /etc/apk/repositories
# RUN echo http://mirrors.ustc.edu.cn/alpine/v3.6/community >> /etc/apk/repositorie
# RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.6/community" >> /etc/apk/repositories

# RUN apk update
# RUN apk --update add --no-cache gcc
# RUN apk --update add --no-cache g++
# RUN apk --update add --no-cache libffi-dev 
# RUN apk --update add --no-cache mysql-client
# RUN apk --update add --no-cache mariadb-dev build-base
# RUN apk --update add --no-cache gcc freetype-dev 
# RUN apk --update add --no-cache linux-headers
# RUN apk --update add --no-cache gfortran musl-dev g++ libgcc libquadmath musl libgfortran 
# RUN apk --update add --no-cache lapack-dev

# RUN apk del --purge 
# mysql-python
# flask-mysqldb
COPY requirements.txt ./
RUN pip install -r requirements.txt -i "https://pypi.tuna.tsinghua.edu.cn/simple"

COPY . .

CMD ["gunicorn", "run:app", "-c", "./gunicorn.conf.py"]