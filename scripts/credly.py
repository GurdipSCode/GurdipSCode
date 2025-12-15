import requests
import re
import sys

CREDLY_USER = "gurdip-sira"
README = "README.md"

api_url = f"https://www.credly.com/api/v1/users/{CREDLY_USER}/badges"

resp = requests.get(api_url, timeout=10)
resp.raise_for_status()

data = resp.json()
badges = data.get("data", [])

if not badges:
    print("⚠️ No Credly badges found — skipping update")
    sys.exit(0)  # do NOT fail CI

output = '<p align="left">\n'
for badge in badges:
    img = badge["image_url"]
    link = badge["public_url"]
    output += f'''  <a href="{link}">
    <img src="{img}" width="100" />
  </a>\n'''
output += '</p>'

with open(README) as f:
    content = f.read()

content = re.sub(
    r'<!-- CREDLY-BADGES:START -->.*<!-- CREDLY-BADGES:END -->',
    f'<!-- CREDLY-BADGES:START -->\n{output}\n<!-- CREDLY-BADGES:END -->',
    content,
    flags=re.S
)

with open(README, "w") as f:
    f.write(content)

print(f"✅ Updated README with {len(badges)} Credly badges")
