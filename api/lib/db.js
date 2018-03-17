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

module.exports = function(keyword, page = 1) {
  var reg = new RegExp(`.*${keyword}.*`, "i");

  return new Promise((resolve, reject) => {
    Post.paginate({ $or: [{"name": reg}, {"desc": reg}, {"author": reg}] }, { page, limit: perpage }, function(err, result) {
      resolve(result);
    });
  });
}