#!/usr/bin/env python3
"""
ds_sync.py - Reconcile a Zoho Creator .ds (Application IDE export) against the
SOS repo's .dg files, and optionally emit a compact navigation manifest.

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

--manifest writes MANIFEST.tsv (repo root): one row per workflow/function with
its file, name, form, trigger, field, and a content hash, plus best-effort
relationship columns (calls / writes / reads / fetches / integrations). The
relationship columns are a NAVIGATION AID derived by regex over each body; they
are not an authoritative logic model. calls and fetches are matched against known
function and form names (reliable); writes/reads track input.<field> assignments
and references (heuristic). Open the .dg for ground truth before editing.

Usage:
  python3 tools/ds_sync.py --ds SOS_Referrals_App.ds --repo .            # dry run
  python3 tools/ds_sync.py --ds SOS_Referrals_App.ds --repo . --apply    # write
  python3 tools/ds_sync.py --ds SOS_Referrals_App.ds --repo . --manifest # + MANIFEST.tsv
  python3 tools/ds_sync.py --ds SOS_Referrals_App.ds --repo . --manifest --map

--map writes context/ds_map/ (relationship index: _index.md, forms/<Form>.md,
functions.md, unresolved.md, changes.md, map.json). It parses only
SOS_Referrals_App.ds, verifies its counts against independent line counts of the
.ds, and writes nothing (exit 3) on a mismatch. It runs before --manifest, so a
failed map also leaves MANIFEST.tsv untouched. Output is deterministic.
"""
import argparse, os, re, glob, hashlib
from collections import Counter

TRIGGER_PREFIX = {"on load": "OnLoad", "on success": "OnSuccess", "on validate": "OnValidate"}
NAME_RE = re.compile(r'^\t+([A-Za-z0-9_]+) as "([^"]*)"\s*$')
FN_SIG_RE = re.compile(r'^\s*(void|string|int|bigint|decimal|bool|boolean|map|list|collection|key|file|date|time|datetime)\s+([A-Za-z0-9_]+)\s*\((.*)\)\s*$')

CALL_RE = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\(')
ASSIGN_RE = re.compile(r'\binput\.([A-Za-z0-9_]+)\s*=(?!=)')
INPUT_RE = re.compile(r'\binput\.([A-Za-z0-9_]+)')
UI_RE = re.compile(r'\b(?:disable|enable|hide|show)\s+([A-Za-z0-9_]+)')
FETCH_RE = re.compile(r'\b([A-Za-z][A-Za-z0-9_]+)\s*\[')
INTEG_KEYS = [("zoho.books", "Books"), ("books.", "Books"), ("twilio", "Twilio"),
              ("transcribe", "AWS-Transcribe"), ("bedrock", "AWS-Bedrock"),
              ("srfax", "SRFax"), ("sendmail", "Email"), ("invokeurl", "HTTP"),
              ("geturl", "HTTP"), ("posturl", "HTTP"), ("zoho.crm", "CRM"),
              ("creator/custom", "CustomAPI"), ("thisapp.", "AppFunc")]


def norm(body):
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


def parse_workflows(lines, wf_start, keep_all=False):
    # keep_all=True (used by --map only) also returns button workflows,
    # schedules and report custom actions with their header metadata and raw
    # action text. The default return set is unchanged.
    section = lines[wf_start:]
    out, cur, i, sec = [], None, 0, None
    while i < len(section):
        l = section[i]
        if keep_all and i > 0 and re.match(r'^\t[a-z_]+\s*$', l):
            break
        sm = re.match(r'^\t\t([a-z]+)\s*$', l)
        if sm:
            sec = sm.group(1)
        m = NAME_RE.match(l)
        if m and i + 1 < len(section) and section[i + 1].strip() == "{":
            cur = {"name": m.group(1), "form": None, "ttype": None, "field": None, "body": None,
                   "display": m.group(2), "line": wf_start + i + 1, "section": sec, "kind": None,
                   "record_event": None, "status": "active", "button": None, "click": False,
                   "start": None, "frequency": None, "exec_type": None, "action": None}
            out.append(cur)
        elif cur is not None:
            s = l.strip()
            if s.startswith("form ="):
                cur["form"] = s.split("=", 1)[1].strip()
            elif s.startswith("on user input of"):
                cur["ttype"] = "OnUserInput"; cur["field"] = s[len("on user input of"):].strip()
            elif s in TRIGGER_PREFIX:
                cur["ttype"] = TRIGGER_PREFIX[s]
                if keep_all and cur["action"] is None and i + 1 < len(section) and section[i + 1].strip() == "(":
                    i = _raw_action(section, i, cur, wf_start)
            elif s == "custom deluge script":
                j = i + 1
                while j < len(section) and section[j].strip() != "(":
                    j += 1
                body, j = [], j + 1
                b0 = j
                while j < len(section) and section[j].strip() != ")":
                    body.append(section[j]); j += 1
                cur["body"] = dedent(body); i = j
                cur["body_line"] = wf_start + b0 + 1 + next((k for k, b in enumerate(body) if b.strip()), 0)
            elif s.startswith("type ="):
                cur["kind"] = s.split("=", 1)[1].strip()
            elif s.startswith("record event ="):
                cur["record_event"] = s.split("=", 1)[1].strip()
            elif s.startswith("status ="):
                cur["status"] = s.split("=", 1)[1].strip()
            elif s.startswith("button ="):
                cur["button"] = s.split("=", 1)[1].strip()
            elif s.startswith("start ="):
                cur["start"] = s.split("=", 1)[1].strip()
            elif s.startswith("frequency ="):
                cur["frequency"] = s.split("=", 1)[1].strip()
            elif s.startswith("execution type ="):
                cur["exec_type"] = s.split("=", 1)[1].strip()
            elif s == "on click":
                cur["click"] = True
                if keep_all and cur["action"] is None and i + 1 < len(section) and section[i + 1].strip() == "(":
                    i = _raw_action(section, i, cur, wf_start)
        i += 1
    if keep_all:
        return [w for w in out if w["form"] or w["kind"]]
    return [w for w in out if w["form"] and w["ttype"]]


def _raw_action(section, i, cur, wf_start):
    j, body = i + 2, []
    while j < len(section) and section[j].strip() != ")":
        body.append(section[j]); j += 1
    cur["action"] = dedent(body)
    cur["body_line"] = wf_start + i + 3 + next((k for k, b in enumerate(body) if b.strip()), 0)
    return j


def parse_functions(lines):
    try:
        fstart = next(i for i, l in enumerate(lines) if l.strip() == "functions")
    except StopIteration:
        return []
    dstart = next(i for i in range(fstart, len(lines)) if lines[i].strip() == "Deluge")
    namespace = lines[dstart].strip()
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
            fns.append({"name": name, "body": dedent(inner), "rtype": m.group(1),
                        "args": m.group(3).strip(), "namespace": namespace})
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


def body_hash(body):
    return hashlib.sha1(norm(body or "").encode("utf-8")).hexdigest()[:8]


def edges(body, known_fns, known_forms):
    body = body or ""
    writes = set(ASSIGN_RE.findall(body)) | set(UI_RE.findall(body))
    reads = set(INPUT_RE.findall(body)) - writes
    calls = {m for m in CALL_RE.findall(body) if m in known_fns}
    fetches = {f for f in FETCH_RE.findall(body) if f in known_forms}
    low = body.lower()
    integ = {label for key, label in INTEG_KEYS if key in low}
    return sorted(calls), sorted(writes), sorted(reads), sorted(fetches), sorted(integ)


def write_manifest(repo, resolved, fns, known_fns, known_forms):
    cols = ["file", "name", "form", "trigger", "field", "calls", "writes", "reads", "fetches", "integrations", "hash"]
    rows = []
    for path, body, name, w in resolved:
        rel = os.path.relpath(path, repo) if path else f"{w['form']}/?__{name}.dg"
        c, wr, rd, fe, ig = edges(body, known_fns, known_forms)
        rows.append([rel, name, w["form"], w["ttype"], w["field"] or "",
                     ";".join(c), ";".join(wr), ";".join(rd), ";".join(fe), ";".join(ig), body_hash(body)])
    for f in fns:
        rel = os.path.join("functions", f["name"] + ".dg")
        c, wr, rd, fe, ig = edges(f["body"], known_fns, known_forms)
        rows.append([rel, f["name"], "", "function", "",
                     ";".join(c), ";".join(wr), ";".join(rd), ";".join(fe), ";".join(ig), body_hash(f["body"])])
    rows.sort(key=lambda r: (r[2], r[0]))
    out = os.path.join(repo, "MANIFEST.tsv")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")
    return out, len(rows)


# ---------------------------------------------------------------------------
# --map: relationship index written to context/ds_map/ (navigation aid).
# Reuses parse_workflows / parse_functions / edges above. Everything here is
# derived from SOS_Referrals_App.ds only and is written deterministically.
# ---------------------------------------------------------------------------
MAP_DS_NAME = "SOS_Referrals_App.ds"
MAP_DIR = os.path.join("context", "ds_map")
SYS_FIELDS = {"ID", "Added_Time", "Modified_Time", "Added_User", "Modified_User",
              "Added_User_IPAddress", "Modified_User_IPAddress"}
KNOWN_FIELD_TYPES = {"text", "textarea", "email", "phonenumber", "number", "decimal", "USD",
                     "date", "datetime", "picklist", "radiobuttons", "checkboxes", "checkbox",
                     "list", "upload file", "richtext", "plaintext", "section", "address"}
FIELD_HEAD_RE = re.compile(r'^\t{3}((?:must have |unique )*)([A-Za-z0-9_]+)\s*$')
LOOKUP_RE = re.compile(r'^values\s*=\s*([A-Za-z0-9_]+)\.ID\s*$')
REPORT_HEAD_RE = re.compile(r'^\t\t(?:(default)\s+)?([a-z]+)\s+([A-Za-z0-9_]+)\s*$')
SECRET_RE = re.compile(r'ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bpar]-[A-Za-z0-9-]{10,}|Bearer [A-Za-z0-9._-]{20,}|eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}')
SSN_RE = re.compile(r'(^|[^0-9])[0-9]{3}-[0-9]{2}-[0-9]{4}([^0-9]|$)')


def _section_bounds(lines, name, tabs, start=0):
    pat = re.compile(r'^ ?' + '\t' * tabs + r' ?' + name + r'\s*$')
    s = next(i for i in range(start, len(lines)) if pat.match(lines[i]))
    e = next((i for i in range(s + 1, len(lines)) if re.match(r'^\t[a-z_]+\s*$', lines[i])), len(lines))
    return s, e


def parse_forms(lines):
    s, e = _section_bounds(lines, "forms", 1)
    forms, cur, i = {}, None, s
    while i < e:
        l = lines[i]
        m = re.match(r'^\t\tform ([A-Za-z0-9_]+)\s*$', l)
        if m:
            cur = {"name": m.group(1), "display": "", "fields": [], "line": i + 1}
            forms[cur["name"]] = cur
        elif cur is not None:
            st = l.strip()
            if re.match(r'^\t{3}displayname\s*=', l) and not cur["display"]:
                cur["display"] = st.split("=", 1)[1].strip().strip('"')
            fm = FIELD_HEAD_RE.match(l)
            if fm and i + 1 < e and lines[i + 1].strip() == "(":
                f = {"name": fm.group(2), "display": "", "type": None, "lookup": None,
                     "mandatory": "must have" in fm.group(1), "unique": "unique" in fm.group(1)}
                j = i + 2
                while j < e and not re.match(r'^\t{3}\)\s*$', lines[j]):
                    t = lines[j].strip()
                    if f["type"] is None and re.match(r'^type\s*=', t):
                        f["type"] = t.split("=", 1)[1].strip()
                    elif not f["display"] and re.match(r'^displayname\s*=', t):
                        f["display"] = t.split("=", 1)[1].strip().strip('"')
                    else:
                        lm = LOOKUP_RE.match(t)
                        if lm and f["lookup"] is None:
                            f["lookup"] = lm.group(1)
                    j += 1
                cur["fields"].append(f)
                i = j
        i += 1
    return forms


def parse_reports(lines):
    s, e = _section_bounds(lines, "reports", 1)
    reps, cur, ca = {}, None, None
    for i in range(s, e):
        l = lines[i]
        m = REPORT_HEAD_RE.match(l)
        if m and i + 1 < e and lines[i + 1].strip() == "{":
            cur = {"name": m.group(3), "type": m.group(2), "default": bool(m.group(1)),
                   "display": "", "form": None, "criteria": "", "actions": [], "line": i + 1}
            reps[cur["name"]] = cur
            continue
        if cur is None:
            continue
        st = l.strip()
        if st.startswith("displayName") and not cur["display"]:
            cur["display"] = st.split("=", 1)[1].strip().strip('"')
        sm = re.match(r'^show (?:all )?rows from\s+([A-Za-z0-9_]+)\s*(.*)$', st)
        if sm and cur["form"] is None:
            cur["form"] = sm.group(1); cur["criteria"] = sm.group(2).strip()
        am = re.match(r'^custom action\s+"([^"]*)"', st)
        if am:
            ca = {"label": am.group(1), "workflow": None, "line": i + 1}
            cur["actions"].append(ca)
        wm = re.match(r'^workflow\s*=\s*([A-Za-z0-9_]+)', st)
        if wm and ca is not None and ca["workflow"] is None:
            ca["workflow"] = wm.group(1)
    return reps


def _unescape_content(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            out.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\", "r": ""}.get(n, "\\" + n)); i += 2
            continue
        out.append(c); i += 1
    import html
    return html.unescape("".join(out))


def parse_pages(lines):
    s, e = _section_bounds(lines, "pages", 1)
    pages, cur = {}, None
    for i in range(s, e):
        l = lines[i]
        m = re.match(r'^\t\tpage ([A-Za-z0-9_]+)\s*(?:\((.*)\))?\s*$', l)
        if m:
            cur = {"name": m.group(1), "params": (m.group(2) or "").strip(), "display": "",
                   "content": "", "line": i + 1}
            pages[cur["name"]] = cur
            continue
        if cur is None:
            continue
        st = l.strip()
        if st.startswith("displayname") and not cur["display"]:
            cur["display"] = st.split("=", 1)[1].strip().strip('"')
        cm = re.match(r'^Content="(.*)"\s*$', st)
        if cm:
            cur["content"] = _unescape_content(cm.group(1))
    return pages


def ds_counts(lines):
    """Independent line-pattern counts straight off the .ds, used to verify the map."""
    fs, fe = _section_bounds(lines, "forms", 1)
    rs, re_ = _section_bounds(lines, "reports", 1)
    ps, pe = _section_bounds(lines, "pages", 1)
    ws = next(i for i, l in enumerate(lines) if l.strip() == "workflow")
    we = next((i for i in range(ws + 1, len(lines)) if re.match(r'^\t[a-z_]+\s*$', lines[i])), len(lines))
    fn_s = next(i for i, l in enumerate(lines) if l.strip() == "functions")
    blocks = sum(1 for l in lines[fs:fe] if re.match(r'^\t{3}\)\s*$', l))
    sections = sum(1 for l in lines[fs:fe] if re.match(r'^\t{4}type = section\s*$', l))
    wf_types = Counter(re.sub(r'\s+', ' ', l.strip()) for l in lines[ws:we] if re.match(r'^\t{4}type =', l))
    return {
        "forms": sum(1 for l in lines[fs:fe] if re.match(r'^\t\tform [A-Za-z0-9_]+\s*$', l)),
        "fields": blocks - sections,
        "workflows": wf_types.get("type = form", 0),
        "inactive_workflows": sum(1 for l in lines[ws:we] if l.strip() == "status = inactive"),
        "functions": sum(1 for l in lines[fn_s:ws] if re.match(r'^\t{4} [a-z]+ [A-Za-z0-9_]+\s*\(', l)),
        "schedules": wf_types.get("type = schedule", 0),
        "batch_workflows": wf_types.get("type = batch", 0),
        "approval_workflows": wf_types.get("type = approval", 0),
        "report_actions_wf": wf_types.get("type = functions", 0),
        "reports": sum(1 for l in lines[rs:re_] if re.match(r'^\t{3}show (?:all )?rows from', l)),
        "pages": sum(1 for l in lines[ps:pe] if re.match(r'^\t\tpage ', l)),
    }


def _strip_comments(code):
    out, i, n, q = [], 0, len(code), False
    while i < n:
        c = code[i]
        if q:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(code[i + 1]); i += 2; continue
            if c == '"':
                q = False
            i += 1; continue
        if c == '"':
            q = True; out.append(c); i += 1; continue
        if code.startswith("//", i):
            while i < n and code[i] != "\n":
                i += 1
            continue
        if code.startswith("/*", i):
            j = code.find("*/", i + 2); j = n if j < 0 else j + 2
            out.append("".join("\n" if ch == "\n" else " " for ch in code[i:j])); i = j; continue
        out.append(c); i += 1
    return "".join(out)


def _blank_strings(code):
    out, q, i = [], False, 0
    while i < len(code):
        c = code[i]
        if q:
            if c == "\\" and i + 1 < len(code):
                out.append("  "); i += 2; continue
            if c == '"':
                q = False; out.append(c)
            else:
                out.append("\n" if c == "\n" else " ")
            i += 1; continue
        if c == '"':
            q = True
        out.append(c); i += 1
    return "".join(out)


def _close(text, i, o="[", c="]"):
    d = 0
    for k in range(i, len(text)):
        if text[k] == o:
            d += 1
        elif text[k] == c:
            d -= 1
            if d == 0:
                return k
    return len(text) - 1


def _snip(code, pos):
    a = code.rfind("\n", 0, pos) + 1
    b = code.find("\n", pos); b = len(code) if b < 0 else b
    t = re.sub(r'\s+', ' ', code[a:b]).strip()
    t = SECRET_RE.sub("[redacted]", t)
    t = SSN_RE.sub(r"\1[redacted]\2", t)
    t = t.replace("|", "\\|").replace("`", "'")
    return t[:140] + (" ..." if len(t) > 140 else "")


CRIT_ID_RE = re.compile(r'(?<![\w.])([A-Za-z_]\w*)\s*(?:==|!=|>=|<=|<|>|\.contains\s*\(|\.startsWith\s*\(|\.endsWith\s*\(|\s+in\s|\s+not\s+in\s)')
DELUGE_WORDS = {"null", "true", "false", "zoho", "input", "and", "or", "not", "in", "if", "else"}


def analyze(body, own_form, forms, fn_names, report_names, page_names, params=(), deluge=True):
    """Resolve references in one body against the known model. Returns a dict."""
    r = {"fetch": {}, "insert": {}, "update": {}, "delete": {}, "read": {},
         "in_read": set(), "in_set": set(), "in_ui": set(), "calls": set(),
         "opens": set(), "unresolved": []}
    if not body:
        return r
    code = _strip_comments(body)
    ns = _blank_strings(code)
    line_of = lambda p: code.count("\n", 0, p) + 1
    unres = lambda p, kind, what: r["unresolved"].append((line_of(p), kind, what, _snip(code, p)))
    fieldset = {k: {f["name"] for f in v["fields"]} for k, v in forms.items()}
    lookups = {k: {f["name"]: f["lookup"] for f in v["fields"] if f["lookup"]} for k, v in forms.items()}
    add = lambda op, form, fld: r[op].setdefault(form, set()).update([fld] if fld else [])

    def crit_fields(form, a, b):
        inner = ns[a + 1:b]
        if re.fullmatch(r'\s*[A-Za-z_]\w*\s*', inner) and inner.strip() not in fieldset.get(form, ()):
            unres(a, "dynamic criteria", f"{form}[{inner.strip()}]")
            return set()
        got = set()
        for m in CRIT_ID_RE.finditer(inner):
            x = m.group(1)
            if x in fieldset.get(form, ()) or x in SYS_FIELDS:
                got.add(x)
            elif x in assigned or x in params or x in DELUGE_WORDS:
                continue
            else:
                unres(a + 1 + m.start(1), "criteria field not on form", f"{form}.{x}")
        return got

    assigned = set(re.findall(r'(?<![\w.])([A-Za-z_]\w*)\s*=(?!=)', ns))
    assigned |= set(re.findall(r'for each\s+([A-Za-z_]\w*)\s+in\b', ns))
    assigned |= set(params)
    bind, bad = {}, set()

    def do_bind(v, f):
        if v in bind and bind[v] != f:
            bad.add(v)
        bind[v] = f

    for m in re.finditer(r'(?<![\w.])([A-Za-z_]\w*)\s*=(?!=)\s*([A-Za-z_]\w*)\s*\[', ns):
        if m.group(2) in forms:
            do_bind(m.group(1), m.group(2))
    for m in re.finditer(r'for each\s+([A-Za-z_]\w*)\s+in\s+([A-Za-z_]\w*)\s*\[', ns):
        if m.group(2) in forms:
            do_bind(m.group(1), m.group(2))
    for _ in range(3):
        for m in re.finditer(r'for each\s+([A-Za-z_]\w*)\s+in\s+([A-Za-z_]\w*)\b(?!\s*\[)', ns):
            if m.group(2) in bind and m.group(2) not in bad:
                do_bind(m.group(1), bind[m.group(2)])
    for v in sorted(bad):
        p = re.search(r'(?<![\w.])' + re.escape(v) + r'\b', ns)
        unres(p.start() if p else 0, "variable bound to more than one form", f"{v} -> " + ", ".join(sorted({bind[v]})))
        bind.pop(v, None)

    special = set()
    for m in re.finditer(r'\binsert\s+into\s+([A-Za-z_]\w*)\s*\[', ns):
        f, a = m.group(1), m.end() - 1
        b = _close(ns, a); special.add(a)
        if f not in forms:
            unres(m.start(), "insert into unknown form", f); continue
        add("insert", f, None)
        for fm in re.finditer(r'(?:^|[\n,\[])\s*([A-Za-z_]\w*)\s*=(?!=)', ns[a:b + 1]):
            x = fm.group(1)
            if x in fieldset[f] or x in SYS_FIELDS:
                add("insert", f, x)
            else:
                unres(a + fm.start(1), "insert field not on form", f"{f}.{x}")
    for m in re.finditer(r'\bdelete\s+from\s+([A-Za-z_]\w*)\s*\[', ns):
        f, a = m.group(1), m.end() - 1
        b = _close(ns, a); special.add(a)
        if f not in forms:
            unres(m.start(), "delete from unknown form", f); continue
        add("delete", f, None)
        for x in crit_fields(f, a, b):
            add("delete", f, x)
    for m in re.finditer(r'\bupdate\s+([A-Za-z_]\w*)\s*\[', ns):
        v, a = m.group(1), m.end() - 1
        b = _close(ns, a); special.add(a)
        f = bind.get(v)
        if f is None:
            unres(m.start(), "update target not resolvable to a form", v); continue
        add("update", f, None)
        for fm in re.finditer(r'(?:^|[\n,\[])\s*([A-Za-z_]\w*)\s*=(?!=)', ns[a:b + 1]):
            x = fm.group(1)
            if x in fieldset[f] or x in SYS_FIELDS:
                add("update", f, x)
            else:
                unres(a + fm.start(1), "update field not on form", f"{f}.{x}")
    for m in re.finditer(r'(?<![\w.])([A-Za-z_]\w*)\s*\[', ns):
        name, a = m.group(1), m.end() - 1
        if a in special:
            continue
        if name in forms:
            b = _close(ns, a)
            add("fetch", name, None)
            for x in crit_fields(name, a, b):
                add("fetch", name, x)
            tail = re.match(r'\s*\.\s*([A-Za-z_]\w*)(\s*\()?', ns[b + 1:b + 200])
            if tail and not tail.group(2):
                x = tail.group(1)
                if x in fieldset[name] or x in SYS_FIELDS:
                    add("read", name, x)
                else:
                    unres(b + 1, "field not on form", f"{name}.{x}")
        elif deluge and name[:1].isupper() and name not in assigned and name not in bind:
            unres(m.start(), "fetch target is not a known form", name)
    for m in re.finditer(r'(?<![\w.])([A-Za-z_]\w*)\s*\.\s*([A-Za-z_]\w*)(?:\s*\.\s*([A-Za-z_]\w*))?', ns):
        v, x, y = m.group(1), m.group(2), m.group(3)
        if v not in bind:
            continue
        f = bind[v]
        after = ns[m.end(2):m.end(2) + 3].lstrip()
        if after.startswith("("):
            continue
        if x in fieldset[f] or x in SYS_FIELDS:
            rest = ns[m.end(2):m.end(2) + 4].lstrip()
            if rest.startswith("=") and not rest.startswith("=="):
                add("update", f, x)
            else:
                add("read", f, x)
            tgt = lookups[f].get(x)
            if y and tgt and not ns[m.end(3):m.end(3) + 3].lstrip().startswith("("):
                if y in fieldset.get(tgt, ()) or y in SYS_FIELDS:
                    add("read", tgt, y)
                else:
                    unres(m.start(3), "field not on lookup target form", f"{tgt}.{y}")
        else:
            unres(m.start(2), "field not on form", f"{f}.{x} (via {v})")
    if own_form:
        _, wr, rd, _, _ = edges(code, set(), set())
        own = fieldset.get(own_form, set())
        r["in_set"] = set(ASSIGN_RE.findall(code))
        r["in_ui"] = set(wr) - r["in_set"]
        r["in_read"] = set(rd)
        for m in INPUT_RE.finditer(code):
            if m.group(1) not in own and m.group(1) not in SYS_FIELDS:
                unres(m.start(), "input field not on form", f"{own_form}.{m.group(1)}")
        for x in sorted(r["in_ui"] - own - SYS_FIELDS):
            p = re.search(r'\b(?:disable|enable|hide|show)\s+' + re.escape(x) + r'\b', code)
            unres(p.start() if p else 0, "show/hide field not on form", f"{own_form}.{x}")
    for m in re.finditer(r'\bthisapp\s*\.\s*([A-Za-z_][\w.]*)\s*\(', ns):
        nm = m.group(1).split(".")[-1]
        if nm in fn_names:
            r["calls"].add(nm)
        else:
            unres(m.start(), "thisapp call to unknown function", m.group(1))
    for m in CALL_RE.finditer(ns):
        if m.group(1) in fn_names:
            r["calls"].add(m.group(1))
    for m in re.finditer(r'\binvokeurl\b', ns, re.I):
        u = re.search(r'\burl\s*:\s*(.*)', code[m.end():m.end() + 600])
        unres(m.start(), "dynamic: invokeUrl", (u.group(1).strip()[:100] if u else "url not found"))
    for m in re.finditer(r'\b(getUrl|postUrl)\s*\(', ns):
        unres(m.start(), f"dynamic: {m.group(1)}", "")
    for m in re.finditer(r'\bzoho\s*\.\s*creator\s*\.\s*([A-Za-z_]\w*)\s*\(', ns):
        unres(m.start(), "dynamic: zoho.creator." + m.group(1), "")
    for m in re.finditer(r'#(Form|Report|Page):([A-Za-z0-9_]+)', code):
        kind, nm = m.group(1), m.group(2)
        known = {"Form": forms, "Report": report_names, "Page": page_names}[kind]
        if nm in known:
            r["opens"].add((kind, nm))
        else:
            unres(m.start(), f"link to unknown {kind.lower()}", nm)
    for m in re.finditer(r'\bopenUrl\s*\(', ns):
        arg = code[m.end():m.end() + 200].lstrip()
        if not arg.startswith('"'):
            unres(m.start(), "dynamic: openUrl target built from a variable", "")
    return r


def build_map(lines, ds_path):
    wf_start = next(i for i, l in enumerate(lines) if l.strip() == "workflow")
    forms = parse_forms(lines)
    fns = parse_functions(lines)
    allw = parse_workflows(lines, wf_start, keep_all=True)
    reports = parse_reports(lines)
    pages = parse_pages(lines)
    fn_names = {f["name"] for f in fns}
    fn_s = next(i for i, l in enumerate(lines) if l.strip() == "functions")
    for f in fns:
        f["line"] = next((i + 1 for i in range(fn_s, wf_start)
                          if re.match(r'^\s*[a-z]+\s+' + re.escape(f["name"]) + r'\s*\(', lines[i])), None)
    A = lambda body, own=None, params=(), deluge=True: analyze(body, own, forms, fn_names, set(reports), set(pages), params, deluge)
    items = []
    for w in allw:
        fbase, fcrit = (w["form"] or ""), ""
        mm = re.match(r'^([A-Za-z0-9_]+)\s*(\[.*\])?\s*$', fbase)
        if mm:
            fbase, fcrit = mm.group(1), (mm.group(2) or "")
        kind = {"form": "workflow", "schedule": "schedule", "functions": "report_action"}.get(w["section"], w["section"])
        if (w["kind"] or "").strip() in ("batch", "approval"):
            kind = w["kind"].strip()
        body = w["body"] if w["body"] is not None else w["action"]
        a = A(body, fbase if fbase in forms else None)
        if fcrit and fbase in forms:
            for x in sorted({m.group(1) for m in CRIT_ID_RE.finditer(_blank_strings(fcrit))}):
                if x in {f["name"] for f in forms[fbase]["fields"]} or x in SYS_FIELDS:
                    a["fetch"].setdefault(fbase, set()).add(x)
                else:
                    a["unresolved"].append((0, "criteria field not on form", f"{fbase}.{x}", fcrit))
        sm2 = re.search(r'\bfrom\s+([A-Za-z_]\w*)\s*$', w["start"] or "")
        if sm2 and fbase in forms:
            if sm2.group(1) in {f["name"] for f in forms[fbase]["fields"]} or sm2.group(1) in SYS_FIELDS:
                a["read"].setdefault(fbase, set()).add(sm2.group(1))
            else:
                a["unresolved"].append((0, "schedule start field not on form", f"{fbase}.{sm2.group(1)}", w["start"]))
        if w["form"] and fbase not in forms:
            a["unresolved"].append((0, "workflow form is not a known form", fbase, w["form"]))
        trig = w["ttype"] or ("OnClick" if w["click"] else "")
        if w["section"] == "schedule":
            trig = "schedule"
        items.append({"kind": kind, "name": w["name"], "display": w["display"], "form": fbase if w["form"] else "",
                      "form_criteria": fcrit, "record_event": w["record_event"] or "", "trigger": trig,
                      "field": w["field"] or "", "button": w["button"] or "",
                      "enabled": w["status"] != "inactive", "line": w["line"], "body_line": w.get("body_line"),
                      "start": (w["start"] or "").strip('"'), "frequency": w["frequency"] or "", "exec_type": w["exec_type"] or "",
                      "hash": body_hash(body), "a": a})
    for f in fns:
        params = re.findall(r'[A-Za-z]+\s+([A-Za-z_]\w*)', f["args"])
        f["a"] = A(f["body"], None, params)
    for p in pages.values():
        params = re.findall(r'[A-Za-z]+\s+([A-Za-z_]\w*)', p["params"])
        a = A(p["content"], None, params, deluge=False)
        a["unresolved"] = [u for u in a["unresolved"] if not u[1].startswith("fetch target")]
        p["embeds"] = []
        for m in re.finditer(r"<(report|form)\b[^>]*?linkName\s*=\s*'([A-Za-z0-9_]+)'", p["content"]):
            k, nm = m.group(1), m.group(2)
            ok = (nm in reports) if k == "report" else (nm in forms)
            if ok:
                p["embeds"].append((k.capitalize(), nm))
            else:
                a["unresolved"].append((p["content"].count("\n", 0, m.start()) + 1, f"embedded {k} not found", nm, nm))
        p["a"] = a
        p["hash"] = body_hash(p["content"])
    for rp in reports.values():
        rp["crit_fields"] = set()
        if rp["form"] in forms and rp["criteria"]:
            for x in {m.group(1) for m in CRIT_ID_RE.finditer(_blank_strings(rp["criteria"]))}:
                if x in {f["name"] for f in forms[rp["form"]]["fields"]} or x in SYS_FIELDS:
                    rp["crit_fields"].add(x)
    return {"forms": forms, "fns": fns, "items": items, "reports": reports, "pages": pages}


def _fmt_ops(a, ops=("fetch", "insert", "update", "delete", "read")):
    out = []
    for op in ops:
        for f in sorted(a[op]):
            flds = sorted(a[op][f])
            out.append(f"{op} {f}" + (f" ({', '.join(flds)})" if flds else ""))
    return out


def _scrub(t):
    return t.replace("\u2014", "-")


def _item_label(it):
    if it["kind"] == "workflow":
        return f"workflow {it['form']}/{it['name']}"
    return f"{it['kind'].replace('_', ' ')} {it['name']}"


def map_model_json(M, ds_sha):
    J = {"ds_sha256": ds_sha, "forms": {}, "workflows": {}, "functions": {}, "schedules": {},
         "reports": {}, "pages": {}, "report_actions": {}}
    for fn, f in M["forms"].items():
        J["forms"][fn] = {"display": f["display"],
                          "fields": {x["name"]: [x["type"] or "", x["display"], x["lookup"] or ""] for x in f["fields"]}}
    for it in M["items"]:
        key = {"workflow": "workflows", "schedule": "schedules", "report_action": "report_actions"}.get(it["kind"], "workflows")
        nm = f"{it['form']}/{it['name']}" if it["kind"] == "workflow" else it["name"]
        J[key][nm] = [it["hash"], it["record_event"], it["trigger"], it["field"],
                      "enabled" if it["enabled"] else "disabled", it["form_criteria"], it["start"], it["frequency"]]
    for f in M["fns"]:
        J["functions"][f["name"]] = [body_hash(f["body"]), f["rtype"], f["args"]]
    for r in M["reports"].values():
        J["reports"][r["name"]] = [r["form"] or "", r["criteria"], ";".join(f"{a['label']}={a['workflow']}" for a in r["actions"])]
    for p in M["pages"].values():
        J["pages"][p["name"]] = [p["hash"], p["params"]]
    return J


def _baseline(repo, ds_sha):
    """Newest committed map.json built from a DIFFERENT .ds (so reruns stay stable)."""
    import subprocess, json
    rel = os.path.join(MAP_DIR, "map.json").replace(os.sep, "/")
    try:
        revs = subprocess.run(["git", "-C", repo, "log", "--format=%H", "--", rel],
                              capture_output=True, text=True, check=True).stdout.split()
    except Exception:
        return None, None
    for h in revs:
        try:
            txt = subprocess.run(["git", "-C", repo, "show", f"{h}:{rel}"],
                                 capture_output=True, text=True, check=True).stdout
            j = json.loads(txt)
        except Exception:
            continue
        if j.get("ds_sha256") != ds_sha:
            return j, h[:7]
    return None, None


def render_changes(J, base, base_rev):
    L = ["# ds_map changes", ""]
    if base is None:
        L += ["No earlier committed map built from a different .ds was found. This map is the baseline.", ""]
        return "\n".join(L) + "\n"
    L += [f"Compared against the map committed at {base_rev} (built from .ds SHA-256 {base.get('ds_sha256', '')}).", ""]
    total = 0
    for sec in ("forms", "workflows", "functions", "schedules", "report_actions", "reports", "pages"):
        a, b = base.get(sec, {}), J.get(sec, {})
        added, removed = sorted(set(b) - set(a)), sorted(set(a) - set(b))
        modified = sorted(k for k in set(a) & set(b) if a[k] != b[k])
        if sec == "forms":
            modified = sorted(k for k in set(a) & set(b) if a[k].get("display") != b[k].get("display"))
        L.append(f"## {sec.replace('_', ' ').capitalize()}")
        if not (added or removed or modified):
            L.append("- no change")
        for k in added:
            L.append(f"- added: {k}")
        for k in removed:
            L.append(f"- removed: {k}")
        for k in modified:
            L.append(f"- modified: {k}")
        total += len(added) + len(removed) + len(modified)
        L.append("")
    L.append("## Fields")
    fl = []
    for fn in sorted(set(J["forms"]) | set(base.get("forms", {}))):
        a = base.get("forms", {}).get(fn, {}).get("fields", {})
        b = J["forms"].get(fn, {}).get("fields", {})
        for k in sorted(set(b) - set(a)):
            fl.append(f"- added: {fn}.{k}")
        for k in sorted(set(a) - set(b)):
            fl.append(f"- removed: {fn}.{k}")
        for k in sorted(x for x in set(a) & set(b) if a[x] != b[x]):
            fl.append(f"- modified: {fn}.{k} ({' / '.join(a[k])} -> {' / '.join(b[k])})")
    L += fl or ["- no change"]
    total += len(fl)
    L += ["", f"Total changes: {total}"]
    return "\n".join(L) + "\n"


def render_map(M, ds_path, ds_sha, mtime, gen_on, J, base, base_rev):
    import datetime
    forms, fns, items, reports, pages = M["forms"], M["fns"], M["items"], M["reports"], M["pages"]
    wfs = [i for i in items if i["kind"] == "workflow"]
    sch = [i for i in items if i["kind"] == "schedule"]
    acts = {i["name"]: i for i in items if i["kind"] == "report_action"}
    other = [i for i in items if i["kind"] in ("batch", "approval")]
    real = lambda f: [x for x in f["fields"] if x["type"] != "section"]
    files = {}
    callers = {}
    refs = {}

    def addref(form, fld, label, how):
        refs.setdefault((form, fld), {}).setdefault(label, set()).add(how)

    def index_item(label, a, own=None):
        for c in a["calls"]:
            callers.setdefault(c, set()).add(label)
        for op in ("fetch", "insert", "update", "delete", "read"):
            for f, flds in a[op].items():
                for x in flds:
                    addref(f, x, label, op)
        if own:
            for x in a["in_read"]:
                addref(own, x, label, "read")
            for x in a["in_set"]:
                addref(own, x, label, "set")
            for x in a["in_ui"]:
                addref(own, x, label, "show/hide")
    for it in items:
        index_item(_item_label(it), it["a"], it["form"] if it["form"] in forms else None)
        if it["trigger"] == "OnUserInput" and it["field"]:
            addref(it["form"], it["field"], _item_label(it), "trigger")
    for f in fns:
        index_item(f"function {f['name']}", f["a"])
    for p in pages.values():
        index_item(f"page {p['name']}", p["a"])
    for r in reports.values():
        for x in r["crit_fields"]:
            addref(r["form"], x, f"report {r['name']}", "filter")
        for ac in r["actions"]:
            it = acts.get(ac["workflow"])
            if it:
                for op in ("fetch", "insert", "update", "delete", "read"):
                    for f, flds in it["a"][op].items():
                        for x in flds:
                            addref(f, x, f"report action {r['name']}/{ac['label']}", op)
                for x in it["a"]["in_read"] | it["a"]["in_set"]:
                    addref(it["form"], x, f"report action {r['name']}/{ac['label']}", "read")

    # ---- _index.md
    I = ["# ds_map index", "",
         f"- Source: {os.path.basename(ds_path)}",
         f"- .ds export generated on (from .ds header): {gen_on}",
         f"- .ds file modified time: {mtime}",
         f"- .ds SHA-256: {ds_sha}",
         "- STATUS: CURRENT", "",
         "Derived from the .ds. Wins over schema/ when they disagree. Open the .dg or .ds for ground truth before editing.", "",
         "Relationship columns are regex-derived navigation aids, not an authoritative logic model. "
         "Unmatched and dynamic references are listed in unresolved.md and are never guessed.", "",
         "Files: forms/<Form>.md (fields, workflows, reverse index), functions.md, unresolved.md, changes.md, map.json (diff baseline).", "",
         "## Counts", "", "| Item | Count |", "|---|---|"]
    cnt = {"Forms": len(forms), "Fields (excluding sections)": sum(len(real(f)) for f in forms.values()),
           "Form workflows": len(wfs), "Form workflows disabled": sum(1 for w in wfs if not w["enabled"]),
           "Functions": len(fns), "Schedules": len(sch), "Batch workflows": sum(1 for i in other if i["kind"] == "batch"),
           "Approval workflows": sum(1 for i in other if i["kind"] == "approval"),
           "Reports": len(reports), "Report custom actions": sum(len(r["actions"]) for r in reports.values()),
           "Pages": len(pages)}
    I += [f"| {k} | {v} |" for k, v in cnt.items()]
    I += ["", "## Forms", "", "| Link name | Display name | Fields | Workflows | Parent form (subform) |", "|---|---|---|---|---|"]
    subs = {}
    for fn, f in forms.items():
        for x in f["fields"]:
            if x["type"] in ("subform", "grid"):
                subs[x["lookup"] or x["name"]] = fn
    for fn in sorted(forms):
        f = forms[fn]
        I.append(f"| {fn} | {f['display'] or '-'} | {len(real(f))} | {sum(1 for w in wfs if w['form'] == fn)} | {subs.get(fn, '-')} |")
    I += ["", f"Subforms: {len(subs)} detected." + ("" if subs else " No subform field type is present in this .ds."), ""]
    I += ["## Form-to-form lookups", ""]
    lk = sorted(f"{fn}.{x['name']} -> {x['lookup']}" for fn, f in forms.items() for x in f["fields"] if x["lookup"])
    I += [f"- {x}" for x in lk] or ["- none"]
    I += ["", "## Functions", "", "| Name | Namespace | Returns | Arguments |", "|---|---|---|---|"]
    for f in sorted(fns, key=lambda x: x["name"]):
        I.append(f"| {f['name']} | {f['namespace']} | {f['rtype']} | {f['args'] or '-'} |")
    I += ["", "## Reports", "", "| Report | Type | Source form | Filter | Custom actions |", "|---|---|---|---|---|"]
    for rn in sorted(reports):
        r = reports[rn]
        ca = "; ".join(f"\"{a['label']}\" -> {a['workflow']}" for a in r["actions"]) or "-"
        crit = r["criteria"].replace("|", "\\|") or "-"
        I.append(f"| {rn} | {r['type']}{' (default)' if r['default'] else ''} | {r['form']} | {crit} | {ca} |")
    I += ["", "### Report custom actions", ""]
    any_ca = False
    for rn in sorted(reports):
        for a in reports[rn]["actions"]:
            any_ca = True
            it = acts.get(a["workflow"])
            if it:
                calls = ", ".join(sorted(it["a"]["calls"])) or "none"
                opens = ", ".join(f"{k} {n}" for k, n in sorted(it["a"]["opens"])) or "none"
                I.append(f"- {rn} \"{a['label']}\" -> action workflow {a['workflow']} (form {it['form']}, {it['exec_type'] or 'n/a'}): calls {calls}; opens {opens}")
            else:
                I.append(f"- {rn} \"{a['label']}\" -> {a['workflow']} (action workflow not found, see unresolved.md)")
    if not any_ca:
        I.append("- none")
    I += ["", "## Pages", "", "| Page | Parameters | Source forms | Embeds and links | Functions called |", "|---|---|---|---|---|"]
    for pn in sorted(pages):
        p = pages[pn]
        src = set(p["a"]["fetch"]) | set(p["a"]["read"])
        for k, n in p["embeds"] + sorted(p["a"]["opens"]):
            if k == "Report" and reports.get(n, {}).get("form"):
                src.add(reports[n]["form"])
            elif k == "Form":
                src.add(n)
        emb = ", ".join(f"{k} {n}" for k, n in sorted(set(p["embeds"]) | p["a"]["opens"])) or "-"
        I.append(f"| {pn} | {p['params'] or '-'} | {', '.join(sorted(src)) or '-'} | {emb} | {', '.join(sorted(p['a']['calls'])) or '-'} |")
    I += ["", "## Schedules", "", "| Schedule | Form (criteria) | Start | Frequency | Functions called | Fields touched |", "|---|---|---|---|---|---|"]
    for s in sorted(sch, key=lambda x: x["name"]):
        touched = "; ".join(_fmt_ops(s["a"])) or "-"
        I.append(f"| {s['name']} | {(s['form'] + ' ' + s['form_criteria']).strip().replace('|', chr(92) + '|') or '-'} | {s['start'] or '-'} | {s['frequency'] or '-'} | {', '.join(sorted(s['a']['calls'])) or '-'} | {touched} |")
    I += ["", "## Batch and approval workflows", ""]
    I += [f"- {i['kind']} {i['name']} form {i['form']} trigger {i['trigger']}: calls {', '.join(sorted(i['a']['calls'])) or 'none'}" for i in other] or \
         ["- none present in this .ds"]
    files["_index.md"] = I

    # ---- forms/<Form>.md
    for fn in sorted(forms):
        f = forms[fn]
        F = [f"# {fn}", "", f"- Display name: {f['display'] or '-'}", f"- .ds line: {f['line']}",
             f"- Fields (excluding sections): {len(real(f))}", f"- Parent form: {subs.get(fn, '-')}", "",
             "## Fields", "", "| Link name | Display name | Type | Lookup target |", "|---|---|---|---|"]
        for x in f["fields"]:
            F.append(f"| {x['name']} | {x['display'] or '-'} | {x['type'] or '-'} | {x['lookup'] or '-'} |")
        F += ["", "## Workflows", ""]
        mine = sorted([w for w in wfs if w["form"] == fn], key=lambda w: w["name"])
        if not mine:
            F.append("- none")
        for w in mine:
            ev = w["trigger"] + (f" of {w['field']}" if w["field"] else "") + (f" (button {w['button']})" if w["button"] else "")
            F += [f"### {w['name']}", "",
                  f"- Display: {w['display']}", f"- Record event: {w['record_event'] or '-'}", f"- Form event: {ev or '-'}",
                  f"- Status: {'ENABLED' if w['enabled'] else 'DISABLED'}", f"- .ds line: {w['line']}",
                  f"- Fields read: {', '.join(sorted(w['a']['in_read'])) or '-'}",
                  f"- Fields set: {', '.join(sorted(w['a']['in_set'])) or '-'}",
                  f"- Fields shown/hidden/enabled/disabled: {', '.join(sorted(w['a']['in_ui'])) or '-'}",
                  f"- Functions called: {', '.join(sorted(w['a']['calls'])) or '-'}",
                  f"- Other forms: {'; '.join(_fmt_ops(w['a'])) or '-'}", ""]
        F += ["## Reverse index", "", "Every item that references a field of this form.", ""]
        for x in f["fields"]:
            if x["type"] == "section":
                continue
            rs = [f"{lb} [{', '.join(sorted(h))}]" for lb, h in sorted(refs.get((fn, x["name"]), {}).items())]
            F.append(f"- {fn}.{x['name']}: " + ("; ".join(rs) if rs else "no references"))
        files[os.path.join("forms", fn + ".md")] = F

    # ---- functions.md
    FN = ["# Functions", "", "Per function: forms and fields it fetches, inserts, updates, deletes or reads through a fetched record; "
          "functions it calls; callers; integrations (INTEG_KEYS).", ""]
    for f in sorted(fns, key=lambda x: x["name"]):
        a = f["a"]
        _, _, _, _, ig = edges(f["body"], set(), set())
        FN += [f"## {f['name']}", "", f"- Signature: {f['namespace']}.{f['name']}({f['args']}) returns {f['rtype']}",
               f"- .ds line: {f['line']}"]
        for op in ("fetch", "insert", "update", "delete", "read"):
            v = "; ".join(_fmt_ops(a, (op,))).replace(f"{op} ", "")
            FN.append(f"- {op.capitalize()}: {v or '-'}")
        FN += [f"- Calls: {', '.join(sorted(a['calls'] - {f['name']})) or '-'}",
               f"- Called by: {', '.join(sorted(callers.get(f['name'], set()) - {'function ' + f['name']})) or '-'}",
               f"- Integrations: {', '.join(ig) or '-'}", ""]
    files["functions.md"] = FN

    # ---- unresolved.md
    U = ["# Unresolved references", "",
         "References that could not be matched to a known form, field, function, report or page, plus string-built or "
         "dynamic references. None of these are guessed. Location is the item, its .ds start line, and the line within its body.", ""]
    rows = []
    for it in items:
        for ln, kind, what, sn in it["a"]["unresolved"]:
            loc = it["body_line"] + ln - 1 if it.get("body_line") and ln else None
            rows.append((_item_label(it), it["line"], ln, kind, what, sn, loc))
    for f in fns:
        for ln, kind, what, sn in f["a"]["unresolved"]:
            rows.append((f"function {f['name']}", f["line"], ln, kind, what, sn, None))
    for p in pages.values():
        for ln, kind, what, sn in p["a"]["unresolved"]:
            rows.append((f"page {p['name']}", p["line"], ln, kind, what, sn, None))
    for r in reports.values():
        if r["form"] not in forms:
            rows.append((f"report {r['name']}", r["line"], 0, "report source form not found", r["form"] or "", "", None))
        for a in r["actions"]:
            if a["workflow"] not in acts:
                rows.append((f"report {r['name']}", a["line"], 0, "custom action workflow not found", a["workflow"] or "", "", None))
    for fn, f in forms.items():
        for x in f["fields"]:
            if x["lookup"] and x["lookup"] not in forms:
                rows.append((f"form {fn}", f["line"], 0, "lookup target form not found", f"{fn}.{x['name']} -> {x['lookup']}", "", None))
            if x["type"] not in KNOWN_FIELD_TYPES:
                rows.append((f"form {fn}", f["line"], 0, "unrecognized field type", f"{fn}.{x['name']} type {x['type']}", "", None))
    rows.sort(key=lambda r: (r[3], r[0], r[2], r[4]))
    U += [f"Total: {len(rows)}", "", "| Kind | Reference | Location | Body line | Snippet |", "|---|---|---|---|---|"]
    by = Counter(r[3] for r in rows)
    for r in rows:
        U.append(f"| {r[3]} | {r[4].replace('|', chr(92) + '|')} | {r[0]} (.ds line {r[1]}) | {r[2] or '-'} | {r[5] or '-'} |")
    U += ["", "## By kind", ""] + [f"- {k}: {v}" for k, v in sorted(by.items())]
    files["unresolved.md"] = U

    files["changes.md"] = render_changes(J, base, base_rev).rstrip("\n").split("\n")
    out = {k: _scrub("\n".join(v).rstrip("\n") + "\n") for k, v in files.items()}
    import json
    out["map.json"] = json.dumps(J, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    return out, cnt, len(rows)


def run_map(repo, ds_path, lines):
    import datetime
    if os.path.basename(ds_path) != MAP_DS_NAME:
        raise SystemExit(f"--map parses only {MAP_DS_NAME}, never a versioned copy (got {os.path.basename(ds_path)})")
    raw = open(ds_path, "rb").read()
    ds_sha = hashlib.sha256(raw).hexdigest()
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(ds_path)).strftime("%Y-%m-%d %H:%M:%S")
    # checkouts and clones reset file mtimes; keep the recorded time while the
    # .ds bytes are unchanged so a rerun produces no diff
    prev = os.path.join(repo, MAP_DIR, "_index.md")
    if os.path.exists(prev):
        pt = open(prev, encoding="utf-8").read()
        ps = re.search(r'^- \.ds SHA-256: ([0-9a-f]{64})\s*$', pt, re.M)
        pm = re.search(r'^- \.ds file modified time: (.+?)\s*$', pt, re.M)
        if ps and pm and ps.group(1) == ds_sha:
            mtime = pm.group(1)
    gm = re.search(r'Generated on\s*:\s*(.+)', "\n".join(lines[:8]))
    gen_on = gm.group(1).strip() if gm else "unknown"
    M = build_map(lines, ds_path)
    J = map_model_json(M, ds_sha)
    base, base_rev = _baseline(repo, ds_sha)
    out, cnt, nunres = render_map(M, ds_path, ds_sha, mtime, gen_on, J, base, base_rev)
    dc = ds_counts(lines)
    checks = [("forms", dc["forms"], cnt["Forms"]),
              ("fields", dc["fields"], cnt["Fields (excluding sections)"]),
              ("workflows", dc["workflows"], cnt["Form workflows"]),
              ("disabled workflows", dc["inactive_workflows"], cnt["Form workflows disabled"]),
              ("functions", dc["functions"], cnt["Functions"]),
              ("schedules", dc["schedules"], cnt["Schedules"]),
              ("batch workflows", dc["batch_workflows"], cnt["Batch workflows"]),
              ("approval workflows", dc["approval_workflows"], cnt["Approval workflows"]),
              ("reports", dc["reports"], cnt["Reports"]),
              ("pages", dc["pages"], cnt["Pages"]),
              ("report action workflows", dc["report_actions_wf"], sum(1 for i in M["items"] if i["kind"] == "report_action"))]
    print(f"\nMAP verify ({'item':24} {'.ds':>6} {'map':>6})")
    bad = []
    for name, d, m in checks:
        print(f"  {name:28} {d:6} {m:6}{'' if d == m else '  MISMATCH'}")
        if d != m:
            bad.append(f"{name} .ds={d} map={m}")
    for name, d, m in checks[:2]:
        if d == 0:
            bad.append(f"no {name} found in the .ds (section not located)")
    for k, v in out.items():
        if "\u2014" in v:
            bad.append(f"em dash in {k}")
    if bad:
        print("MAP: count mismatch, map NOT written: " + "; ".join(bad))
        return 3
    root = os.path.join(repo, MAP_DIR)
    want = {os.path.join(root, k) for k in out}
    for k, v in out.items():
        p = os.path.join(root, k)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p) or open(p, encoding="utf-8").read() != v:
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(v)
    for p in glob.glob(os.path.join(root, "forms", "*.md")):
        if p not in want:
            os.remove(p)
    print(f"MAP: wrote {len(out)} files to {MAP_DIR}/ ({nunres} unresolved references)")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--new-only", action="store_true")
    ap.add_argument("--manifest", action="store_true")
    ap.add_argument("--map", action="store_true")
    a = ap.parse_args()
    lines = open(a.ds, encoding="utf-8", errors="replace").read().split("\n")
    wf_start = next(i for i, l in enumerate(lines) if l.strip() == "workflow")
    wfs = parse_workflows(lines, wf_start)
    fns = parse_functions(lines)

    resolved = []
    for w in wfs:
        path, how = resolve_wf_path(a.repo, w)
        resolved.append((None if how == "ambiguous" else path, w["body"], w["name"], w))
    # an EMPTY body never writes, so it must not claim a path and fake a
    # collision (Partner_Rate_Partner_Stam vs Partner_Rate_Stamp_Genera1, v53)
    claims = Counter(p for p, b, _, _ in resolved if p and (b or "").strip())
    collided = {p for p, c in claims.items() if c > 1}

    rows, written = [], 0
    for path, body, name, w in resolved:
        if path is None or path in collided:
            lbl = f"{w['form']}/{w['ttype']} {name}" if path is None else f"{os.path.relpath(path, a.repo)} <- {name}"
            rows.append(("AMBIGUOUS", lbl, "")); continue
        st, wr = classify(path, body, a.apply)
        rows.append((st, os.path.relpath(path, a.repo), name))
        if wr and (not a.new_only or st == "NEW"):
            os.makedirs(os.path.dirname(wr), exist_ok=True)
            open(wr, "w", encoding="utf-8").write(body + "\n"); written += 1

    for f in fns:
        path = os.path.join(a.repo, "functions", f["name"] + ".dg")
        st, wr = classify(path, f["body"], a.apply)
        rows.append((st, os.path.relpath(path, a.repo), f["name"]))
        if wr and (not a.new_only or st == "NEW"):
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

    if a.map:
        rc = run_map(a.repo, a.ds, lines)
        if rc:
            raise SystemExit(rc)

    if a.manifest:
        known_fns = {f["name"] for f in fns} | {os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(a.repo, "functions", "*.dg"))}
        known_forms = {w["form"] for w in wfs} | {d for d in os.listdir(a.repo) if os.path.isdir(os.path.join(a.repo, d)) and not d.startswith(".")}
        mpath, mcount = write_manifest(a.repo, resolved, fns, known_fns, known_forms)
        print(f"MANIFEST: wrote {mcount} rows to {os.path.relpath(mpath, a.repo)}")


if __name__ == "__main__":
    main()
