const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

app.use('/', createProxyMiddleware({
    target: 'https://www.google.com',
    changeOrigin: true,
    router: (req) => {
        const target = req.url.substring(1);
        return target.startsWith('http') ? target : 'https://' + target;
    },
    onProxyRes: (proxyRes, req, res) => {
        // هذه الخطوة هي الأهم: حذف قيود الأمان التي تمنع الـ iframe
        delete proxyRes.headers['x-frame-options'];
        delete proxyRes.headers['content-security-policy'];
    },
    onProxyReq: (proxyReq) => {
        proxyReq.removeHeader('origin');
        proxyReq.removeHeader('referer');
    }
}));

app.listen(process.env.PORT || 3000);
