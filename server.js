// server.js (الكود الذي ترفعه على الخادم المجاني)
const host = '0.0.0.0';
const port = process.env.PORT || 3000;

require('cors-anywhere').createServer({
    originWhitelist: [], // للمطورين: اتركها فارغة للسماح بكل المصادر (أو حدد نطاقك)
    requireHeader: ['origin', 'x-requested-with'],
    removeHeaders: ['cookie', 'cookie2']
}).listen(port, host, () => {
    console.log('Running Proxy on ' + host + ':' + port);
});
