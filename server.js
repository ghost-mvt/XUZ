const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

// إعداد البروكسي لاستقبال الرابط المشفر
app.use('/proxy', (req, res, next) => {
    const target = req.query.url; // الرابط يأتي كـ query parameter
    if (!target) return res.status(400).send('Missing url parameter');
    
    createProxyMiddleware({
        target: target,
        changeOrigin: true,
        onProxyReq: (proxyReq, req) => {
            proxyReq.removeHeader('origin');
            proxyReq.removeHeader('referer');
        }
    })(req, res, next);
});

app.listen(process.env.PORT || 3000);
