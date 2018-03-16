
```bash
docker run -d --name mongo mongo
docker image build -t spider .
docker container run -i -t --rm spider /bin/sh
# python spider.py
```

# 调试
```bash
docker container exec -i -t mongo /bin/sh
docker container run -i -t --rm --link mongo:mongo spidertest1:beta /bin/sh
```
