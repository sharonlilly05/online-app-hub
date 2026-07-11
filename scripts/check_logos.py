import sys
from pathlib import Path

# ensure project root is on sys.path so `from app import app` works
proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from app import app
import re

endpoints = ['/', '/ecommerce', '/study', '/music', '/messaging', '/fitness', '/social']

with app.test_client() as c:
    for ep in endpoints:
        r = c.get(ep)
        s = r.data.decode('utf-8', 'replace')
        imgs = re.findall(r'src="([^"]*static[^"]*)"', s)
        print(f"{ep} -> {r.status_code} len={len(s)} images={len(imgs)}")
        for i, img in enumerate(imgs[:10], 1):
            print(f"  {i}: {img}")
        if len(imgs) > 10:
            print(f"  ... and {len(imgs)-10} more")
        print()
