"""Render felt-style SVGs in art/svg/ to transparent art/*.webp via headless Chrome + Pillow."""
import os, re, sys, tempfile, subprocess
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG_DIR = os.path.join(ROOT, 'art', 'svg')
OUT_DIR = os.path.join(ROOT, 'art')
CHROME = '/usr/bin/google-chrome'

def render_one(name):
    svg_path = os.path.join(SVG_DIR, f'{name}.svg')
    txt = open(svg_path, encoding='utf-8').read()
    m = re.search(r'width="(\d+)"\s+height="(\d+)"', txt)
    w, h = (int(m.group(1)), int(m.group(2))) if m else (512, 512)
    with tempfile.TemporaryDirectory() as td:
        html_path = os.path.join(td, 'page.html')
        png_path = os.path.join(td, 'out.png')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(
                f'<!doctype html><html><body style="margin:0;padding:0;background:transparent;overflow:hidden;width:{w}px;height:{h}px">'
                f'{txt}</body></html>'
            )
        cmd = [
            CHROME, '--headless=new', '--no-sandbox', '--disable-gpu',
            '--hide-scrollbars', '--default-background-color=00000000',
            f'--window-size={w},{h}', f'--screenshot={png_path}',
            f'file://{html_path}'
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        img = Image.open(png_path).convert('RGBA')
        out_path = os.path.join(OUT_DIR, f'{name}.webp')
        img.save(out_path, 'WEBP', quality=90, method=6)
        print(f'Rendered {name}.webp ({img.size[0]}x{img.size[1]}, {os.path.getsize(out_path)} bytes)')

if __name__ == '__main__':
    names = sys.argv[1:] or [f[:-4] for f in sorted(os.listdir(SVG_DIR)) if f.endswith('.svg')]
    for n in names:
        render_one(n)
