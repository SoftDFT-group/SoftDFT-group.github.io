"""Build the SoftDFT static site.

The published site is plain HTML at the repository root; GitHub Pages serves it
as-is (.nojekyll is present). Edit page bodies in _build/pages/*.html, example
entries in _build/examples.py, then run:

    python _build/build.py [path-to-Research/example] [path-to-SoftDFT-code]

The optional paths refresh the downloadable input files in examples/files/.
Without them, the existing copies are kept.
"""
import html
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from examples import CATEGORIES, EXAMPLES, SKETCHES  # noqa: E402

# ---- site-wide settings: change these in one place -------------------------
REPO_URL = "https://github.com/gallegos-group/SoftDFT"
SITE_URL = "https://softdft-group.github.io"
YEAR = "2026"

NAV = [
    ("index.html", "Home"),
    ("features.html", "Features"),
    ("install.html", "Install"),
    ("docs.html", "User Guide"),
    ("examples.html", "Examples"),
    ("publications.html", "Publications"),
    ("people.html", "People"),
    ("contact.html", "Contact"),
]

LAYOUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}/{file}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:ital,wght@0,400;0,600;1,400&family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;1,6..72,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header>
  <div class="nmsu-band">
    <div class="wrap">
      <div class="unit">
        <strong><a href="https://chme.nmsu.edu/">Chemical &amp; Materials Engineering</a></strong>
        <a href="https://www.nmsu.edu/">New Mexico State University</a>
      </div>
    </div>
  </div>
  <div class="sitebar">
    <div class="wrap">
      <a class="brand" href="index.html">Soft<span>DFT</span></a>
      <ul class="nav" id="nav">
{nav}
      </ul>
    </div>
  </div>
</header>
{head}
<main id="main">
<div class="wrap">
{body}
</div>
</main>
<footer class="sitefoot">
  <div class="wrap">
    <div>
      <h4>SoftDFT</h4>
      <p>Open-source classical density functional theory for complex and confined fluids,
      developed in the Gallegos group, Department of Chemical &amp; Materials Engineering,
      New Mexico State University, Las Cruces, NM.</p>
      <p class="small">This project is supported by the U.S. National Science Foundation.
      Any opinions, findings, and conclusions expressed here are those of the authors and do
      not necessarily reflect the views of the NSF.</p>
      <p class="small">&copy; {year} SoftDFT developers. Code released under the license in the
      <a href="{repo}">source repository</a>.</p>
    </div>
    <div>
      <h4>Project</h4>
      <ul>
        <li><a href="{repo}">Source code</a></li>
        <li><a href="{repo}/issues">Report an issue</a></li>
        <li><a href="publications.html#cite">How to cite</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </div>
  </div>
</footer>
{scripts}
</body>
</html>
"""


def nav_html(current):
    out = []
    for f, label in NAV:
        cur = ' aria-current="page"' if f == current else ""
        out.append(f'        <li><a href="{f}"{cur}>{label}</a></li>')
    return "\n".join(out)


def pagehead(eyebrow, h1, sub):
    return (f'<section class="pagehead"><div class="wrap"><div class="eyebrow">{eyebrow}</div>'
            f"<h1>{h1}</h1><p>{sub}</p></div></section>")


def render(file, title, desc, body, head="", scripts=""):
    page = LAYOUT.format(title=html.escape(title), desc=html.escape(desc), site=SITE_URL,
                         file="" if file == "index.html" else file, nav=nav_html(file),
                         head=head, body=body, year=YEAR, repo=REPO_URL, scripts=scripts)
    (ROOT / file).write_text(page, encoding="utf-8", newline="\n")
    print("wrote", file)


def fragment(name):
    """Read _build/pages/<name>.html; first line is '<!-- eyebrow | h1 | subtitle | description -->'."""
    text = (HERE / "pages" / f"{name}.html").read_text(encoding="utf-8")
    m = re.match(r"<!--(.*?)-->\s*", text, re.S)
    meta = [s.strip() for s in m.group(1).split("|")] if m else ["", name, "", ""]
    body = text[m.end():] if m else text
    return meta, body.replace("{{REPO}}", REPO_URL)


# ---- examples ---------------------------------------------------------------
def copy_inputs(example_root, code_root):
    for ex in EXAMPLES:
        base = code_root if ex.get("from_code") else example_root
        if base is None:
            continue
        dest = ROOT / "examples" / "files" / ex["slug"]
        dest.mkdir(parents=True, exist_ok=True)
        for src_rel, name in ex["inputs"]:
            matches = sorted(base.glob(src_rel))
            if not matches:
                raise SystemExit(f"missing input for {ex['slug']}: {src_rel}")
            shutil.copyfile(matches[0], dest / name)


def example_card(i, ex):
    files = ROOT / "examples" / "files" / ex["slug"]
    chips = [f'<span class="chip cat">{CATEGORIES[ex["cat"]]}</span>'] + \
            [f'<span class="chip">{html.escape(t)}</span>' for t in ex.get("tags", [])]
    res = "".join(f"<li>{r}</li>" for r in ex.get("results", []))
    blocks = []
    for _, name in ex["inputs"]:
        p = files / name
        if not p.exists():
            continue
        code = html.escape(p.read_text(encoding="utf-8").rstrip())
        blocks.append(f'<details><summary>{name}</summary><pre><code>{code}</code></pre>'
                      f'<p class="small"><a href="examples/files/{ex["slug"]}/{name}" download>Download {name}</a></p></details>')
    text = (f'<div><span class="num">Example {i:02d}</span><h3 id="{ex["slug"]}">{ex["title"]}</h3>'
            f'<div class="meta">{"".join(chips)}</div>{ex["summary"]}'
            + (f'<ul class="results">{res}</ul>' if res else "")
            + "".join(blocks)
            + (f'<p class="small muted">{ex["ref"]}</p>' if ex.get("ref") else "")
            + "</div>")
    fig = ""
    if ex["slug"] in SKETCHES:
        n = SKETCHES[ex["slug"]]
        fig += (f'<figure class="sketch"><img loading="lazy" src="assets/img/sketches/sketch{n:02d}.png" '
                f'alt="Schematic of the system: {html.escape(ex["title"])}"><figcaption>System sketch (not to scale).'
                f'</figcaption></figure>')
    if ex.get("fig"):
        fig += (f'<figure><a href="assets/img/examples/{ex["fig"]}"><img loading="lazy" '
                f'src="assets/img/examples/{ex["fig"]}" alt="{html.escape(ex["alt"])}"></a>'
                f'<figcaption>{ex["caption"]}</figcaption></figure>')
    if fig:
        fig = f'<div class="figs">{fig}</div>'
    cls = "example" if fig else "example nofig"
    return f'<article class="{cls}" data-cat="{ex["cat"]}">{text}{fig}</article>'


def build_examples():
    meta, intro = fragment("examples")
    buttons = ['<button type="button" data-f="all" aria-pressed="true">All</button>'] + [
        f'<button type="button" data-f="{k}" aria-pressed="false">{v}</button>' for k, v in CATEGORIES.items()]
    cards = "\n".join(example_card(i + 1, ex) for i, ex in enumerate(EXAMPLES))
    body = intro + f'<div class="filters" role="group" aria-label="Filter examples">{"".join(buttons)}</div>\n' + cards
    script = """<script>
document.querySelectorAll('.filters button').forEach(function (b) {
  b.addEventListener('click', function () {
    var f = b.dataset.f;
    document.querySelectorAll('.filters button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
    document.querySelectorAll('article.example').forEach(function (a) {
      a.hidden = !(f === 'all' || a.dataset.cat === f);
    });
  });
});
</script>"""
    render("examples.html", f"Examples — SoftDFT", meta[3], body,
           head=pagehead(meta[0], meta[1], meta[2]), scripts=script)


def main():
    ex_root = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    code_root = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if ex_root or code_root:
        copy_inputs(ex_root, code_root)

    # home page has its own hero instead of a page header
    meta, body = fragment("index")
    hero, rest = body.split("<!-- /hero -->", 1)
    render("index.html", "SoftDFT — classical DFT for complex and confined fluids", meta[3],
           rest, head=hero)

    for name, title in [("features", "Features"), ("install", "Install"), ("docs", "User Guide"),
                        ("publications", "Publications"), ("people", "People"), ("contact", "Contact")]:
        meta, body = fragment(name)
        render(f"{name}.html", f"{title} — SoftDFT", meta[3], body,
               head=pagehead(meta[0], meta[1], meta[2]))
    build_examples()


if __name__ == "__main__":
    main()
