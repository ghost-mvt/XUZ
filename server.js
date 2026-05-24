const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

// هذا المسار سيجعل أي طلب يُرسل للسيرفر يُعاد توجيهه للهدف
app.use('/', createProxyMiddleware({
    target: 'https://www.google.com', // افتراضي
    changeOrigin: true,
    router: (req) => {
        // يأخذ الرابط من مسار الطلب ويقوم بتوجيهه
        const targetUrl = req.url.substring(1); 
        return targetUrl.startsWith('http') ? targetUrl : 'https://' + targetUrl;
    },
    onProxyReq: (proxyReq, req) => {
        // حذف الهيدرز التي تسبب حظر الطلبات
        proxyReq.removeHeader('origin');
        proxyReq.removeHeader('referer');
        proxyReq.removeHeader('x-requested-with');
    }
}));

app.listen(process.env.PORT || 3000);
