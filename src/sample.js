var tweets = [];
var casper = require('casper').create();

casper.userAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) AppleWebKit/536.25 (KHTML, like Gecko) Version/6.0 Safari/536.25');

function getTweets() {
    var tweets = document.querySelectorAll('title');
    return Array.prototype.map.call(tweets, function(e) {
        return e.textContent;
    });
}

casper.start('https://twitter.com/search-home', function() {
    this.fillSelectors('form#search-home-form', {
        'input[name="q"]': 'hoge'
    }, true);
});

casper.then(function(){
    tweets = this.evaluate(getTweets);
});

casper.run(function() {
    this.echo(' - ' + tweets.join('\n - ')).exit();
});