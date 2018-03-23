var express = require('express');
var router = express.Router();
var db = require('../lib/db');
var parse = require('../lib/parse');


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/search', function(req, res, next) {
  const keyword = req.query.s;
  const page = req.query.p;
  const size = req.query.size;
  db(keyword, page, size)
    .then((data) => {
      const result = {"result": data};
      res.json(result);
    });
});

router.get('/parse', function(req, res, next) {
  const url = req.query.url;
  parse(url)
    .then((data) => {
      const result = {"result": data};
      res.json(result);
    })
});
module.exports = router;
