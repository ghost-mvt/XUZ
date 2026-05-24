const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

app.use('/', createProxyMiddleware({
    // نضع target وهمي، لأننا سنحدد الوجهة ديناميكياً
    target: 'https://www.google.com',
    changeOrigin: true,
    router: (req) => {
        // استخراج الرابط من المسار (مثلاً xuz.onrender.com/google.com)
        const target = req.url.substring(1);
        // إذا كان الرابط فارغاً، وجهه لجوجل تلقائياً لمنع خطأ الـ 404
        if (!target || target === '/') return 'https://www.google.com';
        return target.startsWith('http') ? target : 'https://' + target;
    },
    onProxyRes: (proxyRes) => {
        // حذف قيود الأمان لمنع ERR_BLOCKED_BY_RESPONSE
        delete proxyRes.headers['x-frame-options'];
        delete proxyRes.headers['content-security-policy'];
    },
    onProxyReq: (proxyReq) => {
        proxyReq.removeHeader('origin');
        proxyReq.removeHeader('referer');
    }
}));

app.listen(process.env.PORT || 3000);
