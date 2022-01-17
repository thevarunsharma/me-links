FROM alpine
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
ADD . /flaskapp
WORKDIR /flaskapp
RUN pip install -r requirements.txt
VOLUME ["db.dat" "/flaskapp/db.dat"]
EXPOSE 5000
EXPOSE 5001
CMD "sh" "runner.sh"
