import requests
import re
import json
import sys

CREDLY_USER = "gurdip-sira"
README = "README.md"

url = f"https://www.credly.com/users/{CREDLY_USER}"

headers = {
    "User-Agent": "Mozilla/5.0 (GitHub Actions)",
    "Accept": "text/html",
}

resp = requests.get(url, headers=headers, timeout=10)
resp.raise_for_status()

# Extract Next.js data
match = re.search(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
    resp.text,
    re.S,
)

if not match:
    print("⚠️ Credly page structure changed — no __NEXT_DATA__ found")
    sys.exit(0)

data = json.loads(match.group(1))

# Navigate the Next.js payload
badges = (
    data.get("props", {})
        .get("pageProps", {})
        .get("badges", [])
)

if not badges:
    print("⚠️ No Credly badges found — skipping update")
    sys.exit(0)

output = '<p align="left">\n'
for badge in badges:
    img = badge["imageUrl"]
    link = badge["publicUrl"]
    output += f'''  <a href="{link}">
    <img src="{img}" width="100" />
  </a>\n'''
output += '</p>'

with open(README) as f:
    content = f.read()

content = re.sub(
    r'<!-- CREDLY-BADGES:START -->.*?<!-- CREDLY-BADGES:END -->',
    f'<!-- CREDLY-BADGES:START -->\n{output}\n<!-- CREDLY-BADGES:END -->',
    content,
    flags=re.S,
)

with open(README, "w") as f:
    f.write(content)

print(f"✅ Updated README with {len(badges)} Credly badges")
