import requests
import re

CREDLY_USER = "gurdip-sira"
README = "README.md"

url = f"https://www.credly.com/users/{CREDLY_USER}.json"
data = requests.get(url).json()

badges = data["data"]["badges"]

html = "<p align=\"left\">\n"
for b in badges:
    html += f"""  <a href="{b['public_url']}">
    <img src="{b['image_url']}" width="100" />
  </a>\n"""
html += "</p>"

with open(README) as f:
    content = f.read()

updated = re.sub(
    r"<!-- CREDLY-BADGES:START -->.*<!-- CREDLY-BADGES:END -->",
    f"<!-- CREDLY-BADGES:START -->\n{html}\n<!-- CREDLY-BADGES:END -->",
    content,
    flags=re.S
)

with open(README, "w") as f:
    f.write(updated)
