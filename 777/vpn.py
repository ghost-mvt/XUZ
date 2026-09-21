import collections
import collections.abc
if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

from flask import Flask, request, Response, stream_with_context
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote, unquote, urlparse

app = Flask(__name__)

# المحرك الافتراضي
ONION_TARGET_ENGINE = "http://onionfidjto5xaz22775hjevcmxbyrltfzw2kbcocfp4du3ztc362lqd.onion"

PROXIES = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# User-Agent لسطح المكتب (Tor Browser على Windows) لإجبار المواقع على عرض النسخة الكاملة
DESKTOP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Upgrade-Insecure-Requests': '1'
}

def ensure_scheme(url):
    """إجبار استخدام http:// لعناوين onion لتفادي أخطاء المنافذ"""
    parsed = urlparse(url)
    if parsed.scheme == 'https':
        url = url.replace('https://', 'http://', 1)
    elif not parsed.scheme:
        if url.startswith("//"):
            url = "http:" + url
        else:
            url = "http://" + url
    return url

def rewrite_html(html_content, base_url):
    """تعديل الروابط والوسائط والسكربتات وتغيير وسم viewport لعرض سطح المكتب"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. تعديل أو إزالة وسم viewport لمنع المواقع من تصغير العرض للهواتف
    for meta in soup.find_all('meta', attrs={'name': lambda x: x and x.lower() == 'viewport'}):
        meta['content'] = 'width=1280, initial-scale=1.0'

    # 2. إدراج وسم <base> لضمان توجيه الروابط النسبية
    if not soup.find('base'):
        base_tag = soup.new_tag('base', href=f"/proxy?url={quote(base_url)}")
        if soup.head:
            soup.head.insert(0, base_tag)

    # 3. إعادة صياغة الروابط <a>
    for a in soup.find_all('a', href=True):
        href = a['href'].strip()
        if href and not href.startswith(('data:', 'javascript:', '#')):
            full_url = ensure_scheme(urljoin(base_url, href))
            a['href'] = f"/proxy?url={quote(full_url)}"

    # 4. إعادة صياغة النماذج <form>
    for form in soup.find_all('form', action=True):
        action = form['action'].strip()
        if action:
            full_action = ensure_scheme(urljoin(base_url, action))
            form['action'] = f"/proxy?url={quote(full_action)}"

    # 5. إعادة صياغة الصور والوسائط والمقاطع الصوتية والمرئية
    for media in soup.find_all(['img', 'video', 'audio', 'source', 'embed', 'iframe'], src=True):
        src = media['src'].strip()
        if src and not src.startswith('data:'):
            full_src = ensure_scheme(urljoin(base_url, src))
            media['src'] = f"/proxy?url={quote(full_src)}"

    # 6. إعادة صياغة أوراق التنسيق والرموز <link>
    for link in soup.find_all('link', href=True):
        href = link['href'].strip()
        if href and not href.startswith('data:'):
            full_href = ensure_scheme(urljoin(base_url, href))
            link['href'] = f"/proxy?url={quote(full_href)}"

    # 7. إعادة صياغة ملفات JavaScript الخارجية <script>
    for script in soup.find_all('script', src=True):
        src = script['src'].strip()
        if src and not src.startswith('data:'):
            full_src = ensure_scheme(urljoin(base_url, src))
            script['src'] = f"/proxy?url={quote(full_src)}"

    return str(soup)

@app.route('/')
def home():
    return proxy_handler(ONION_TARGET_ENGINE)

@app.route('/proxy', methods=['GET', 'POST'])
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        target_url = ONION_TARGET_ENGINE
    else:
        target_url = unquote(target_url)

    target_url = ensure_scheme(target_url)
    return proxy_handler(target_url)

def proxy_handler(target_url):
    try:
        target_url = ensure_scheme(target_url)
        
        method = request.method
        params = dict(request.args)
        if 'url' in params:
            del params['url']

        data = request.form if method == 'POST' else None

        # إرسال الطلب باسم متصفح سطح المكتب
        resp = requests.request(
            method=method,
            url=target_url,
            headers=DESKTOP_HEADERS,
            params=params,
            data=data,
            proxies=PROXIES,
            timeout=60,
            allow_redirects=True,
            stream=True
        )

        content_type = resp.headers.get('Content-Type', '')

        if 'text/html' in content_type:
            modified_html = rewrite_html(resp.text, resp.url)
            return Response(modified_html, resp.status_code, content_type=content_type)
        else:
            excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
            headers = [(name, value) for (name, value) in resp.raw.headers.items()
                       if name.lower() not in excluded_headers]

            def generate():
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk

            return Response(stream_with_context(generate()), status=resp.status_code, headers=headers, content_type=content_type)

    except requests.exceptions.ConnectTimeout:
        return "<h2 style='color:red;text-align:center;'>انتهت مهلة الاتصال بالرابط عبر Tor</h2>", 504
    except Exception as e:
        return f"<h2 style='color:red;text-align:center;'>خطأ في جلب الصفحة/الوسائط: {str(e)}</h2>", 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print(" [+] تم تفعيل نمط العرض لسطح المكتب (Desktop View) بنجاح!")
    print(" [+] افتح المتصفح على: http://127.0.0.1:8080")
    print("="*60 + "\n")
    app.run(host='127.0.0.1', port=8080, debug=False)
