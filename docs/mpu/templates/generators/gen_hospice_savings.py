import json, re, os

D = json.load(open('accentcare_july.json'))
T = lambda n: open('tpl/p%02d.html' % n).read()

PARTNER = 'AccentCare'
N = D['n']
QUAL = D['total_qual']
SAV = D['total_sav']
DIV = D['div']
AVG = SAV / QUAL
ANN = SAV * 12
BENCH = {'Paracentesis Performed': 5655.87, 'Thoracentesis Performed': 10185.43,
         'Catheter Management': 3897.49, 'G-Tube/PEG Management': 2549.19}
LABEL = {'Paracentesis Performed': 'Paracentesis', 'Thoracentesis Performed': 'Thoracentesis',
         'Catheter Management': 'Catheter Management', 'G-Tube/PEG Management': 'G-Tube/PEG Management'}
RATE = {'High Complexity': 545.0, 'Moderate Complexity': 343.0, 'Low Complexity': 150.0,
        'Telemedicine': 55.0, 'No Charge': 0.0}
TRANSPORT = 955.04
SVC = D['svc']
ACU = D['acu']
BR = D['branches']

def m0(v):
    return '$' + format(int(round(v)), ',')

def m2(v):
    return '$' + format(v, ',.2f')

def pct(a, b):
    v = 100.0 * a / b
    return '%d%%' % round(v) if abs(v - round(v)) < 0.05 and v in (0.0, 100.0) else '%.1f%%' % v

def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

BADID = ('1FT7UC1VE46', '6AD6CW4MQ73')
def hid(v):
    v = str(v).strip()
    if not v or v.lower() in ('none', 'na', 'n/a') or v in BADID:
        return '&#8211;'
    return esc(v)

proc = {}
for b in BR.values():
    for r in b['rows']:
        v = r[3]
        if v in BENCH:
            d = proc.setdefault(v, {'n': 0, 'hosp': 0.0, 'sav': 0.0})
            d['n'] += 1
            d['hosp'] += BENCH[v]
            d['sav'] += BENCH[v] - RATE.get(r[4], 0.0)
ORDER = [k for k in ['Paracentesis Performed', 'Thoracentesis Performed',
                     'Catheter Management', 'G-Tube/PEG Management'] if k in proc]

NAVY = '#0b0b5b'
MID = '#5b5b9a'
LILAC = '#a5a5c8'
PALE = '#c9c9e0'
GREEN = '#02cd3b'
ACUCOL = {'High Complexity': '#0b0b5b', 'Moderate Complexity': '#3d3d80',
          'Telemedicine': '#5b5b9a', 'Low Complexity': '#a5a5c8', 'No Charge': '#ff0000'}
BARCOL = ['#0b0b5b', '#3d3d80', '#5b5b9a', '#7a7ab0', '#a5a5c8', '#c9c9e0']

def spine(page, num):
    page = page.replace('Empath &middot; July 2026', PARTNER + ' &middot; July 2026')
    page = page.replace('Empath · July 2026', PARTNER + ' · July 2026')
    page = page.replace('Empath | July 2026', PARTNER + ' | July 2026')
    page = re.sub(r"(sans-serif; color: #a5a5c8;\">)\d\d(</div>)",
                  lambda mm: mm.group(1) + '%02d' % num + mm.group(2), page, count=1)
    return page

def swap(page, pairs):
    for old, new in pairs:
        assert page.count(old) >= 1, 'MISSING: ' + old[:90]
        page = page.replace(old, new, 1)
    return page

def block(page, anchor_open, replacement):
    """replace the balanced div that starts at the first occurrence of anchor_open"""
    i = page.find(anchor_open)
    assert i >= 0, 'anchor missing: ' + anchor_open[:80]
    start = page.rfind('<div', 0, i + 1)
    dpt = 0
    j = start
    rx = re.compile(r'<div\b|</div>')
    while j < len(page):
        mm = rx.search(page, j)
        if not mm:
            break
        dpt += 1 if mm.group(0).startswith('<div') else -1
        j = mm.end()
        if dpt == 0:
            break
    return page[:start] + replacement + page[j:]

PAGES = []

# ---------------- P1 cover ----------------
p = T(1)
p = p.replace('color: #0d155c;">Empath</div>', 'color: #0d155c;">' + PARTNER + '</div>')
PAGES.append(p)

# ---------------- P2 executive summary ----------------
p = spine(T(2), 2)
top = SVC[0]
qsvc = [s for s in SVC if s[0] in BENCH]
evals = sum(c for s, c in SVC if 'Eval (Not Performed)' in s)
brtop = max(BR.items(), key=lambda x: x[1]['n'])
peak = max(D['refhours'], key=lambda x: x[1])
a0, a1 = ACU[0], ACU[1]
p = swap(p, [
 ('>118</div>', '>%d</div>' % N),
 ('>117</div>', '>%d</div>' % DIV),
 ('>99.2%</div>', '>%s</div>' % pct(DIV, N)),
 ('>$233,810</div>', '>%s</div>' % m0(SAV)),
 ('<strong>$233,810.16</strong> in hospital cost for Empath in July 2026, across 54 qualifying visits, an average of $4,329.82 per qualifying visit. Held at this rate, current utilization represents approximately <strong>$2,805,721.92</strong>',
  '<strong>%s</strong> in hospital cost for %s in July 2026, across %d qualifying visits, an average of %s per qualifying visit. Held at this rate, current utilization represents approximately <strong>%s</strong>'
  % (m2(SAV), PARTNER, QUAL, m2(AVG), m2(ANN))),
 ('SOS completed 118 in-home clinical visits for Empath patients across 6 service areas in Florida. 117 of 118 visits (99.2%) were completed as diversions, preventing transport or referral to an outside care setting.',
  'SOS completed %d in-home clinical visits for %s patients across %d service areas in Florida. %d of %d visits (%s) were completed as diversions, preventing transport or referral to an outside care setting.'
  % (N, PARTNER, len(BR), DIV, N, pct(DIV, N))),
 ('Paracentesis Performed led billable procedures at 32 visits (27.1%). SOS delivered 13 distinct service types, including 19 in-home paracentesis and thoracentesis evaluations where the procedure was appropriately deferred.',
  '%s led service volume at %d visits (%s). SOS delivered %d distinct service types, including %d in-home paracentesis and thoracentesis evaluations where the procedure was appropriately deferred.'
  % (esc(top[0]), top[1], pct(top[1], N), len(SVC), evals)),
 ('The visit mix was led by High Complexity at 59 visits (50.0%) and Moderate Complexity at 39 visits (33.1%).',
  'The visit mix was led by %s at %d visits (%s) and %s at %d visits (%s).'
  % (a0[0], a0[1], pct(a0[1], N), a1[0], a1[1], pct(a1[1], N))),
 ('Referrals concentrated in the 10:00-12:00 window at 25 (19.7%). Suncoast Pinellas led branch volume at 44 visits (37.3%).',
  'Referrals concentrated in the %s window at %d (%s). %s led branch volume at %d visits (%s).'
  % (peak[0], peak[1], pct(peak[1], D['refhours_total']), esc(brtop[0]), brtop[1]['n'], pct(brtop[1]['n'], N))),
])
st = D['status']
parts = []
for k, lab in [('Cancelled', 'were cancelled before care was rendered'),
               ('Duplicate', 'were duplicate submissions of a visit already recorded'),
               ('Folded', 'were folded into another visit'),
               ('Excluded', 'were excluded on review')]:
    if st.get(k):
        n = st[k]
        w = lab.replace('were', 'was', 1) if n == 1 else lab
        parts.append('%d %s' % (n, w))
recon = ('<strong>Records reconciliation.</strong> %d patient visit records were submitted for %s in July 2026. '
         '%s; all are excluded from every figure in this report. The remaining %d are the visits reported throughout.'
         % (D['submitted'], PARTNER, ', '.join(parts[:-1]) + ' and ' + parts[-1] if len(parts) > 1 else parts[0], N))
p = re.sub(r'<strong>Records reconciliation\.</strong>.*?throughout\.', recon, p, flags=re.S)
PAGES.append(p)
print('p1,p2 ok')

# ---------------- P3 volume, services, delivery ----------------
SHORT = {'Paracentesis Eval (Not Performed)': 'Paracentesis Eval',
         'Thoracentesis Eval (Not Performed)': 'Thoracentesis Eval',
         'G-Tube/PEG Management': 'G-Tube/PEG Mgmt',
         'Consultation/Evaluation': 'Consultation/Evaluation',
         'Pleural Catheter/Chest Tube': 'Pleural Cath/Chest Tube'}
ELL60 = ('<svg viewBox="0 0 400 60" preserveAspectRatio="none" style="position: absolute; left: -12px; '
 'right: -12px; top: -11px; bottom: -14px; width: calc(100% + 24px); height: calc(100% + 25px); '
 'pointer-events: none; overflow: visible;"><path d="M 397 24 C 399 46 331 59 199 59 C 70 59 3 47 3 30 '
 'C 3 13 70 2 199 2 C 328 2 397 10 396 25 C 395 45 380 56 348 59" fill="none" stroke="#02cd3b" '
 'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke" '
 'opacity="0.9"/></svg>')

def svcrow(name, cnt, top, first):
    w = 100.0 * cnt / top
    col = NAVY if first else (MID if w >= 40 else LILAC)
    bold = ' style="font-weight: 600;"' if first else ''
    return ('<div style="display: grid; grid-template-columns: 150px 1fr 58px; gap: 8px; align-items: center;">'
            '<div style="text-align: right;">%s</div><div><div style="height: 12px; background: %s; '
            'width: %.2f%%;"></div></div><div%s>%d &middot; %s</div></div>'
            % (esc(SHORT.get(name, name)), col, w, bold, cnt, pct(cnt, N)))

top = SVC[0][1]
rows_top = ''.join(svcrow(s, c, top, i == 0) for i, (s, c) in enumerate(SVC[:3]))
rows_rest = ''.join(svcrow(s, c, top, False) for s, c in SVC[3:])
svcblock = ('<div style="display: flex; flex-direction: column; gap: 6px; font: 400 10.5px '
 "'Libre Franklin', sans-serif; color: #000000; white-space: nowrap;\">"
 '<div style="position: relative; display: flex; flex-direction: column; gap: 6px; margin: 5px 0 15px 0;">'
 + rows_top + ELL60 + '</div>' + rows_rest + '</div>')

p = spine(T(3), 3)
p = block(p, 'white-space: nowrap;"><div style="position: relative;', svcblock)
p = swap(p, [
 ('13 distinct service types. The top three account for 64 of 118 visits.',
  '%d distinct service types. The top three account for %d of %d visits.'
  % (len(SVC), sum(c for _, c in SVC[:3]), N)),
])

# time of day
hb = D['refhours']
mx = max(c for _, c in hb)
peak = max(hb, key=lambda x: x[1])
bars = ''.join('<div style="flex: 1; display: flex; flex-direction: column; justify-content: flex-end; '
               'height: 100%%;"><div style="background: %s; height: %.0f%%;"></div></div>'
               % (NAVY if c == mx else (MID if c >= mx * 0.6 else LILAC), 100.0 * c / mx)
               for _, c in hb)
p = block(p, 'display: flex; align-items: flex-end; gap: 4px; height: 90px;',
          '<div style="display: flex; align-items: flex-end; gap: 4px; height: 90px;">%s</div>' % bars)
p = swap(p, [
 ('<div>06:00</div><div>10:00-12:00 peak \u00b7 25 (19.7%)</div><div>24:00</div>',
  '<div>%s</div><div>%s peak \u00b7 %d (%s)</div><div>%s</div>'
  % (hb[0][0].split('-')[0], peak[0], peak[1], pct(peak[1], D['refhours_total']), hb[-1][0].split('-')[1])),
 ('127 referrals received in the month.', '%d referrals received in the month.' % D['refhours_total']),
])

# visit complexity
SEG = {'High Complexity': '#0b0b5b', 'Moderate Complexity': '#5b5b9a', 'Telemedicine': '#8d8db8',
       'Low Complexity': '#c4c4dd', 'No Charge': '#ff0000'}
DOT = {'High Complexity': '#0b0b5b', 'Moderate Complexity': '#5b5b9a', 'Telemedicine': '#a5a5c8',
       'Low Complexity': '#c4c4dd', 'No Charge': '#ff0000'}
ACUORD = ['High Complexity', 'Moderate Complexity', 'Telemedicine', 'Low Complexity', 'No Charge']
acud = dict(ACU)
seq = [(a, acud.get(a, 0)) for a in ACUORD]
segs = ''.join('<div style="width: %.1f%%; background: %s;"></div>' % (100.0 * c / N, SEG[a])
               for a, c in seq if c)
p = block(p, 'display: flex; height: 22px;', '<div style="display: flex; height: 22px;">%s</div>' % segs)
legend = ''.join('<div style="display: flex; justify-content: space-between;"><div>'
 '<span style="display: inline-block; width: 9px; height: 9px; background: %s; margin-right: 6px;"></span>%s</div>'
 '<div%s>%d &middot; %s</div></div>'
 % (DOT[a], a, ' style="font-weight: 600;"' if c == max(x[1] for x in seq) else '', c, pct(c, N))
 for i, (a, c) in enumerate(seq))
p = block(p, "gap: 4px; margin-top: 8px; font: 400 10.5px 'Libre Franklin'",
 '<div style="display: flex; flex-direction: column; gap: 4px; margin-top: 8px; font: 400 10.5px '
 "'Libre Franklin', sans-serif; color: #000000;\">%s</div>" % legend)

# branch breakdown
bv = sorted(BR.items(), key=lambda x: -x[1]['n'])
nb = len(bv)
bmax = bv[0][1]['n']
bbars = ''.join('<div style="display: flex; flex-direction: column; justify-content: flex-end; height: 100%%; '
 'text-align: center;"><div style="font: %s 13px \'Libre Franklin\', sans-serif; color: %s; margin-bottom: 4px;">%d</div>'
 '<div style="background: %s; height: %.1f%%;"></div></div>'
 % ('700' if i == 0 else '600', NAVY if i == 0 else MID, d['n'],
    BARCOL[min(i, len(BARCOL) - 1)], 100.0 * d['n'] / bmax)
 for i, (b, d) in enumerate(bv))
p = block(p, 'grid-template-columns: repeat(6, 1fr); gap: 12px; align-items: end; height: 120px;',
 '<div style="display: grid; grid-template-columns: repeat(%d, 1fr); gap: 12px; align-items: end; '
 'height: 120px; margin-top: 8px;">%s</div>' % (nb, bbars))
def brlabel(b):
    w = b.split()
    return (esc(' '.join(w[:-1])) + '<br>' + esc(w[-1])) if len(w) > 1 else esc(b) + '<br>&nbsp;'
blabels = ''.join('<div>%s<div style="font-weight: 400; color: #5b5b9a; margin-top: 2px;">%s</div></div>'
                  % (brlabel(b), pct(d['n'], N)) for b, d in bv)
p = block(p, 'grid-template-columns: repeat(6, 1fr); gap: 12px; margin-top: 8px; font: 600 10px/1.35',
 '<div style="display: grid; grid-template-columns: repeat(%d, 1fr); gap: 12px; margin-top: 8px; '
 "font: 600 10px/1.35 'Libre Franklin', sans-serif; color: #0b0b5b; text-align: center;\">%s</div>"
 % (nb, blabels))
p = re.sub(r'\d+ branches served\.[^<]*',
           '%d branches served. %s carried the highest volume at %d visits (%s).'
           % (nb, esc(bv[0][0]), bv[0][1]['n'], pct(bv[0][1]['n'], N)), p, count=1)
PAGES.append(p)
print('p3 ok')

# ---------------- P4 estimated cost savings ----------------
def card(name):
    d = proc[name]
    hp = 100.0 * d['sav'] / d['hosp']
    return ('<div style="border: 1px solid #a5a5c8; padding: 18px 20px;">\n'
     '              <div style="display: flex; justify-content: space-between; align-items: baseline;">'
     '<div style="font: 700 14px \'Libre Franklin\', sans-serif; color: #0d155c;">%s</div>'
     '<div style="border: 1px solid #a5a5c8; padding: 3px 8px; font: 600 11px \'Libre Franklin\', sans-serif; '
     'color: #5b5b9a;">%d visit%s</div></div>\n'
     '              <div style="display: flex; align-items: baseline; gap: 10px; margin-top: 10px;">'
     '<div style="font: 700 30px \'Libre Franklin\', sans-serif; color: #0b0b5b;">%s</div>'
     '<div style="font: 600 10.5px \'Libre Franklin\', sans-serif; letter-spacing: 0.08em; color: #02cd3b;">'
     'EST SAVINGS</div></div>\n'
     '              <div style="display: flex; align-items: center; gap: 8px; margin-top: 12px;">\n'
     '                <div style="width: 108px; flex-shrink: 0; border: 1px solid #a5a5c8; box-sizing: border-box; '
     'display: flex; justify-content: space-between; padding: 3px 8px; font: 600 10px \'Libre Franklin\', sans-serif; '
     'color: #0b0b5b;"><span style="font-weight: 700; font-size: 9.5px; letter-spacing: 0.06em;">HOSP</span>'
     '<span>%s</span></div>\n'
     '                <div style="flex: 1; display: flex; height: 16px;">\n'
     '                  <div style="background: #02cd3b; width: %.1f%%;"></div>\n'
     '                  <div style="background: #0b0b5b; width: %.1f%%;"></div>\n'
     '                </div>\n              </div>\n            </div>'
     % (LABEL[name], d['n'], '' if d['n'] == 1 else 's', m0(d['sav']), m0(d['hosp']), hp, 100.0 - hp))

p = spine(T(4), 4)
p = block(p, 'display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;',
 '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;">\n            %s\n          </div>'
 % ''.join(card(k) for k in ORDER))
p = swap(p, [
 ('54 qualifying visits \u00b7 $4,329.82 avg per visit',
  '%d qualifying visits \u00b7 %s avg per visit' % (QUAL, m2(AVG))),
 ('>$233,810.16</div>', '>%s</div>' % m2(SAV)),
 ('64 of 118 visits carry no published hospital benchmark and are excluded entirely. Transport alone accounts for $61,122.56 across those visits, none of it in the total above.',
  '%d of %d visits carry no published hospital benchmark and are excluded entirely. Transport alone accounts for %s across those visits, none of it in the total above.'
  % (N - QUAL, N, m2((N - QUAL) * TRANSPORT))),
])
PAGES.append(p)
print('p4 ok')

# ---------------- P5 continued ----------------
p = spine(T(5), 5)
body = ''
for i, k in enumerate(ORDER):
    d = proc[k]
    body += ('<tr style="border-bottom: 1px solid #a5a5c8;%s"><td style="padding: 4px 10px;">%s</td>'
     '<td style="padding: 4px 10px; text-align: right;">%d</td>'
     '<td style="padding: 4px 10px; text-align: right;">%s</td>'
     '<td style="padding: 4px 10px; text-align: right; font-weight: 600; color: #0b0b5b;">%s</td></tr>'
     % (' background: #f7f7fb;' if i % 2 else '', LABEL[k], d['n'], m0(d['hosp']), m0(d['sav'])))
i0 = p.find('<td style="padding: 4px 10px;">Paracentesis</td>')
assert i0 > 0, 'p5 row anchor missing'
i0 = p.rfind('<tr', 0, i0)
i1 = p.find('<tr style="background: #0b0b5b;"><td style="padding: 6px 10px; font: 700 13px', i0)
assert i1 > i0, 'p5 total anchor missing'
p = p[:i0] + body + '\n              ' + p[i1:]
p = swap(p, [
 ('color: #ffffff;">54</td>', 'color: #ffffff;">%d</td>' % QUAL),
 ('color: #ffffff;">$262,234</td>', 'color: #ffffff;">%s</td>' % m0(sum(proc[k]['hosp'] for k in ORDER))),
 ("color: #02cd3b;\">$233,810</td>", "color: #02cd3b;\">%s</td>" % m0(SAV)),
 ('What This Means for Empath', 'What This Means for ' + PARTNER),
 ('>$2,805,722</div>', '>%s</div>' % m0(ANN)),
])
hosp_txt = ('Under the Medicare hospice benefit %s is paid a per diem for each day a patient is on service, '
 'and care related to the terminal diagnosis is paid out of that per diem rather than billed to Medicare '
 'separately. Across the counties %s&rsquo;s July visits resolved to, the FY2026 routine home care rate for '
 'the first 60 days runs from $208.24 per day in Pinellas to $220.42 in Miami-Dade, and general inpatient '
 'care from $1,087.94 to $1,149.01 per day. A hospital encounter avoided is cost %s would have carried '
 'against the same per diem it was already receiving. This report makes no claim about what %s pays any '
 'contracted hospital.' % (PARTNER, PARTNER, PARTNER, PARTNER))
p = re.sub(r'Under the Medicare hospice benefit .*?contracted hospital\.', hosp_txt, p, flags=re.S)
PAGES.append(p)
print('p5 ok')

# ---------------- P6 savings by branch + upside ----------------
p = spine(T(6), 6)
bs = [(b, d) for b, d in BR.items()]
smax = bs[0][1]['sav']
sbars = ''.join('<div style="display: flex; flex-direction: column; justify-content: flex-end; height: 100%%; '
 'text-align: center;"><div style="font: 700 12px \'Libre Franklin\', sans-serif; color: %s; margin-bottom: 4px;">%s</div>'
 '<div style="background: %s; height: %.1f%%;"></div></div>'
 % (NAVY if i == 0 else MID, m0(d['sav']), BARCOL[min(i, len(BARCOL) - 1)],
    max(2.0, 100.0 * d['sav'] / smax)) for i, (b, d) in enumerate(bs))
p = block(p, 'grid-template-columns: repeat(6, 1fr); gap: 12px; align-items: end; height: 150px;',
 '<div style="display: grid; grid-template-columns: repeat(%d, 1fr); gap: 12px; align-items: end; '
 'height: 150px; margin-top: 8px;">%s</div>' % (len(bs), sbars))
slabels = ''.join('<div>%s</div>' % brlabel(b) for b, d in bs)
p = block(p, 'grid-template-columns: repeat(6, 1fr); gap: 12px; margin-top: 8px; font: 600 10px/1.35',
 '<div style="display: grid; grid-template-columns: repeat(%d, 1fr); gap: 12px; margin-top: 8px; '
 "font: 600 10px/1.35 'Libre Franklin', sans-serif; color: #0b0b5b; text-align: center;\">%s</div>"
 % (len(bs), slabels))
p = swap(p, [
 ('>54</td>', '>%d</td>' % QUAL),
 ('>$233,810</td>', '>%s</td>' % m0(SAV)),
 ('>68</td>', '>%d</td>' % round(QUAL * 1.25)),
 ('>$292,263</td>', '>%s</td>' % m0(SAV * 1.25)),
 ('>+$58,453</td>', '>+%s</td>' % m0(SAV * 0.25)),
 ('>81</td>', '>%d</td>' % round(QUAL * 1.5)),
 ('>$350,715</td>', '>%s</td>' % m0(SAV * 1.5)),
 ('>+$116,905</td>', '>+%s</td>' % m0(SAV * 0.5)),
 ('>108</td>', '>%d</td>' % (QUAL * 2)),
 ('>$467,620</td>', '>%s</td>' % m0(SAV * 2)),
 ('>+$233,810</td>', '>+%s</td>' % m0(SAV)),
])
PAGES.append(p)
print('p6 ok')

# ---------------- P7 year to date ----------------
YTD = [('April 2026', 'April', 23, 9, 34165.0),
       ('May 2026', 'May', 33, 12, 56596.0),
       ('June 2026', 'June', 53, 11, 50337.0),
       ('July 2026', 'July', N, QUAL, SAV)]
p = spine(T(7), 7)
vmax = max(v[4] for v in YTD)
step = 25000
axis_top = int((vmax // step + 1) * step)
ticks = list(range(0, axis_top + 1, step))
H, W = 190.0, 660.0
def y(v):
    return H - (v / axis_top) * H
xs = [W / len(YTD) * (i + 0.5) for i in range(len(YTD))]
svg = '<svg viewBox="0 0 660 198" style="width: 100%; height: 200px; overflow: visible;">'
for t in ticks:
    yy = y(t)
    svg += ('<line x1="0" y1="%.1f" x2="660" y2="%.1f" stroke="#e2e2ee" stroke-width="1"/>'
            '<text x="0" y="%.1f" font-family="Libre Franklin, sans-serif" font-size="9" fill="#a5a5c8">%s</text>'
            % (yy, yy, yy - 4, m0(t)))
seq = ['%.1f %.1f' % (xs[i], y(v[4])) for i, v in enumerate(YTD)]
svg += '<path d="M %.1f %.1f L %s L %.1f %.1f Z" fill="#5b5b9a" opacity="0.12"/>' % (
    xs[0], H, ' L '.join(seq), xs[-1], H)
svg += '<path d="M %s" fill="none" stroke="#0b0b5b" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>' % (' L '.join(seq))
for i, v in enumerate(YTD):
    last = (i == len(YTD) - 1)
    svg += ('<circle cx="%.1f" cy="%.1f" r="%d" fill="%s" stroke="#0b0b5b" stroke-width="2"/>'
            % (xs[i], y(v[4]), 5 if last else 4, '#0b0b5b' if last else '#ffffff'))
for i, v in enumerate(YTD):
    svg += ('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="Libre Franklin, sans-serif" '
            'font-size="12" font-weight="700" fill="#0b0b5b">%s</text>' % (xs[i], y(v[4]) - 13, m0(v[4])))
svg += '</svg>'
i0 = p.find('<svg viewBox="0 0 660 198"')
i1 = p.find('</svg>', i0) + 6
p = p[:i0] + svg + p[i1:]
lab = ''.join('<div>%s<div style="font-weight: 400; color: #5b5b9a; margin-top: 2px;">%d qualifying</div></div>'
              % (v[1], v[3]) for v in YTD)
p = block(p, 'grid-template-columns: repeat(4, 1fr); gap: 26px; margin-top: 8px; font: 600 11px/1.35',
 '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 26px; margin-top: 8px; '
 "font: 600 11px/1.35 'Libre Franklin', sans-serif; color: #0b0b5b; text-align: center;\">\n              %s\n            </div>" % lab)
tv = sum(v[2] for v in YTD); tq = sum(v[3] for v in YTD); ts = sum(v[4] for v in YTD)
rows = ''.join('<tr style="border-bottom: 1px solid #a5a5c8;%s"><td style="padding: 9px 10px;">%s</td>'
 '<td style="padding: 9px 10px; text-align: right;">%d</td>'
 '<td style="padding: 9px 10px; text-align: right;">%d</td>'
 '<td style="padding: 9px 10px; text-align: right; font-weight: 600; color: #0b0b5b;">%s</td></tr>'
 % (' background: #f7f7fb;' if i % 2 else '', v[0], v[2], v[3], m0(v[4])) for i, v in enumerate(YTD))
i0 = p.find('<td style="padding: 9px 10px;">April 2026</td>')
assert i0 > 0, 'ytd row anchor missing'
i0 = p.rfind('<tr', 0, i0)
i1 = p.find('YEAR TO DATE', i0)
assert i1 > i0, 'ytd total anchor missing'
i1 = p.rfind('<tr', 0, i1)
p = p[:i0] + rows + '\n              ' + p[i1:]
p = swap(p, [
 ('187 qualifying visits of 472 completed', '%d qualifying visits of %d completed' % (tq, tv)),
 ('>$860,813</div>', '>%s</div>' % m0(ts)),
])
i1 = p.find('YEAR TO DATE')
tail = p[i1:]
tail = re.sub(r'>472<', '>%d<' % tv, tail, count=1)
tail = re.sub(r'>187<', '>%d<' % tq, tail, count=1)
tail = re.sub(r'>\$860,813<', '>%s<' % m0(ts), tail, count=1)
p = p[:i1] + tail
p = p.replace('delivered for Empath since', 'delivered for %s since' % PARTNER)
PAGES.append(p)
print('p7 ok')

# ---------------- P8 recurring patients ----------------
REC = D['recurring']
rvis = sum(r[3] for r in REC)
rdiv = sum(r[4] for r in REC)
rsav = sum(r[5] for r in REC)
p = spine(T(8), 8)
p = swap(p, [
 ('sans-serif; color: #0b0b5b;">12</div>', 'sans-serif; color: #0b0b5b;">%d</div>' % len(REC)),
 ('sans-serif; color: #0b0b5b;">30</div>', 'sans-serif; color: #0b0b5b;">%d</div>' % rvis),
 ('Visits, 25.4% of Volume', 'Visits, %s of Volume' % pct(rvis, N)),
 ('sans-serif; color: #0b0b5b;">100%</div>', 'sans-serif; color: #0b0b5b;">%s</div>' % pct(rdiv, rvis)),
 ('color: #02cd3b;">$86,787</div>', 'color: #02cd3b;">%s</div>' % m0(rsav)),
])
def svcname(s):
    parts = [x.strip() for x in s.split('/')]
    if len(parts) > 1 and all('Paracentesis' in x for x in parts):
        return 'Paracentesis (performed and eval)'
    return esc(s)
rrows = ''.join('<tr style="border-bottom: 1px solid #a5a5c8;%s">'
 '<td style="padding: 8px 10px;">%s</td><td style="padding: 8px 10px;">%s</td>'
 '<td style="padding: 8px 10px;">%s</td>'
 '<td style="padding: 8px 10px; text-align: center; font-weight: 700; color: #0b0b5b;">%d</td>'
 '<td style="padding: 8px 10px; text-align: center; font-weight: 600;">%d</td>'
 '<td style="padding: 8px 10px; text-align: right; font-weight: 600; color: #0b0b5b;">%s</td></tr>'
 % (' background: #f7f7fb;' if i % 2 else '', hid(r[0]), esc(r[1]), svcname(r[2]), r[3], r[4],
    m0(r[5]) if r[5] else '&#8211;')
 for i, r in enumerate(REC))
i0 = p.find('<tbody><tr style="border-bottom: 1px solid #a5a5c8;">')
assert i0 > 0, 'p8 tbody anchor missing'
i1 = p.find('</tbody>', i0)
p = p[:i0] + '<tbody>' + rrows + p[i1:]
PAGES.append(p)
print('p8 ok')

# ---------------- branch pages ----------------
ELL44 = ('<svg viewBox="0 0 400 44" preserveAspectRatio="none" style="position: absolute; left: -10px; '
 'top: -12px; width: calc(100% + 20px); height: 45px; pointer-events: none; overflow: visible;">'
 '<path d="M 397 19 C 399 33 331 42 199 42 C 70 42 3 34 3 22 C 3 10 70 2 199 2 C 328 2 397 8 396 20 '
 'C 395 33 380 40 348 42" fill="none" stroke="#02cd3b" stroke-width="2" stroke-linecap="round" '
 'stroke-linejoin="round" vector-effect="non-scaling-stroke" opacity="0.9"/></svg>')
BSEG = {'High Complexity': '#0b0b5b', 'Moderate Complexity': '#5b5b9a', 'Telemedicine': '#8d8db8',
        'Low Complexity': '#c4c4dd', 'No Charge': '#ff0000'}
ROWS_MAIN = 13
TPL_MAIN = T(9)
TPL_CONT = T(10)

def vrow(r):
    return ('<tr style="border-bottom: 1px solid #e2e2ee;">'
     '<td style="padding: 4px 6px;">%s</td><td style="padding: 4px 6px;">%s</td>'
     '<td style="padding: 4px 6px;">%s</td><td style="padding: 4px 6px;">%s</td>'
     '<td style="padding: 4px 6px;">%s</td></tr>'
     % (esc(r[0]), hid(r[1]), esc(r[2]), esc(r[3]), esc(r[4])))

def replace_tbody(page, rows, nth=0):
    i0 = page.find('<tbody>', page.find('Patient Visit Detail'))
    i1 = page.find('</tbody>', i0)
    return page[:i0] + '<tbody>' + ''.join(vrow(r) for r in rows) + page[i1:]

def branch_main(bname, d, num, rank, nb):
    p = TPL_MAIN
    p = re.sub(r"(sans-serif; color: #a5a5c8;\">)\d\d(</div>)",
               lambda mm: mm.group(1) + '%02d' % num + mm.group(2), p, count=1)
    p = p.replace('color: #ffffff; letter-spacing: -0.01em;">Suncoast Pinellas</div>',
                  'color: #ffffff; letter-spacing: -0.01em;">%s</div>' % esc(bname))
    p = p.replace('<div>Suncoast Pinellas | July 2026</div>', '<div>%s | July 2026</div>' % esc(bname))
    p = p.replace("sans-serif; color: #ffffff;\">44</div>", "sans-serif; color: #ffffff;\">%d</div>" % d['n'])
    p = p.replace("sans-serif; color: #ffffff;\">100%</div>",
                  "sans-serif; color: #ffffff;\">%s</div>" % pct(d['div'], d['n']))
    p = p.replace("color: #02cd3b;\">$95,081</div>", "color: #02cd3b;\">%s</div>" % m0(d['sav']))
    # narrative
    top = d['svc'][0]
    ac = sorted(d['acu'], key=lambda x: -x[1])
    q = sum(c for s, c in d['svc'] if s in BENCH)
    lead = 'SOS completed %d visit%s for %s in July 2026, %s of %s’s total volume%s.' % (
        d['n'], '' if d['n'] == 1 else 's', esc(bname), pct(d['n'], N), PARTNER,
        ', and the highest of any branch' if rank == 0 else '')
    s2 = '%s led at %d visit%s.' % (esc(top[0]), top[1], '' if top[1] == 1 else 's')
    if len(ac) > 1:
        s3 = 'The acuity mix was led by %s at %d and %s at %d.' % (ac[0][0], ac[0][1], ac[1][0], ac[1][1])
    else:
        s3 = 'Every visit was %s.' % ac[0][0]
    if q:
        s4 = '%d visit%s qualified for the savings model, accounting for an estimated %s in avoided hospital cost.' % (
            q, '' if q == 1 else 's', m0(d['sav']))
    else:
        s4 = 'No visits qualified for the savings model this month.'
    narr = ' '.join([lead, s2, s3, s4])
    p = re.sub(r'SOS completed 44 visits for Suncoast Pinellas.*?avoided hospital cost\.', narr, p, flags=re.S)
    # services table
    smax = d['svc'][0][1]
    srows = ''
    for i, (s, c) in enumerate(d['svc']):
        w = 100.0 * c / smax
        col = NAVY if i == 0 else (MID if w >= 40 else LILAC)
        srows += ('<tr style="border-bottom: 1px solid #e2e2ee;"><td style="padding: 4px 6px;">%s</td>'
         '<td style="padding: 4px 0; width: 70px;"><div style="height: 8px; background: %s; width: %d%%;">'
         '</div></td><td style="padding: 4px 6px; text-align: right;">%d</td></tr>'
         % (esc(s), col, int(round(w)), c))
    srows += ('<tr style="background: #f2f2f7;"><td style="padding: 5px 6px; font-weight: 700; color: #0b0b5b;">'
     'TOTAL</td><td></td><td style="padding: 5px 6px; text-align: right; font-weight: 700; color: #0b0b5b;">'
     '%d</td></tr>' % d['n'])
    p = block(p, 'position: relative; padding-top: 3px;',
        '<div style="position: relative; padding-top: 3px;"><table style="width: 100%; '
        "border-collapse: collapse; font: 400 10.5px 'Libre Franklin', sans-serif; color: #33335c;\">"
        '<tbody>' + srows + '</tbody></table>' + ELL44 + '</div>')
    # complexity
    ad = dict(d['acu'])
    seq = [(a, ad.get(a, 0)) for a in ACUORD]
    segs = ''.join('<div style="width: %.1f%%; background: %s;"></div>' % (100.0 * c / d['n'], BSEG[a])
                   for a, c in seq if c)
    p = block(p, 'display: flex; height: 20px;',
              '<div style="display: flex; height: 20px;">%s</div>' % segs)
    leg = ''.join('<div style="display: flex; justify-content: space-between;%s"><div>'
     '<span style="display: inline-block; width: 9px; height: 9px; background: %s; margin-right: 6px;">'
     '</span>%s</div><div%s>%d &middot; %s</div></div>'
     % ('' if c else ' color: #c4c4dd;', BSEG[a], a,
        ' style="font-weight: 600;"' if c and c == max(x[1] for x in seq) else '', c, pct(c, d['n']))
     for i, (a, c) in enumerate(seq))
    p = block(p, 'gap: 4px; margin-top: 10px; font: 400 10.5px',
        '<div style="display: flex; flex-direction: column; gap: 4px; margin-top: 10px; '
        "font: 400 10.5px 'Libre Franklin', sans-serif; color: #33335c;\">" + leg + '</div>')
    p = re.sub(r'Every one of the 44 completed visits prevented a referral to an outside care setting\.',
        ('Every one of the %d completed visits prevented a referral to an outside care setting.' % d['n'])
        if d['div'] == d['n'] else
        ('%d of the %d completed visits prevented a referral to an outside care setting.' % (d['div'], d['n'])), p)
    p = replace_tbody(p, d['rows'][:ROWS_MAIN])
    return p

def branch_cont(bname, d, num):
    p = TPL_CONT
    p = re.sub(r"(sans-serif; color: #a5a5c8;\">)\d\d(</div>)",
               lambda mm: mm.group(1) + '%02d' % num + mm.group(2), p, count=1)
    p = p.replace('letter-spacing: -0.01em; margin-bottom: 18px;">Suncoast Pinellas</div>',
                  'letter-spacing: -0.01em; margin-bottom: 18px;">%s</div>' % esc(bname))
    p = p.replace('<div>Suncoast Pinellas | July 2026</div>', '<div>%s | July 2026</div>' % esc(bname))
    p = replace_tbody(p, d['rows'][ROWS_MAIN:])
    return p

num = 9
for rank, (bname, d) in enumerate(BR.items()):
    PAGES.append(branch_main(bname, d, num, rank, len(BR)))
    num += 1
    if len(d['rows']) > ROWS_MAIN:
        PAGES.append(branch_cont(bname, d, num))
        num += 1
print('branch pages ok, total now', len(PAGES), 'next num', num)

# ---------------- disclaimers ----------------
p = spine(T(17), num)
p = p.replace('Empath', PARTNER)
old_scope = ('Of the 118 visits SOS completed for %s in July 2026, 54 carry a published hospital '
             'benchmark and appear in the savings figures; the remaining 64 are excluded entirely.' % PARTNER)
assert old_scope in p, 'disclaimer scope sentence missing'
p = p.replace(old_scope,
    'Of the %d visits SOS completed for %s in July 2026, %d carry a published hospital benchmark and '
    'appear in the savings figures; the remaining %d are excluded entirely.' % (N, PARTNER, QUAL, N - QUAL))
PAGES.append(p)

head = open('tpl/_head.html').read()
tail = open('tpl/_tail.html').read()
head = head.replace('<title>MPU Empath July 2026</title>', '<title>MPU AccentCare July 2026</title>')
head = head.replace('Empath', PARTNER)
out = head + '\n'.join(PAGES) + tail
open('MPU_AccentCare_July_2026.html', 'w').write(out)
print('WROTE', len(PAGES), 'pages', len(out), 'bytes')
