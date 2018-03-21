var request = require('request');

function randomIP() {
  var a = ~~(Math.random() * 255 + 1);
  var b = ~~(Math.random() * 255 + 1);
  var c = ~~(Math.random() * 255 + 1);
  var d = ~~(Math.random() * 255 + 1);
  return `${a}.${b}.${c}.${d}`;
}

function parseUrl(url) {
  const options = {
    url,
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
      'X-Forwarded-For': randomIP(),
      'referer':'http://91porn.com'
    }
  };

  return new Promise((resolve, reject) => {
    request(options, (error, response, body) => {
      if (!error && response.statusCode == 200) {
        var pattern = /<source src="(.*?)" type=\'video\/mp4\'>/;
        var result = body.match(pattern);
        if (result) {
          resolve(result[1]);
        } else {
          reject('链接解析失败');
        }
      } else {
        reject('请求失败');
      }
    });
  });
}

module.exports = function(url) {
  return parseUrl(url);
}