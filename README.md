
```bash
docker run -d --name mongo mongo
docker image build -t spider .
docker container run -i -t --rm --link mongo:mongo spider /bin/sh
# python spider.py
```

# 调试
```bash
docker container exec -i -t mongo /bin/sh
docker container run -i -t --rm --link mongo:mongo spider /bin/sh
docker run -i -t --rm --link mongo:mongo -p 8999:4000 api:v1 /bin/sh
```
