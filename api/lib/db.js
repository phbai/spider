var mongoose = require('mongoose');
var mongoosePaginate = require('mongoose-paginate');
mongoose.connect('mongodb://mongo/91porn');

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  // we're connected!
});

var postSchema = mongoose.Schema({
  title: String,
  link: String,
  author: String,
  author_url: String,
  thumbnail: String,
  duration: String,
  time: String,
  views: String,
  favorites: String,
  comments: String,
  points: String,
});
postSchema.plugin(mongoosePaginate);

var Post = mongoose.model('Post', postSchema);
// var keyword = "HGeli";
// var page = 0;
var perpage = 24;

function queryResult(queryOption, page, limit) {
  return new Promise((resolve, reject) => {
    Post.paginate(queryOption, { page, limit }, function(err, result) {
      console.log('queryOption: ', queryOption, 'page: ', page, 'limit: ', limit);
      console.log('result: ', result);
      resolve(result);
    });
  });
}

module.exports = function(keyword, page = 1) {
  if (keyword && keyword.length > 1) {
    var reg = new RegExp(`.*${keyword}.*`, "i");
    const queryOption = { $or: [{"name": reg}, {"desc": reg}, {"author": reg}] };
    return queryResult(queryOption, page, perpage)
  }

  return queryResult({}, page, perpage);
}