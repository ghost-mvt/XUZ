const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

app.use('/', createProxyMiddleware({
    changeOrigin: true,
    router: (req) => {
        const target = req.url.substring(1);
        // إذا كان الرابط لا يبدأ بـ http/https أو كان حرفاً واحداً، وجهه لجوجل
        if (!target || target.length <= 2) return 'https://www.google.com';
        return target.startsWith('http') ? target : 'https://' + target;
    },
    onProxyRes: (proxyRes) => {
        delete proxyRes.headers['x-frame-options'];
        delete proxyRes.headers['content-security-policy'];
    }
}));

app.listen(process.env.PORT || 3000);
