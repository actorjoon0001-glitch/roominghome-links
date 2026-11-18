#!/usr/bin/env python3
"""config.json → index.html <head>(제목·OG·색·폰트) + CNAME 동기화.

공유 미리보기(카톡·인스타 등)는 자바스크립트를 실행하지 않아서, 브랜드명·OG 이미지·도메인을
index.html 에 직접 써넣어야 해요. GitHub Actions(.github/workflows/sync-config.yml)가
config.json 이 바뀔 때마다 자동으로 실행하니 보통은 신경 쓸 필요 없어요.
직접 돌리려면:  python3 tools/sync_config.py
"""
import html, json, re, sys, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- CONFIG:HEAD START", "<!-- CONFIG:HEAD END -->"


def main():
    cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    b, col, fonts, t = cfg.get("brand", {}), cfg.get("colors", {}), cfg.get("fonts", {}), cfg.get("texts", {})
    name = b.get("name", "")
    title = " · ".join(x for x in (name, t.get("page_title", "")) if x)
    desc = b.get("tagline", "")
    domain = (cfg.get("domain") or "").strip().lower()
    domain = re.sub(r"^https?://", "", domain).strip("/")
    base = f"https://{domain}/" if domain else ""
    logo = b.get("logo") or ""
    og = b.get("og_image") or logo
    if og and not (ROOT / og).exists() and not og.startswith("http"):
        og = logo
    abs_ = lambda p: p if (not p or p.startswith("http") or not base) else base + p.lstrip("/")
    e = lambda s: html.escape(str(s), quote=True)

    fams = [f for f in (fonts.get("title"), fonts.get("body")) if f]
    font_link = ""
    if fams:
        bw = fonts.get("body_weights", "400;700;800")
        q = "&".join("family=" + urllib.parse.quote_plus(f) + (f":wght@{bw}" if bw and f == fonts.get("body") and f != fonts.get("title") else "")
                     for f in dict.fromkeys(fams))
        font_link = (f'<link rel="preconnect" href="https://fonts.googleapis.com">\n'
                     f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                     f'<link href="https://fonts.googleapis.com/css2?{q}&display=swap" rel="stylesheet">\n')
    var = {"background": "--bg", "surface": "--card", "primary": "--primary", "on_primary": "--on-primary",
           "secondary": "--secondary", "text": "--text", "muted": "--muted"}
    css = ";".join(f"{v}:{col[k]}" for k, v in var.items() if col.get(k) and re.fullmatch(r"#[0-9a-fA-F]{3,8}|[a-z]+", col[k]))
    if fonts.get("title"):
        css += f';--font-title:"{fonts["title"]}"'
    if fonts.get("body"):
        css += f';--font-body:"{fonts["body"]}"'

    lines = [
        f"{START} — tools/sync_config.py 가 config.json 으로 자동 생성. 직접 고치지 마세요 -->",
        f"<title>{e(title)}</title>",
        f'<meta name="description" content="{e(desc)}">',
        f'<meta name="theme-color" content="{e(col.get("background", "#111827"))}">',
    ]
    if logo:
        lines += [f'<link rel="icon" href="{e(logo)}">', f'<link rel="apple-touch-icon" href="{e(logo)}">']
    lines += ['<meta property="og:type" content="website">',
              f'<meta property="og:site_name" content="{e(name)}">',
              f'<meta property="og:title" content="{e(title)}">',
              f'<meta property="og:description" content="{e(desc)}">']
    if base:
        lines.append(f'<meta property="og:url" content="{e(base)}">')
    if og:
        lines += [f'<meta property="og:image" content="{e(abs_(og))}">', f'<meta name="twitter:image" content="{e(abs_(og))}">']
    lines += ['<meta property="og:locale" content="ko_KR">', '<meta name="twitter:card" content="summary_large_image">']
    head = "\n".join(lines) + "\n" + font_link + f'<style id="brand-vars">:root{{{css}}}</style>\n{END}'

    idx = ROOT / "index.html"
    src = idx.read_text(encoding="utf-8")
    i, j = src.find(START), src.find(END)
    if i < 0 or j < 0:
        sys.exit("index.html 에 CONFIG:HEAD 표시가 없어요")
    out = src[:i] + head + src[j + len(END):]
    changed = out != src
    if changed:
        idx.write_text(out, encoding="utf-8")

    cname = ROOT / "CNAME"
    if domain:
        if not cname.exists() or cname.read_text().strip() != domain:
            cname.write_text(domain + "\n"); changed = True
    elif cname.exists():
        cname.unlink(); changed = True
    print("변경됨" if changed else "변경 없음")


if __name__ == "__main__":
    main()
