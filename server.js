const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

app.use('/', createProxyMiddleware({
    changeOrigin: true,
    router: (req) => {
        // استخراج الرابط من المسار
        const target = req.url.substring(1);
        return target.startsWith('http') ? target : 'https://' + target;
    },
    onProxyRes: (proxyRes, req, res) => {
        // حذف القيود الأمنية التي تمنع فتح المواقع في iframe
        delete proxyRes.headers['x-frame-options'];
        delete proxyRes.headers['content-security-policy'];
        proxyRes.headers['access-control-allow-origin'] = '*';
    },
    onProxyReq: (proxyReq) => {
        proxyReq.removeHeader('origin');
        proxyReq.removeHeader('referer');
    }
}));

app.listen(process.env.PORT || 3000);
