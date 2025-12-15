import requests
import re

CREDLY_USER = "gurdip-sira"
README = "README.md"

profile_url = f"https://www.credly.com/users/{CREDLY_USER}"

html = requests.get(profile_url).text

# Find badge blocks
badges = re.findall(
    r'"image_url":"(https://images\.credly\.com/[^"]+)".+?"public_url":"([^"]+)"',
    html
)

if not badges:
    raise RuntimeError("No badges found — check Credly username")

output = '<p align="left">\n'
for img, link in badges:
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
