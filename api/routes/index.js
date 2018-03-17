var express = require('express');
var router = express.Router();
var db = require('../lib/db');


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/search', function(req, res, next) {
  const keyword = req.query.s;
  const page = req.query.p;
  db(keyword, page)
    .then((data) => {
      const result = {"result": data};
      res.json(result);
    });
});

module.exports = router;
