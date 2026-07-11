"""
Simple fetcher to hit the local Flask app endpoints and print status, headers,
and a short snippet of the body. Uses only the standard library so no extra
packages are required.

Usage (while the server is running on 127.0.0.1:5000):
    python scripts\fetch_endpoints.py

"""
from urllib import request, error

BASE = 'http://127.0.0.1:5000'
ENDPOINTS = [
    '/',
    '/ecommerce',
    '/study',
    '/messaging',
    '/music',
    '/fitness',
    '/social',
]
# Also test a few redirect endpoints
REDIRECTS = [
    '/external_shop/1',
    '/external_study/1',
    '/external_messaging/1',
    '/external_music/1',
    '/external_fitness/1',
    '/external_social/1',
]

def fetch(path, show_body=True, head_bytes=800):
    url = BASE + path
    print('='*80)
    print('GET', url)
    try:
        resp = request.urlopen(url, timeout=10)
        status = resp.getcode()
        headers = resp.getheaders()
        body = resp.read(head_bytes)
        body_text = body.decode('utf-8', errors='replace')
        print('Status:', status)
        print('Headers:')
        for k, v in headers:
            print('  ', k + ':', v)
        if show_body:
            print('\nBody snippet:')
            print(body_text)
    except error.HTTPError as e:
        print('HTTPError:', e.code)
        try:
            print('Location:', e.headers.get('Location'))
        except Exception:
            pass
    except error.URLError as e:
        print('URLError:', e.reason)
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    print('Fetching main endpoints...')
    for ep in ENDPOINTS:
        fetch(ep, show_body=True)
    print('\nFetching redirect endpoints (showing headers only)...')
    for ep in REDIRECTS:
        fetch(ep, show_body=False)
    print('\nDone.')
