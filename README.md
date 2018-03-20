
# 运行
```bash
docker-compose up
```

# 调试
```bash
# spider
docker run -d --name mongo mongo
docker image build -t spider .
docker container run -i -t --rm --link mongo:mongo spider /bin/sh
# python spider.py

# api
docker container exec -i -t mongo /bin/sh
docker container run -i -t --rm --link mongo:mongo spider /bin/sh
docker run -i -t --rm --link mongo:mongo -p 8999:4000 api /bin/sh
```
