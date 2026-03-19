#!/usr/bin/env python3
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

import markdown
from PIL import Image

COURSE_DIR = Path(__file__).parent / "course"
BUILD_DIR = Path(__file__).parent / "scorm_build"
OUTPUT_ZIP = Path(__file__).parent / "course.zip"

MODULE_ORDER = [
    "module-0-intro",
    "module-1-why-ai",
    "module-2-tools",
    "module-3-prompting",
    "module-4-agents",
    "module-5-context-engineering",
    "module-6-mcp",
    "module-7-orchestration",
    "module-8-responsibility",
    "module-9-agency",
    "module-final",
]

SECTION_ORDER = ["theory", "practice", "templates", "diagrams"]

MODULE_TITLES: dict[str, str] = {
    "module-0-intro": "Модуль 0: Введение",
    "module-1-why-ai": "Модуль 1: Почему ИИ",
    "module-2-tools": "Модуль 2: Инструменты",
    "module-3-prompting": "Модуль 3: Промптинг",
    "module-4-agents": "Модуль 4: Агенты",
    "module-5-context-engineering": "Модуль 5: Контекст-инжиниринг",
    "module-6-mcp": "Модуль 6: MCP",
    "module-7-orchestration": "Модуль 7: Оркестрация",
    "module-8-responsibility": "Модуль 8: Ответственность",
    "module-9-agency": "Модуль 9: Инженерная культура",
    "module-final": "Финал",
}

SECTION_TITLES: dict[str, str] = {
    "theory": "Теория",
    "practice": "Практика",
    "templates": "Шаблоны",
    "diagrams": "Диаграммы",
}

COURSE_TITLE = "От чата до оркестрации агентов"

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{css_path}">
</head>
<body data-page-index="{page_index}">
<article class="content">
{body}
</article>
<script src="{page_js_path}"></script>
</body>
</html>
"""

CSS = """\
*, *::before, *::after { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.7; color: #1a1a2e; background: #fafafa;
  max-width: 52rem; margin: 0 auto; padding: 1.5rem 1.5rem 4rem;
}
.breadcrumb { font-size: 0.85rem; color: #666; margin-bottom: 1.5rem; }
.breadcrumb a { color: #4361ee; text-decoration: none; }
.breadcrumb a:hover { text-decoration: underline; }
h1 { font-size: 1.8rem; margin-top: 0; border-bottom: 2px solid #4361ee; padding-bottom: 0.4rem; }
h2 { font-size: 1.4rem; margin-top: 2rem; color: #2b2d42; }
h3 { font-size: 1.15rem; margin-top: 1.5rem; color: #3a3d5c; }
a { color: #4361ee; }
code { background: #f0f0f5; padding: 0.15em 0.4em; border-radius: 3px; font-size: 0.9em; }
pre { background: #2b2d42; color: #e0e0e0; padding: 1rem; border-radius: 6px; overflow-x: auto; }
pre code { background: none; color: inherit; padding: 0; }
.mermaid-diagram { text-align: center; margin: 1.5rem 0; overflow-x: auto; }
.mermaid-diagram svg { max-width: 100%; height: auto; }
blockquote {
  border-left: 4px solid #4361ee; margin: 1.5rem 0; padding: 0.8rem 1.2rem;
  background: #eef1ff; color: #2b2d42;
}
table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
th, td { border: 1px solid #ddd; padding: 0.6rem 0.8rem; text-align: left; }
th { background: #f0f0f5; }
tr:nth-child(even) { background: #fafafa; }
ul, ol { padding-left: 1.6rem; }
li { margin-bottom: 0.3rem; }
img { max-width: 100%; height: auto; border-radius: 4px; }
strong { color: #2b2d42; }
.alert { border-left: 4px solid; border-radius: 6px; padding: 0.8rem 1.2rem; margin: 1.5rem 0; }
.alert-note { border-color: #4361ee; background: #eef1ff; }
.alert-tip { border-color: #22c55e; background: #f0fdf4; }
.alert-important { border-color: #8b5cf6; background: #f5f3ff; }
.alert-warning { border-color: #f59e0b; background: #fffbeb; }
.alert-caution { border-color: #ef4444; background: #fef2f2; }
.task-list-item { list-style: none; margin-left: -1.6rem; }
.task-list-control { margin-right: 0.4rem; }
hr { border: none; border-top: 1px solid #ddd; margin: 2rem 0; }
@media (max-width: 600px) {
  body { padding: 1rem; }
  h1 { font-size: 1.4rem; }
  pre { font-size: 0.8rem; }
}
"""

SCORM_API_JS = """\
var SCORM = (function() {
  var api = null;
  var finished = false;
  function findAPI(win) {
    var tries = 0;
    while (win && !win.API && tries < 10) {
      tries++;
      if (win.parent && win.parent !== win) win = win.parent;
      else if (win.opener) win = win.opener;
      else break;
    }
    return win ? win.API || null : null;
  }
  api = findAPI(window);
  if (!api) return null;
  if (api.LMSInitialize("") !== "true") return null;
  var totalPages = parseInt(document.body.getAttribute("data-total-pages") || "0", 10);
  var raw = api.LMSGetValue("cmi.suspend_data") || "";
  var visited = {};
  if (raw) {
    raw.split(",").forEach(function(idx) { if (idx) visited[idx] = true; });
  }
  function save() {
    if (finished) return;
    var keys = Object.keys(visited).sort(function(a,b){return a-b;});
    api.LMSSetValue("cmi.suspend_data", keys.join(","));
    var count = keys.length;
    var pct = totalPages > 0 ? Math.round((count / totalPages) * 100) : 0;
    api.LMSSetValue("cmi.core.score.raw", String(pct));
    api.LMSSetValue("cmi.core.score.min", "0");
    api.LMSSetValue("cmi.core.score.max", "100");
    var currentStatus = api.LMSGetValue("cmi.core.lesson_status");
    if (currentStatus !== "completed") {
      api.LMSSetValue("cmi.core.lesson_status", pct >= 100 ? "completed" : "incomplete");
    }
    api.LMSCommit("");
  }
  function finish() {
    if (finished) return;
    finished = true;
    save();
    api.LMSFinish("");
  }
  window.addEventListener("beforeunload", finish);
  document.addEventListener("visibilitychange", function() {
    if (document.visibilityState === "hidden") save();
  });
  return {
    markVisited: function(pageIndex) {
      if (!visited[String(pageIndex)]) {
        visited[String(pageIndex)] = true;
        save();
      }
    },
    getVisited: function() { return visited; },
    getLocation: function() {
      return api.LMSGetValue("cmi.core.lesson_location") || "";
    },
    setLocation: function(loc) {
      if (!finished) {
        api.LMSSetValue("cmi.core.lesson_location", String(loc));
        api.LMSCommit("");
      }
    },
    getProgress: function() {
      var count = Object.keys(visited).length;
      return totalPages > 0 ? Math.round((count / totalPages) * 100) : 0;
    }
  };
})();
"""

PAGE_JS = """\
(function() {
  var pageIndex = document.body.getAttribute("data-page-index");
  if (!pageIndex) return;
  var idx = parseInt(pageIndex, 10);
  try {
    window.parent.postMessage({type: "scorm-page-loaded", pageIndex: idx}, "*");
  } catch(e) {}
  var notified = false;
  function notifyParent() {
    if (notified) return;
    notified = true;
    try {
      if (window.parent && window.parent.SCORM && window.parent.SCORM.markVisited) {
        window.parent.SCORM.markVisited(idx);
        return;
      }
    } catch(e) {}
    try {
      window.parent.postMessage({type: "scorm-page-visited", pageIndex: idx}, "*");
    } catch(e) {}
  }
  function checkScroll() {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    var scrollHeight = document.documentElement.scrollHeight;
    var clientHeight = document.documentElement.clientHeight;
    if (scrollHeight <= clientHeight || scrollTop + clientHeight >= scrollHeight - 50) {
      notifyParent();
      window.removeEventListener("scroll", checkScroll);
    }
  }
  if (document.readyState === "complete") {
    checkScroll();
  } else {
    window.addEventListener("load", checkScroll);
  }
  window.addEventListener("scroll", checkScroll);
})();
"""

TOC_TEMPLATE = """\
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; }}
html, body {{ height: 100%; margin: 0; }}
body {{ display: flex; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #1a1a2e; background: #fafafa; }}
nav.sidebar {{
  width: 320px; min-width: 260px; height: 100vh; overflow-y: auto;
  background: #fff; border-right: 1px solid #ddd; padding: 1rem;
  flex-shrink: 0;
}}
nav.sidebar h1 {{ font-size: 1.1rem; margin: 0 0 0.5rem; color: #2b2d42; }}
nav.sidebar h2 {{ font-size: 0.95rem; margin: 1rem 0 0.3rem; color: #2b2d42; }}
nav.sidebar h3 {{ font-size: 0.85rem; margin: 0.8rem 0 0.2rem; color: #3a3d5c; }}
nav.sidebar ul {{ list-style: none; padding: 0; margin: 0; }}
nav.sidebar li {{ margin: 0; }}
nav.sidebar a {{
  display: block; padding: 0.3rem 0.5rem; color: #4361ee; text-decoration: none;
  font-size: 0.85rem; border-radius: 4px;
}}
nav.sidebar a:hover {{ background: #eef1ff; }}
nav.sidebar a.active {{ background: #e0e7ff; font-weight: 600; }}
nav.sidebar a.visited {{ color: #6b7280; }}
nav.sidebar a.visited::before {{ content: "\\2713 "; color: #22c55e; }}
.progress-bar {{
  background: #f0f0f5; border-radius: 6px; height: 8px; margin: 0.5rem 0 1rem; overflow: hidden;
}}
.progress-fill {{ background: #4361ee; height: 100%; transition: width 0.3s; }}
.progress-text {{ font-size: 0.8rem; color: #666; margin-bottom: 0.5rem; }}
iframe {{
  flex: 1; border: none; height: 100vh;
}}
@media (max-width: 768px) {{
  body {{ flex-direction: column; }}
  nav.sidebar {{ width: 100%; height: auto; max-height: 40vh; }}
  iframe {{ height: 60vh; }}
}}
</style>
</head>
<body data-total-pages="{total_pages}">
<nav class="sidebar" id="sidebar">
  <h1>{title}</h1>
  <div class="progress-text" id="progress-text">0 / {total_pages} страниц</div>
  <div class="progress-bar"><div class="progress-fill" id="progress-fill" style="width:0%"></div></div>
  {toc}
</nav>
<iframe id="content-frame" src="about:blank"></iframe>
<script src="assets/scorm-api.js"></script>
<script>
(function() {{
  var frame = document.getElementById("content-frame");
  var links = document.querySelectorAll("nav.sidebar a[data-page-index]");
  var totalPages = {total_pages};

  function updateUI() {{
    var visited = SCORM ? SCORM.getVisited() : {{}};
    var count = 0;
    links.forEach(function(a) {{
      var idx = a.getAttribute("data-page-index");
      if (visited[idx]) {{
        a.classList.add("visited");
        count++;
      }}
    }});
    var pct = totalPages > 0 ? Math.round((count / totalPages) * 100) : 0;
    document.getElementById("progress-text").textContent = count + " / " + totalPages + " страниц (" + pct + "%)";
    document.getElementById("progress-fill").style.width = pct + "%";
  }}

  function setActive(pageIndex) {{
    links.forEach(function(a) {{
      if (a.getAttribute("data-page-index") === String(pageIndex)) {{
        a.classList.add("active");
        a.scrollIntoView({{block: "nearest"}});
      }} else {{
        a.classList.remove("active");
      }}
    }});
  }}

  links.forEach(function(a) {{
    a.addEventListener("click", function(e) {{
      e.preventDefault();
      frame.src = a.getAttribute("href");
      setActive(a.getAttribute("data-page-index"));
    }});
  }});

  if (SCORM) {{
    var origFn = SCORM.markVisited;
    SCORM.markVisited = function(idx) {{
      origFn(idx);
      updateUI();
    }};
  }}

  window.addEventListener("message", function(e) {{
    if (e.data && e.data.type === "scorm-page-visited" && SCORM) {{
      SCORM.markVisited(e.data.pageIndex);
    }}
    if (e.data && e.data.type === "scorm-page-loaded") {{
      setActive(e.data.pageIndex);
      if (SCORM) SCORM.setLocation(e.data.pageIndex);
    }}
  }});

  updateUI();
  var startIndex = 0;
  if (SCORM) {{
    var loc = SCORM.getLocation();
    if (loc) startIndex = parseInt(loc, 10) || 0;
  }}
  var startLink = document.querySelector('nav.sidebar a[data-page-index="' + startIndex + '"]');
  if (startLink) {{
    frame.src = startLink.getAttribute("href");
    setActive(startIndex);
  }} else if (links.length > 0) {{
    frame.src = links[0].getAttribute("href");
  }}
}})();
</script>
</body>
</html>
"""


def collect_pages() -> list[dict[str, str]]:
    pages: list[dict[str, str]] = []

    for f in sorted(COURSE_DIR.glob("*.md")):
        pages.append({
            "src": str(f),
            "module": "",
            "section": "",
            "filename": f.stem,
            "rel_html": f"{f.stem}.html",
            "title": extract_title(f),
        })

    for mod in MODULE_ORDER:
        mod_path = COURSE_DIR / mod
        if not mod_path.is_dir():
            continue

        for f in sorted(mod_path.glob("*.md")):
            pages.append({
                "src": str(f),
                "module": mod,
                "section": "",
                "filename": f.stem,
                "rel_html": f"{mod}/{f.stem}.html",
                "title": extract_title(f),
            })

        for section in SECTION_ORDER:
            sec_path = mod_path / section
            if not sec_path.is_dir():
                continue
            for f in sorted(sec_path.glob("*.md")):
                pages.append({
                    "src": str(f),
                    "module": mod,
                    "section": section,
                    "filename": f.stem,
                    "rel_html": f"{mod}/{section}/{f.stem}.html",
                    "title": extract_title(f),
                })

    return pages


def extract_file_index(md_file: Path) -> str:
    m = re.match(r'^(\d+)', md_file.stem)
    return m.group(1) if m else ""


def extract_title(md_file: Path) -> str:
    h1 = ""
    h2 = ""
    with open(md_file, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("## ") and not h2:
                h2 = line.removeprefix("## ").strip()
                h2 = re.sub(r'^\d+\.\s*', '', h2)
            elif line.startswith("# ") and not line.startswith("##") and not h1:
                h1 = line.removeprefix("# ").strip()

    module_prefix = re.match(r'^Модуль \d+:', h1)
    if module_prefix and h2:
        title = h2
    elif h1:
        title = re.sub(r'^Модуль \d+:\s*', '', h1)
    else:
        raw = md_file.stem
        raw = re.sub(r'^\d+-', '', raw)
        title = raw.replace("-", " ").strip().title()

    idx = extract_file_index(md_file)
    if idx:
        title = f"{idx}. {title}"
    return title


SVG_CACHE: dict[str, str] = {}


PUPPETEER_CONFIG: Path | None = None


def get_puppeteer_config() -> Path:
    global PUPPETEER_CONFIG
    if PUPPETEER_CONFIG is None:
        cfg = Path(tempfile.mktemp(suffix=".json"))
        cfg.write_text('{"args": ["--no-sandbox"]}', encoding="utf-8")
        PUPPETEER_CONFIG = cfg
    return PUPPETEER_CONFIG


def render_mermaid_svg(mermaid_code: str) -> str:
    cache_key = hashlib.md5(mermaid_code.encode()).hexdigest()
    if cache_key in SVG_CACHE:
        return SVG_CACHE[cache_key]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False, encoding="utf-8") as inp:
        inp.write(mermaid_code)
        inp_path = inp.name

    out_path = inp_path + ".svg"
    try:
        result = subprocess.run(
            ["npx", "@mermaid-js/mermaid-cli",
             "-i", inp_path, "-o", out_path, "-t", "neutral", "-q",
             "-p", str(get_puppeteer_config())],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and Path(out_path).exists():
            svg = Path(out_path).read_text(encoding="utf-8")
            svg = re.sub(r'<\?xml[^?]*\?>\s*', '', svg)
            svg = f'<div class="mermaid-diagram">{svg}</div>'
            SVG_CACHE[cache_key] = svg
            return svg
    except subprocess.TimeoutExpired:
        pass
    finally:
        Path(inp_path).unlink(missing_ok=True)
        Path(out_path).unlink(missing_ok=True)

    return f'<pre><code class="language-mermaid">{mermaid_code}</code></pre>'


def convert_md_to_html(md_file: Path) -> str:
    MERMAID_PLACEHOLDERS.clear()
    with open(md_file, encoding="utf-8") as fh:
        text = fh.read()

    text = re.sub(r'^\[← [^\]]*\]\([^)]*\)\s*', '', text)
    text = re.sub(r'\((?:\.\./)*README\.md\)', '({{INDEX_LINK}})', text)
    text = re.sub(r'\[([^\]]+)\]\((?!https?://)([^)]+)\.md\)', r'[\1](\2.html)', text)
    text = text.replace("yegge-8-levels.png", "yegge-8-levels.jpg")

    def replace_alert(m: re.Match[str]) -> str:
        alert_type = m.group(1).upper()
        inline_text = m.group(2).strip()
        body_lines = m.group(3)
        label = {"NOTE": "Примечание", "TIP": "Совет", "IMPORTANT": "Важно",
                 "WARNING": "Внимание", "CAUTION": "Осторожно"}.get(alert_type, alert_type)
        css_class = alert_type.lower()
        body = ""
        if inline_text:
            body += inline_text + "\n"
        if body_lines:
            body += re.sub(r'(?m)^> ?', '', body_lines)
        return f'<div class="alert alert-{css_class}" markdown="1">\n\n**{label}:** {body.strip()}\n\n</div>\n'

    text = re.sub(
        r'> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][ \t]*(.*)\n((?:>.*\n)*)',
        replace_alert, text, flags=re.IGNORECASE,
    )

    text = re.sub(r'(?m)(^(?:> )?[^\-\n].+)\n((?:> )?- )', r'\1\n\n\2', text)
    text = re.sub(r'(?m)(^[^\d\n].+)\n(\d+\. )', r'\1\n\n\2', text)

    def replace_mermaid(match: re.Match[str]) -> str:
        svg = render_mermaid_svg(match.group(1).strip())
        placeholder = f"MERMAID_PLACEHOLDER_{id(svg)}"
        MERMAID_PLACEHOLDERS[placeholder] = svg
        return placeholder

    text = re.sub(r'```mermaid\n(.*?)```', replace_mermaid, text, flags=re.DOTALL)

    text = text.replace("<details>", '<details markdown="1">')
    text = text.replace("<summary>", '<summary markdown="1">')

    md_converter = markdown.Markdown(extensions=[
        "tables",
        "fenced_code",
        "toc",
        "attr_list",
        "sane_lists",
        "md_in_html",
        "pymdownx.tasklist",
    ])
    html = md_converter.convert(text)

    for placeholder, svg in MERMAID_PLACEHOLDERS.items():
        html = html.replace(f"<p>{placeholder}</p>", svg)
        html = html.replace(placeholder, svg)

    html = re.sub(
        r'<a href="(https?://[^"]+)"',
        r'<a href="\1" target="_blank" rel="noopener noreferrer"',
        html,
    )
    html = html.replace(' disabled/>', '/>')

    return html


MERMAID_PLACEHOLDERS: dict[str, str] = {}


def compute_depth(rel_html: str) -> int:
    return rel_html.count("/")


def build_breadcrumb(page: dict[str, str]) -> str:
    depth = compute_depth(page["rel_html"])
    parts = ['<a href="{}index.html">Содержание</a>'.format("../" * depth)]
    if page["module"]:
        mod_title = MODULE_TITLES.get(page["module"], page["module"])
        first_page = find_first_page_in_module(page["module"])
        if first_page:
            mod_first_rel = f"{page['module']}/{first_page}"
            mod_link = "../" * depth + mod_first_rel
            parts.append(f'<a href="{mod_link}">{mod_title}</a>')
        else:
            parts.append(mod_title)
    return " → ".join(parts)


def find_first_page_in_module(mod: str) -> str:
    mod_path = COURSE_DIR / mod
    root_md = sorted(mod_path.glob("*.md"))
    if root_md:
        return root_md[0].stem + ".html"
    for section in SECTION_ORDER:
        sec_path = mod_path / section
        if sec_path.is_dir():
            files = sorted(sec_path.glob("*.md"))
            if files:
                return f"{section}/{files[0].stem}.html"
    return ""


def build_toc(pages: list[dict[str, str]]) -> str:
    lines: list[str] = []
    page_index_map: dict[str, int] = {p["rel_html"]: i for i, p in enumerate(pages)}

    def page_link(p: dict[str, str]) -> str:
        idx = page_index_map[p["rel_html"]]
        return f'<li><a href="{p["rel_html"]}" data-page-index="{idx}">{p["title"]}</a></li>'

    root_pages = [p for p in pages if not p["module"]]
    if root_pages:
        lines.append("<h2>Общее</h2><ul>")
        for p in root_pages:
            lines.append(page_link(p))
        lines.append("</ul>")

    for mod in MODULE_ORDER:
        mod_pages = [p for p in pages if p["module"] == mod]
        if not mod_pages:
            continue
        mod_title = MODULE_TITLES.get(mod, mod)
        lines.append(f"<h2>{mod_title}</h2>")

        mod_root = [p for p in mod_pages if not p["section"]]
        sections: dict[str, list[dict[str, str]]] = {}
        for p in mod_pages:
            if p["section"]:
                sections.setdefault(p["section"], []).append(p)

        if mod_root:
            lines.append("<ul>")
            for p in mod_root:
                lines.append(page_link(p))
            lines.append("</ul>")

        for sec in SECTION_ORDER:
            if sec not in sections:
                continue
            sec_title = SECTION_TITLES.get(sec, sec)
            lines.append(f"<h3>{sec_title}</h3><ul>")
            for p in sections[sec]:
                lines.append(page_link(p))
            lines.append("</ul>")

    return "\n".join(lines)


def build_manifest(pages: list[dict[str, str]]) -> str:
    manifest = Element("manifest", {
        "identifier": "mad-devs-ai-course",
        "version": "1.0",
        "xmlns": "http://www.imsproject.org/xsd/imscp_rootv1p1p2",
        "xmlns:adlcp": "http://www.adlnet.org/xsd/adlcp_rootv1p2",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation": (
            "http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd "
            "http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 imsmd_rootv1p2p1.xsd "
            "http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd"
        ),
    })

    metadata = SubElement(manifest, "metadata")
    SubElement(metadata, "schema").text = "ADL SCORM"
    SubElement(metadata, "schemaversion").text = "1.2"

    organizations = SubElement(manifest, "organizations", {"default": "org-1"})
    org = SubElement(organizations, "organization", {"identifier": "org-1"})
    SubElement(org, "title").text = COURSE_TITLE

    item = SubElement(org, "item", {
        "identifier": "item-course",
        "identifierref": "res-course",
        "isvisible": "true",
    })
    SubElement(item, "title").text = COURSE_TITLE

    resources = SubElement(manifest, "resources")

    res = SubElement(resources, "resource", {
        "identifier": "res-course",
        "type": "webcontent",
        "adlcp:scormtype": "sco",
        "href": "index.html",
    })
    SubElement(res, "file", {"href": "index.html"})
    for af in ["assets/style.css", "assets/scorm-api.js", "assets/page.js"]:
        SubElement(res, "file", {"href": af})
    for page in pages:
        SubElement(res, "file", {"href": page["rel_html"]})
    SubElement(res, "file", {"href": "module-1-why-ai/diagrams/yegge-8-levels.jpg"})

    raw = tostring(manifest, encoding="unicode")
    pretty = parseString(raw).toprettyxml(indent="  ", encoding=None)
    xml_lines = pretty.split("\n")
    return "\n".join(xml_lines[1:])


def compress_image(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    img = Image.open(src).convert("RGB")
    img.thumbnail((1200, 1200), Image.LANCZOS)
    img.save(dest, "JPEG", quality=70, optimize=True)


def main() -> None:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True)

    assets_dir = BUILD_DIR / "assets"
    assets_dir.mkdir()
    (assets_dir / "style.css").write_text(CSS, encoding="utf-8")
    (assets_dir / "scorm-api.js").write_text(SCORM_API_JS, encoding="utf-8")
    (assets_dir / "page.js").write_text(PAGE_JS, encoding="utf-8")

    img_src = COURSE_DIR / "module-1-why-ai" / "diagrams" / "yegge-8-levels.png"
    if img_src.exists():
        compress_image(img_src, BUILD_DIR / "module-1-why-ai" / "diagrams" / "yegge-8-levels.jpg")

    pages = collect_pages()
    print(f"Found {len(pages)} pages")

    for i, page in enumerate(pages):
        html_path = BUILD_DIR / page["rel_html"]
        html_path.parent.mkdir(parents=True, exist_ok=True)

        body = convert_md_to_html(Path(page["src"]))
        depth = compute_depth(page["rel_html"])
        prefix = "../" * depth if depth > 0 else ""
        index_link = f"{prefix}index.html"
        body = body.replace("{{INDEX_LINK}}", index_link)

        html = HTML_TEMPLATE.format(
            title=page["title"],
            body=body,
            page_index=i,
            css_path=f"{prefix}assets/style.css",
            page_js_path=f"{prefix}assets/page.js",
        )
        html_path.write_text(html, encoding="utf-8")

    total_pages = len(pages)
    toc_html = TOC_TEMPLATE.format(title=COURSE_TITLE, toc=build_toc(pages), total_pages=total_pages)
    (BUILD_DIR / "index.html").write_text(toc_html, encoding="utf-8")

    manifest_xml = build_manifest(pages)
    (BUILD_DIR / "imsmanifest.xml").write_text(manifest_xml, encoding="utf-8")

    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(BUILD_DIR):
            for fname in sorted(files):
                full = Path(root) / fname
                arcname = full.relative_to(BUILD_DIR)
                zf.write(full, arcname)

    size_kb = OUTPUT_ZIP.stat().st_size / 1024
    print(f"\nBuilt: {OUTPUT_ZIP.name} ({size_kb:.0f} KB)")
    print(f"Pages: {len(pages)}")


if __name__ == "__main__":
    main()
