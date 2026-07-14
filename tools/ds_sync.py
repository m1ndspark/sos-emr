#!/usr/bin/env python3
"""
ds_sync.py - Reconcile a Zoho Creator .ds (Application IDE export) against the
SOS repo's .dg files.

The .ds export (Settings > Application IDE > Export) is authoritative LIVE truth
and is definition-only (no record data, no PHI). This tool extracts every
workflow body and standalone function from the .ds and compares each against its
repo .dg file, reporting per item:
  MATCH     repo already equals live (comparison is whitespace-insensitive;
            Deluge nesting is expressed by braces, not indentation)
  DRIFT     repo differs from live in logic (repo stale or hand-edited)
  NEW       live workflow/function with no repo file yet
  EMPTY     export body blank -> NEVER written (protects the repo copy; some live
            bodies are genuinely empty, e.g. log_change / native-action stamps)
  AMBIGUOUS could not map to exactly one repo file, OR two live sources resolved
            to the SAME repo file (collision) -> never written, human review

Default is a dry-run report. --apply writes DRIFT and NEW targets only.
EMPTY and AMBIGUOUS are never auto-written, so a mis-map can't clobber a file.

Usage:
  python3 tools/ds_sync.py --ds SOS_Referrals_App.ds --repo .            # dry run
  python3 tools/ds_sync.py --ds SOS_Referrals_App.ds --repo . --apply    # write
"""
import argparse, os, re, glob
from collections import Counter

TRIGGER_PREFIX = {"on load": "OnLoad", "on success": "OnSuccess", "on validate": "OnValidate"}
NAME_RE = re.compile(r'^\t+([A-Za-z0-9_]+) as "([^"]*)"\s*$')
FN_SIG_RE = re.compile(r'^\s*(void|string|int|bigint|decimal|bool|boolean|map|list|collection|key|file|date|time|datetime)\s+([A-Za-z0-9_]+)\s*\((.*)\)\s*$')


def norm(body):
    # whitespace-insensitive: Deluge nesting is braces, not indent
    return "\n".join(l.strip() for l in body.split("\n") if l.strip())


def dedent(body_lines):
    ne = [b for b in body_lines if b.strip()]
    if not ne:
        return ""
    common = os.path.commonprefix([b[:len(b) - len(b.lstrip())] for b in ne])
    out = [(b[len(common):] if b.strip() else "") for b in body_lines]
    lines = "\n".join(out).strip("\n").split("\n")
    if lines and lines[0][:1] in ("\t", " "):
        lines[0] = lines[0].lstrip()
    return "\n".join(lines)


def parse_workflows(lines, wf_start):
    section = lines[wf_start:]
    out, cur, i = [], None, 0
    while i < len(section):
        l = section[i]
        m = NAME_RE.match(l)
        if m and i + 1 < len(section) and section[i + 1].strip() == "{":
            cur = {"name": m.group(1), "form": None, "ttype": None, "field": None, "body": None}
            out.append(cur)
        elif cur is not None:
            s = l.strip()
            if s.startswith("form ="):
                cur["form"] = s.split("=", 1)[1].strip()
            elif s.startswith("on user input of"):
                cur["ttype"] = "OnUserInput"; cur["field"] = s[len("on user input of"):].strip()
            elif s in TRIGGER_PREFIX:
                cur["ttype"] = TRIGGER_PREFIX[s]
            elif s == "custom deluge script":
                j = i + 1
                while j < len(section) and section[j].strip() != "(":
                    j += 1
                body, j = [], j + 1
                while j < len(section) and section[j].strip() != ")":
                    body.append(section[j]); j += 1
                cur["body"] = dedent(body); i = j
        i += 1
    return [w for w in out if w["form"] and w["ttype"]]


def parse_functions(lines):
    try:
        fstart = next(i for i, l in enumerate(lines) if l.strip() == "functions")
    except StopIteration:
        return []
    dstart = next(i for i in range(fstart, len(lines)) if lines[i].strip() == "Deluge")
    open_i = next(i for i in range(dstart, len(lines)) if lines[i].strip() == "{")
    text = "\n".join(lines[open_i:])
    buf, depth, started, in_str = [], 0, False, False
    for ci, ch in enumerate(text):
        if ch == '"' and (ci == 0 or text[ci - 1] != "\\"):
            in_str = not in_str
        if not in_str:
            if ch == "{":
                depth += 1; started = True
            elif ch == "}":
                depth -= 1
        buf.append(ch)
        if started and depth == 0:
            break
    block = "".join(buf)
    block = block[block.find("{") + 1: block.rfind("}")]
    blines = block.split("\n")
    fns, i = [], 0
    while i < len(blines):
        m = FN_SIG_RE.match(blines[i])
        if m:
            name = m.group(2)
            j = i + 1
            while j < len(blines) and blines[j].strip() != "{":
                j += 1
            d, in_s, body, started2, jj = 0, False, [], False, j
            while jj < len(blines):
                ln = blines[jj]
                for ci, ch in enumerate(ln):
                    if ch == '"' and (ci == 0 or ln[ci - 1] != "\\"):
                        in_s = not in_s
                    elif not in_s and ch == "{":
                        d += 1; started2 = True
                    elif not in_s and ch == "}":
                        d -= 1
                if started2 and jj > j:
                    body.append(ln)
                if started2 and d == 0:
                    break
                jj += 1
            inner = body[:-1] if body and body[-1].strip() == "}" else body
            fns.append({"name": name, "body": dedent(inner)})
            i = jj + 1; continue
        i += 1
    return fns


def resolve_wf_path(repo, w):
    d = os.path.join(repo, w["form"])
    prefix = f"{w['ttype']}__{w['field']}__" if w["field"] else f"{w['ttype']}__"
    matches = sorted(glob.glob(os.path.join(d, prefix + "*.dg")))
    if len(matches) == 1:
        return matches[0], "resolved"
    if len(matches) == 0:
        return os.path.join(d, f"{prefix}{w['name']}.dg"), "new"
    toks = [re.sub(r"\d+$", "", t).lower() for t in re.split(r"[_ ]", w["name"])]
    toks = [t for t in toks if len(t) >= 2]
    scored = sorted(((sum(1 for t in toks if t in os.path.basename(m).lower()), m) for m in matches), reverse=True)
    if scored and scored[0][0] > 0 and (len(scored) == 1 or scored[0][0] > scored[1][0]):
        return scored[0][1], "resolved"
    return None, "ambiguous"


def classify(path, body, apply):
    if body is None or body.strip() == "":
        return "EMPTY", None
    if not (path and os.path.exists(path)):
        return "NEW", (path if apply else None)
    if norm(open(path, encoding="utf-8").read()) == norm(body):
        return "MATCH", None
    return "DRIFT", (path if apply else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    lines = open(a.ds, encoding="utf-8", errors="replace").read().split("\n")
    wf_start = next(i for i, l in enumerate(lines) if l.strip() == "workflow")
    wfs = parse_workflows(lines, wf_start)
    fns = parse_functions(lines)

    # pass 1: resolve; pass 2: flag any target claimed by >1 source (collision)
    resolved = []
    for w in wfs:
        path, how = resolve_wf_path(a.repo, w)
        resolved.append((None if how == "ambiguous" else path, w["body"], w["name"], w))
    claims = Counter(p for p, _, _, _ in resolved if p)
    collided = {p for p, c in claims.items() if c > 1}

    rows, written = [], 0
    for path, body, name, w in resolved:
        if path is None or path in collided:
            lbl = f"{w['form']}/{w['ttype']} {name}" if path is None else f"{os.path.relpath(path, a.repo)} <- {name}"
            rows.append(("AMBIGUOUS", lbl, "")); continue
        st, wr = classify(path, body, a.apply)
        rows.append((st, os.path.relpath(path, a.repo), name))
        if wr:
            os.makedirs(os.path.dirname(wr), exist_ok=True)
            open(wr, "w", encoding="utf-8").write(body + "\n"); written += 1

    for f in fns:
        path = os.path.join(a.repo, "functions", f["name"] + ".dg")
        st, wr = classify(path, f["body"], a.apply)
        rows.append((st, os.path.relpath(path, a.repo), f["name"]))
        if wr:
            os.makedirs(os.path.dirname(wr), exist_ok=True)
            open(wr, "w", encoding="utf-8").write(f["body"] + "\n"); written += 1

    order = {"DRIFT": 0, "NEW": 1, "EMPTY": 2, "AMBIGUOUS": 3, "MATCH": 4}
    rows.sort(key=lambda r: (order.get(r[0], 9), r[1]))
    print(f"\nParsed {len(wfs)} workflows, {len(fns)} functions from {os.path.basename(a.ds)}")
    print(f"{'STATUS':10} {'FILE':62} SOURCE")
    print("-" * 100)
    for st, rel, name in rows:
        print(f"{st:10} {rel:62} {name}")
    c = Counter(r[0] for r in rows)
    print("-" * 100)
    print("summary:", ", ".join(f"{k}={v}" for k, v in sorted(c.items())))
    print(f"WROTE {written} files." if a.apply else "dry-run (no files written). add --apply to write DRIFT + NEW.")


if __name__ == "__main__":
    main()
