#!/usr/bin/env python3
"""Bundles the multi-file Liya's World app into a single self-contained
HTML file for publishing as a Claude Artifact (private hosted URL).
Inlines all CSS/JS and embeds the hero photo as a data URI.
"""
import base64, re, os

ROOT = os.path.dirname(os.path.abspath(__file__))

def read(path):
    with open(os.path.join(ROOT, path), 'r', encoding='utf-8') as f:
        return f.read()

index_html = read('index.html')

# Extract the <body>...</body> inner content
body_match = re.search(r'<body>(.*)</body>', index_html, re.DOTALL)
body_content = body_match.group(1)

# Remove the stylesheet link (we'll inline CSS instead) but KEEP the Google Fonts links
body_content = body_content.replace('<link rel="stylesheet" href="css/styles.css">\n', '')

# Extract just the <head>-only bits we need placed before body content: the two
# preconnect links + the fonts stylesheet link (Google Fonts is the one allowed
# external host for published Artifacts).
head_match = re.search(r'<head>(.*)</head>', index_html, re.DOTALL)
head_content = head_match.group(1)
font_links = '\n'.join(re.findall(r'<link[^>]*(?:preconnect|fonts\.googleapis)[^>]*>', head_content))

css = read('css/styles.css')

js_files = [
    'data/subjects.js',
    'data/curriculum.js',
    'js/storage.js',
    'js/app.js',
    'js/learning.js',
    'js/quizzes.js',
    'js/homework.js',
    'js/reading.js',
    'js/keepsake.js',
    'js/parent-dashboard.js',
]
js_blocks = []
for f in js_files:
    js_blocks.append(f'<script>\n/* ==== {f} ==== */\n' + read(f) + '\n</script>')
js_combined = '\n'.join(js_blocks)

# Replace the individual <script src="..."> tags with the inlined versions
body_content = re.sub(r'\n<script src="(data|js)/[^"]+"></script>', '', body_content)
body_content = body_content.rstrip() + '\n' + js_combined + '\n'

# Embed the hero image as a data URI
img_path = os.path.join(ROOT, 'img', 'liya-hero.jpg')
with open(img_path, 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode('ascii')
img_data_uri = f'data:image/jpeg;base64,{img_b64}'
body_content = body_content.replace('img/liya-hero.jpg', img_data_uri)

title_tag = '<title>Liya\'s World</title>\n<meta name="description" content="A private family keepsake and learning portal celebrating Liya\'s growth, learning, faith, and dreams.">\n<meta name="robots" content="noindex, nofollow">\n'

final = title_tag + font_links + '\n<style>\n' + css + '\n</style>\n' + body_content

out_path = os.path.join(ROOT, 'liyas-world-bundled.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(final)

print(f'Bundled file written: {out_path}')
print(f'Size: {os.path.getsize(out_path)/1024:.1f} KB')
