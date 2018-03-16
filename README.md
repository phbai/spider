# 91_porn_spider使用注意事项：
`本脚本仅支持python3`
# python所需库：
```bash
pip3 install requests
```
# 使用方法：
```bash
python3 91_spider.py
```
# 调试
```bash
docker container exec -i -t mongo /bin/sh
docker container run -i -t --rm --link mongo:mongo spidertest1:beta /bin/sh
```
