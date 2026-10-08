#!/usr/bin/env python3
"""
Jenkins Change Report Generator
Builds a self-contained HTML (no JS, inline CSS) + JSON report showing what
changed in this build compared to the last successful build.

Uses standard Jenkins/Git-plugin env vars:
  GIT_COMMIT, GIT_PREVIOUS_SUCCESSFUL_COMMIT, JOB_NAME, BUILD_NUMBER,
  BUILD_URL, BRANCH_NAME / GIT_BRANCH, BUILD_STATUS (set by the Jenkinsfile)
"""
import datetime
import html
import json
import os
import subprocess
from pathlib import Path

EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
MAX_DIFF_LINES = 400  # per file, keeps the report readable
OUT_DIR = Path(os.environ.get("REPORT_DIR", "reports"))


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def commit_exists(ref):
    return subprocess.run(
        ["git", "cat-file", "-e", f"{ref}^{{commit}}"],
        capture_output=True,
    ).returncode == 0


def resolve_range():
    head = (os.environ.get("GIT_COMMIT") or git("rev-parse", "HEAD")).strip()
    base = (os.environ.get("GIT_PREVIOUS_SUCCESSFUL_COMMIT") or "").strip()
    if not base or base == head or not commit_exists(base):
        parent = git("rev-parse", f"{head}~1").strip()
        base = parent if parent else EMPTY_TREE
    return base, head


def get_commits(base, head):
    fmt = "%H%x1f%an%x1f%ae%x1f%aI%x1f%s%x1e"
    out = git("log", f"--pretty=format:{fmt}", f"{base}..{head}")
    commits = []
    for rec in out.split("\x1e"):
        rec = rec.strip()
        if not rec:
            continue
        h, an, ae, date, subj = rec.split("\x1f")
        commits.append({"hash": h, "short": h[:7], "author": an,
                        "email": ae, "date": date, "subject": subj})
    return commits


def get_files(base, head):
    status = {}
    for line in git("diff", "--no-renames", "--name-status", base, head).splitlines():
        s, _, path = line.partition("\t")
        status[path] = {"A": "added", "M": "modified", "D": "deleted"}.get(s[:1], s)
    files = []
    for line in git("diff", "--no-renames", "--numstat", base, head).splitlines():
        add, dele, path = line.split("\t", 2)
        binary = add == "-"
        files.append({
            "path": path,
            "status": status.get(path, "modified"),
            "added": 0 if binary else int(add),
            "deleted": 0 if binary else int(dele),
            "binary": binary,
        })
    return files


def get_diff(base, head, path):
    lines = git("diff", "--no-renames", base, head, "--", path).splitlines()
    truncated = len(lines) > MAX_DIFF_LINES
    return lines[:MAX_DIFF_LINES], truncated


def line_class(line):
    if line.startswith("+++") or line.startswith("---"):
        return "meta"
    if line.startswith("@@"):
        return "hunk"
    if line.startswith("+"):
        return "add"
    if line.startswith("-"):
        return "del"
    return "ctx"


CSS = """
:root{--bg:#fff;--fg:#1f2328;--muted:#656d76;--card:#f6f8fa;--bd:#d0d7de;
--add:#e6ffec;--del:#ffebe9;--hunk:#ddf4ff;--ok:#1a7f37;--bad:#cf222e;--warn:#9a6700}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--muted:#8d96a0;
--card:#161b22;--bd:#30363d;--add:#12261e;--del:#2d1214;--hunk:#0c2d4a;--ok:#3fb950;--bad:#f85149;--warn:#d29922}}
*{box-sizing:border-box}
body{margin:0;padding:24px;background:var(--bg);color:var(--fg);
font:14px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif}
.wrap{max-width:1000px;margin:0 auto}
h1{font-size:22px;margin:0 0 4px}h2{font-size:16px;margin:28px 0 10px}
.muted{color:var(--muted)}
.badge{display:inline-block;padding:2px 10px;border-radius:12px;font-weight:600;font-size:12px;color:#fff}
.SUCCESS{background:var(--ok)}.FAILURE{background:var(--bad)}.UNSTABLE,.UNKNOWN{background:var(--warn)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:16px 0}
.card{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:12px}
.card b{display:block;font-size:22px}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--bd)}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--bd);vertical-align:top}
th{font-size:12px;color:var(--muted);text-transform:uppercase}
code,pre{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
.plus{color:var(--ok)}.minus{color:var(--bad)}
.tag{font-size:11px;padding:1px 7px;border-radius:10px;border:1px solid var(--bd)}
.added{color:var(--ok)}.deleted{color:var(--bad)}
details{border:1px solid var(--bd);border-radius:8px;margin:8px 0;background:var(--card)}
summary{cursor:pointer;padding:8px 12px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px}
pre{margin:0;padding:0;overflow-x:auto;background:var(--bg)}
pre span{display:block;padding:0 12px;white-space:pre}
.add{background:var(--add)}.del{background:var(--del)}.hunk{background:var(--hunk);color:var(--muted)}
.meta{color:var(--muted)}
"""


def render(d):
    e = html.escape
    s = d["summary"]
    status = e(d["status"])
    parts = [f"<!doctype html><html><head><meta charset='utf-8'>"
             f"<title>Change Report - {e(d['job'])} #{e(d['build'])}</title>"
             f"<style>{CSS}</style></head><body><div class='wrap'>"]

    link = f"<a href='{e(d['build_url'])}'>#{e(d['build'])}</a>" if d["build_url"] else f"#{e(d['build'])}"
    parts.append(
        f"<h1>{e(d['job'])} {link} <span class='badge {status}'>{status}</span></h1>"
        f"<div class='muted'>Branch <code>{e(d['branch'])}</code> &middot; "
        f"<code>{e(d['base'][:7])}</code> &rarr; <code>{e(d['head'][:7])}</code> &middot; "
        f"generated {e(d['generated'])}</div>")

    parts.append(
        "<div class='grid'>"
        f"<div class='card'><b>{s['commits']}</b><span class='muted'>commits</span></div>"
        f"<div class='card'><b>{s['files']}</b><span class='muted'>files changed</span></div>"
        f"<div class='card'><b class='plus'>+{s['added']}</b><span class='muted'>lines added</span></div>"
        f"<div class='card'><b class='minus'>-{s['deleted']}</b><span class='muted'>lines removed</span></div>"
        f"<div class='card'><b>{s['authors']}</b><span class='muted'>authors</span></div></div>")

    parts.append("<h2>Commits</h2>")
    if d["commits"]:
        parts.append("<table><tr><th>Hash</th><th>Author</th><th>Date</th><th>Message</th></tr>")
        for c in d["commits"]:
            parts.append(f"<tr><td><code>{e(c['short'])}</code></td><td>{e(c['author'])}</td>"
                         f"<td class='muted'>{e(c['date'][:16].replace('T', ' '))}</td>"
                         f"<td>{e(c['subject'])}</td></tr>")
        parts.append("</table>")
    else:
        parts.append("<p class='muted'>No new commits since the last successful build.</p>")

    parts.append("<h2>Files changed</h2>")
    if d["files"]:
        parts.append("<table><tr><th>File</th><th>Status</th><th>Changes</th></tr>")
        for f in d["files"]:
            ch = "binary" if f["binary"] else (
                f"<span class='plus'>+{f['added']}</span> <span class='minus'>-{f['deleted']}</span>")
            parts.append(f"<tr><td><code>{e(f['path'])}</code></td>"
                         f"<td><span class='tag {e(f['status'])}'>{e(f['status'])}</span></td>"
                         f"<td>{ch}</td></tr>")
        parts.append("</table>")

        parts.append("<h2>Diffs</h2>")
        for f in d["files"]:
            if f["binary"]:
                continue
            body = "".join(f"<span class='{line_class(l)}'>{e(l) or ' '}</span>"
                           for l in f["diff"])
            note = "<span class='muted'> (truncated)</span>" if f["truncated"] else ""
            parts.append(f"<details><summary>{e(f['path'])}{note}</summary><pre>{body}</pre></details>")
    else:
        parts.append("<p class='muted'>No file changes.</p>")

    parts.append("</div></body></html>")
    return "".join(parts)


def main():
    base, head = resolve_range()
    commits = get_commits(base, head)
    files = get_files(base, head)
    for f in files:
        f["diff"], f["truncated"] = ([], False) if f["binary"] else get_diff(base, head, f["path"])

    data = {
        "job": os.environ.get("JOB_NAME", "local-run"),
        "build": os.environ.get("BUILD_NUMBER", "0"),
        "build_url": os.environ.get("BUILD_URL", ""),
        "branch": os.environ.get("BRANCH_NAME") or os.environ.get("GIT_BRANCH", "unknown"),
        "status": os.environ.get("BUILD_STATUS", "UNKNOWN"),
        "base": base,
        "head": head,
        "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "commits": commits,
        "files": files,
        "summary": {
            "commits": len(commits),
            "files": len(files),
            "added": sum(f["added"] for f in files),
            "deleted": sum(f["deleted"] for f in files),
            "authors": len({c["email"] for c in commits}),
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "change_report.html").write_text(render(data), encoding="utf-8")
    slim = {**data, "files": [{k: v for k, v in f.items() if k not in ("diff",)} for f in files]}
    (OUT_DIR / "change_report.json").write_text(json.dumps(slim, indent=2), encoding="utf-8")

    s = data["summary"]
    print(f"Change report written to {OUT_DIR}/ "
          f"({s['commits']} commits, {s['files']} files, +{s['added']}/-{s['deleted']})")
    # one-line summary for Jenkins build description
    (OUT_DIR / "summary.txt").write_text(
        f"{s['commits']} commit(s), {s['files']} file(s), +{s['added']}/-{s['deleted']}")


if __name__ == "__main__":
    main()
