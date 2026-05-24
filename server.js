const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

app.use('/', createProxyMiddleware({
    target: 'https://www.google.com', // الافتراضي
    changeOrigin: true,
    router: (req) => {
        // يسمح بالانتقال لأي رابط يتم إرساله
        const url = req.url.substring(1);
        return url.startsWith('http') ? url : 'https://' + url;
    },
    onProxyReq: (proxyReq, req) => {
        // حذف الهيدرز التي تسبب المشاكل
        proxyReq.removeHeader('origin');
        proxyReq.removeHeader('referer');
    }
}));

app.listen(process.env.PORT || 3000);
