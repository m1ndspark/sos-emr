import json, re

D = json.load(open('innovage_july.json'))
PARTNER = 'InnoVage'
N = D['n']
DONE = D['done']
OPEN = D['open']
SITES = D['sites']
NAVY = '#0b0b5b'
DEEP = '#0d155c'
MID = '#5b5b9a'
LILAC = '#a5a5c8'
PALE = '#c4c4dd'
GREEN = '#02cd3b'
GREY = '#f2f2f7'
F = "'Libre Franklin', sans-serif"
SITE_ORDER = ['Orlando', 'Tampa']
WD = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def pct(a, b):
    if not b:
        return '0%'
    v = 100.0 * a / b
    return '%d%%' % round(v) if v in (0.0, 100.0) else '%.1f%%' % v


def shell(num, spine_text, body, pad='42px 48px 38px 42px', mark_top=62, spine_pad=116):
    return (
     '<div class="page">\n'
     '<div style="width: 100%%; height: 100%%; background: #ffffff; display: flex; box-sizing: border-box; '
     'font-family: %s;">\n'
     '        <div style="width: 56px; background: %s; position: relative; display: flex; flex-direction: column; '
     'justify-content: space-between; align-items: center; padding: %dpx 0 28px; box-sizing: border-box;">\n'
     '          <div class="sosmark" style="position: absolute; top: %dpx; left: 50%%; transform: translateX(-50%%); '
     'width: 36px; height: 36px;"></div>\n'
     '          <div style="writing-mode: vertical-rl; transform: rotate(180deg); font: 600 11px %s; '
     'letter-spacing: 0.26em; text-transform: uppercase; color: %s;">%s</div>\n'
     '          <div style="font: 600 12px %s; color: %s;">%02d</div>\n'
     '        </div>\n'
     '        <div style="flex: 1; padding: %s; box-sizing: border-box; display: flex; flex-direction: column; '
     'justify-content: flex-start; gap: 22px;">\n%s\n        </div>\n      </div>\n</div>'
     % (F, DEEP, spine_pad, mark_top, F, LILAC, spine_text, F, LILAC, num, pad, body))


def title(section, heading, sub=''):
    s = ('          <div>\n'
         '            <div style="font: 800 12px %s; letter-spacing: 0.2em; text-transform: uppercase; '
         'color: %s; margin-bottom: 6px;">%s</div>\n'
         '            <div style="font: 700 30px %s; color: %s; letter-spacing: -0.01em;">%s</div>\n'
         % (F, MID, section, F, NAVY, heading))
    if sub:
        s += ('            <div style="font: 400 12.5px/1.6 %s; color: #000000; margin-top: 10px;">%s</div>\n'
              % (F, sub))
    return s + '          </div>'


def rule(label):
    return ('<div style="font: 700 12px %s; letter-spacing: 0.1em; text-transform: uppercase; color: %s; '
            'border-bottom: 2px solid %s; padding-bottom: 6px; margin-bottom: 10px;">%s</div>'
            % (F, NAVY, NAVY, label))


def kpis(items):
    cells = ''
    for i, (v, lab) in enumerate(items):
        last = (i == len(items) - 1)
        cells += ('<div style="background: %s; padding: 20px 18px; text-align: center;">'
                  '<div style="font: 700 34px %s; color: %s;">%s</div>'
                  '<div style="font: 500 12px %s; color: %s; margin-top: 6px;">%s</div></div>'
                  % ('#0b0b5b' if last else '#ffffff', F, GREEN if last else NAVY, v,
                     F, LILAC if last else MID, lab))
    return ('          <div style="display: grid; grid-template-columns: repeat(%d, 1fr); gap: 1px; '
            'background: %s; border: 1px solid %s;">%s</div>' % (len(items), LILAC, LILAC, cells))


def callout(text, color=GREEN, size='15px/1.65'):
    return ('          <div style="border-left: 4px solid %s; padding: 4px 0 4px 20px; font: 400 %s %s; '
            'color: %s;">%s</div>' % (color, size, F, DEEP, text))


def note(head, text, bar=MID):
    return ('          <div style="background: %s; border-left: 4px solid %s; padding: 12px 18px; '
            'font: 400 11px/1.6 %s; color: #000000;"><strong>%s</strong> %s</div>' % (GREY, bar, F, head, text))


def twocol(pairs):
    cells = ''
    for h, t in pairs:
        cells += ('<div><div style="font: 700 13px %s; letter-spacing: 0.12em; text-transform: uppercase; '
                  'color: %s; border-bottom: 2px solid %s; padding-bottom: 8px; margin-bottom: 12px;">%s</div>'
                  '<div style="font: 400 13.5px/1.6 %s; color: #000000;">%s</div></div>'
                  % (F, NAVY, NAVY, h, F, t))
    return ('          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px 36px;">%s</div>' % cells)


def table(cols, rows, widths=None, fontsize='11px', headpad='7px 10px', bodypad='6px 10px', total=None):
    th = ''
    for i, c in enumerate(cols):
        al = 'right' if (widths and widths[i] == 'r') else ('center' if (widths and widths[i] == 'c') else 'left')
        th += '<td style="padding: %s; text-align: %s;">%s</td>' % (headpad, al, c)
    tb = ''
    for n, r in enumerate(rows):
        tds = ''
        for i, c in enumerate(r):
            al = 'right' if (widths and widths[i] == 'r') else ('center' if (widths and widths[i] == 'c') else 'left')
            tds += '<td style="padding: %s; text-align: %s;">%s</td>' % (bodypad, al, c)
        tb += ('<tr style="border-bottom: 1px solid %s;%s">%s</tr>'
               % (LILAC, ' background: #f7f7fb;' if n % 2 else '', tds))
    if total:
        tds = ''
        for i, c in enumerate(total):
            al = 'right' if (widths and widths[i] == 'r') else ('center' if (widths and widths[i] == 'c') else 'left')
            tds += ('<td style="padding: %s; text-align: %s; font-weight: 700; color: #ffffff;">%s</td>'
                    % (bodypad, al, c))
        tb += '<tr style="background: %s;">%s</tr>' % (NAVY, tds)
    return ('<table style="width: 100%%; border-collapse: collapse; font: 400 %s %s; color: #000000; '
            'border: 1px solid %s;"><thead><tr style="background: %s; font: 700 9px %s; color: #ffffff; '
            'text-transform: uppercase; letter-spacing: 0.07em;">%s</tr></thead><tbody>%s</tbody></table>'
            % (fontsize, F, LILAC, NAVY, F, th, tb))


def spacer():
    return '          <div style="flex: 1 0 0;"></div>'


def footer(right, modeled=False):
    left = 'SOS Mobile Medical Care, Monthly Partner Utilization - Confidential'
    if modeled:
        left += ' &middot; Modeled estimates; see Disclaimers'
    return ('          <div style="display: flex; justify-content: space-between; border-top: 1px solid %s; '
            'padding-top: 12px; font: 400 11px %s; color: %s;"><div>%s</div><div>%s</div></div>'
            % (LILAC, F, LILAC, left, right))


SPINE = PARTNER + ' &middot; July 2026'
FOOT = PARTNER + ' | July 2026'
PAGES = []

# ---------------- P1 cover ----------------
cover = open('tpl/p01.html').read()
cover = cover.replace('color: #0d155c;">Empath</div>', 'color: #0d155c;">%s</div>' % PARTNER)
PAGES.append(cover)

# ---------------- P2 executive summary ----------------
o, t = SITES['Orlando'], SITES['Tampa']
tat0 = D['tat'].get('0', D['tat'].get(0, 0))
tat1 = D['tat'].get('1', D['tat'].get(1, 0))
lead = D['prov'][0]
body = '\n'.join([
 title('Section 01', 'Executive Summary'),
 kpis([(str(N), 'Referrals Received'), (str(DONE), 'Evals Completed'),
       (pct(DONE, N), 'Completion Rate'), (str(len(OPEN)), 'Open at Cutoff')]),
 callout('SOS Mobile Medical Care received <strong>%d</strong> Cares/3008 evaluation referrals from %s in '
         'July 2026 and completed <strong>%d</strong> of them within the month, a completion rate of '
         '<strong>%s</strong>. Every completed evaluation closed within one business day of the referral '
         'being received.' % (N, PARTNER, DONE, pct(DONE, N))),
 twocol([
  ('Volume by Site', 'Orlando accounted for %d referrals (%s) and %d completed evaluations. Tampa accounted '
   'for %d referrals (%s) and %d completed evaluations.'
   % (o['n'], pct(o['n'], N), o['done'], t['n'], pct(t['n'], N), t['done'])),
  ('Turnaround', 'All %d completed evaluations closed within one business day. %d closed the same business '
   'day (%s) and %d closed the next (%s).' % (DONE, tat0, pct(tat0, DONE), tat1, pct(tat1, DONE))),
  ('Provider Coverage', '%s completed %d evaluations (%s), with %d additional providers covering the '
   'remainder.' % (esc(lead[0]), lead[1], pct(lead[1], DONE), len(D['prov']) - 1)),
  ('Open Referrals', '%d referrals had not been completed as of the reporting cutoff. %d of them arrived in '
   'the last three days of the month.'
   % (len(OPEN), sum(1 for x in OPEN if int(x['refdate'][3:5]) >= 29))),
 ]),
 note('Reporting basis.', 'Referral counts come from the SOS referral record and completion counts from the '
      'SOS 3008 completion log, joined on referral ID. A referral is counted complete only when a matching '
      'completion is on file. Each referral is attributed to the site it was routed to, so a referral and its '
      'evaluation are always counted at the same site.'),
 spacer(), footer(FOOT)])
PAGES.append(shell(2, SPINE, body, pad='48px 56px 44px 48px', mark_top=73, spine_pad=127))

# ---------------- P3 referral volume and distribution ----------------
HRS = list(range(0, 24, 2))
g = D['grid']
gmax = max(g.values())
wdc = {int(k): v for k, v in D['wd_counts'].items()}
hdr_cells = ''.join('<td style="padding: 4px 2px; text-align: center; font: 700 8.5px %s; color: %s;">%02d</td>'
                    % (F, MID, h) for h in HRS)
grid_rows = ''
for w in range(7):
    cells = ''
    for h in HRS:
        v = g.get('%d|%02d' % (w, h), 0)
        if v == 0:
            bg, col = '#f7f7fb', '#c4c4dd'
        else:
            r = v / float(gmax)
            bg = '#0b0b5b' if r > 0.75 else ('#3d3d80' if r > 0.5 else ('#7a7ab0' if r > 0.25 else '#c4c4dd'))
            col = '#ffffff' if r > 0.25 else NAVY
        cells += ('<td style="padding: 5px 2px; text-align: center; background: %s; color: %s; '
                  'font: 600 10px %s; border: 1px solid #ffffff;">%s</td>' % (bg, col, F, v or ''))
    grid_rows += ('<tr><td style="padding: 5px 8px 5px 0; font: 600 10px %s; color: %s; white-space: nowrap;">%s</td>'
                  '%s<td style="padding: 5px 0 5px 8px; font: 700 10px %s; color: %s; text-align: right;">%d</td></tr>'
                  % (F, NAVY, WD[w], cells, F, NAVY, wdc.get(w, 0)))
top2 = sorted(wdc.items(), key=lambda x: -x[1])[:2]
peakcell = max(g.items(), key=lambda x: x[1])
pw, ph = peakcell[0].split('|')
smax = max(SITES[s2]['n'] for s2 in SITE_ORDER)
sbars = ''.join('<div style="display: flex; flex-direction: column; justify-content: flex-end; height: 100%%; '
 'text-align: center;"><div style="font: 700 13px %s; color: %s; margin-bottom: 4px;">%d</div>'
 '<div style="background: %s; height: %.1f%%;"></div></div>'
 % (F, NAVY if i2 == 0 else MID, SITES[s2]['n'], [NAVY, MID][i2], 100.0 * SITES[s2]['n'] / smax)
 for i2, s2 in enumerate(SITE_ORDER))
slab = ''.join('<div>%s<div style="font-weight: 400; color: %s; margin-top: 2px;">%s</div></div>'
 % (s2, MID, pct(SITES[s2]['n'], N)) for s2 in SITE_ORDER)
site_rows = [[s2, str(SITES[s2]['n']), pct(SITES[s2]['n'], N), str(SITES[s2]['done']),
              str(SITES[s2]['open']), pct(SITES[s2]['done'], SITES[s2]['n'])] for s2 in SITE_ORDER]
body = '\n'.join([
 title('Section 02', 'Referral Volume and Distribution',
       'Every referral received in the period, placed by the weekday and two-hour window in which it was '
       'submitted. Darker cells carry more referrals.'),
 '          <div>' +
 '<table style="width: 100%%; border-collapse: collapse;"><thead><tr><td></td>%s'
 '<td style="padding: 4px 0 4px 8px; text-align: right; font: 700 8.5px %s; color: %s;">TOTAL</td></tr>'
 '</thead><tbody>%s</tbody></table>' % (hdr_cells, F, MID, grid_rows) +
 '<div style="font: 400 10px/1.5 %s; color: %s; margin-top: 8px;">%s and %s together carried %s of all '
 'referrals, and the busiest window was %s between %s:00 and %s:00 with %d. %d referrals arrived outside '
 '08:00 to 18:00 and %d arrived on a weekend.</div>'
 % (F, MID, WD[top2[0][0]], WD[top2[1][0]], pct(top2[0][1] + top2[1][1], N), WD[int(pw)], ph,
    '%02d' % (int(ph) + 2), peakcell[1], D['offhours'], D['weekend']) + '</div>',
 '          <div style="display: grid; grid-template-columns: 0.85fr 1.6fr; gap: 30px; align-items: start;">\n'
 '            <div>' + rule('Referrals by Site') +
 '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; align-items: end; '
 'height: 96px;">%s</div>' % sbars +
 '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; margin-top: 8px; '
 'font: 600 10.5px/1.35 %s; color: %s; text-align: center;">%s</div>' % (F, NAVY, slab) + '</div>\n'
 '            <div>' + rule('Completion by Site') +
 table(['Site', 'Referrals', 'Share', 'Completed', 'Open', 'Completion Rate'], site_rows,
       widths=['l', 'r', 'r', 'r', 'r', 'r'], fontsize='11.5px', bodypad='6px 10px',
       total=['TOTAL', str(N), '100%', str(DONE), str(len(OPEN)), pct(DONE, N)]) + '</div>\n'
 '          </div>',
 note('Site attribution.', 'Each evaluation is counted at the site its referral was routed to. The SOS '
      'completion log records the site at the point of completion, which differs on four July records; '
      'this report uses the referral routing so that referrals and completions share one denominator.'),
 spacer(), footer(FOOT)])
PAGES.append(shell(3, SPINE, body))
print('p3 ok')

# ---------------- P5 provider coverage and turnaround ----------------
prov_rows = [[esc(p), str(c), pct(c, DONE)] for p, c in D['prov']]
tatd = {int(k): v for k, v in D['tat'].items()}
tmax = max(tatd.values())
tbars = ''
for k in sorted(tatd):
    lab = 'Same business day' if k == 0 else ('Next business day' if k == 1 else '%d business days' % k)
    tbars += ('<div style="display: grid; grid-template-columns: 140px 1fr 66px; gap: 10px; align-items: center; '
              'font: 400 11px %s; color: #000000;"><div style="text-align: right;">%s</div>'
              '<div><div style="height: 14px; background: %s; width: %.1f%%;"></div></div>'
              '<div style="font-weight: 600;">%d &middot; %s</div></div>'
              % (F, lab, NAVY if tatd[k] == tmax else MID, 100.0 * tatd[k] / tmax, tatd[k], pct(tatd[k], DONE)))
tbars += ('<div style="display: grid; grid-template-columns: 140px 1fr 66px; gap: 10px; align-items: center; '
          'font: 700 11px %s; color: %s; border-top: 1px solid %s; padding-top: 8px; margin-top: 2px;">'
          '<div style="text-align: right;">TOTAL</div><div></div><div>%d &middot; %s</div></div>'
          % (F, NAVY, LILAC, sum(tatd.values()), pct(sum(tatd.values()), DONE)))
sos_rows = [[esc(p), str(c), pct(c, DONE)] for p, c in D['sosprov']]
body = '\n'.join([
 title('Section 03', 'Provider Coverage and Turnaround'),
 '          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px 30px;">\n'
 '            <div>' + rule('Evaluations by Provider') +
 table(['Provider', 'Count', '% of Total'], prov_rows, widths=['l', 'r', 'r'], fontsize='11.5px',
       total=['TOTAL', str(DONE), '100%']) + '</div>\n'
 '            <div>' + rule('SOS Provider of Record') +
 table(['Provider', 'Count', '% of Total'], sos_rows, widths=['l', 'r', 'r'], fontsize='11.5px',
       total=['TOTAL', str(DONE), '100%']) + '</div>\n          </div>',
 '          <div>' + rule('Turnaround, Business Days from Referral to Completion') +
 '<div style="display: flex; flex-direction: column; gap: 8px; margin-top: 4px;">%s</div>' % tbars +
 '<div style="font: 400 10px/1.5 %s; color: %s; margin-top: 8px;">Turnaround is measured in business days. '
 'Evaluations are not performed on weekends, so a Friday referral completed the following Monday counts as '
 'one business day.</div>' % (F, MID) + '</div>',
 note('What this shows.', 'Every one of the %d completed evaluations closed within one business day, and %s '
      'closed the same business day. No evaluation in the period took longer than one business day, so the '
      'window in which a referral arrives is the only factor that moves turnaround.'
      % (DONE, pct(tat0, DONE)), bar=GREEN),
 spacer(), footer(FOOT)])
PAGES.append(shell(4, SPINE, body))
print('p4 ok')

# ---------------- P6 open referrals ----------------
orows = [[x['id'], x['refdate'], esc(x['name']), x['dob'], x['site'], 'Open'] for x in
         sorted(OPEN, key=lambda x: x['refdt'])]
late = sum(1 for x in OPEN if int(x['refdate'][3:5]) >= 29)
body = '\n'.join([
 title('Section 04', 'Open Referrals',
       'Referrals received in July with no matching completion on file as of the reporting cutoff.'),
 kpis([(str(len(OPEN)), 'Open at Cutoff'), (str(late), 'Received in Last Three Days'),
       (pct(len(OPEN), N), 'Share of Referrals'), (pct(DONE, N), 'Completion Rate')]),
 '          <div>' + table(['Referral ID', 'Referral Date', 'Patient Name', 'DOB', 'Site', 'Status'], orows,
       widths=['l', 'l', 'l', 'l', 'l', 'l'], fontsize='11.5px', bodypad='8px 10px') + '</div>',
 note('Status basis.', 'Status is derived from the SOS 3008 completion log dated through 07/31/2026, which is '
      'the most recent log on file. A referral shows as open only because no completion has been recorded '
      'against it in that log; several of these may have been evaluated in August. Refresh this page against '
      'the August log before issuing.'),
 note('Duplicate referral.', 'Two July referrals were submitted for the same patient, one of which was '
      'completed. The earlier referral remains open and is listed above.'),
 spacer(), footer(FOOT)])
PAGES.append(shell(5, SPINE, body))
print('p5 ok')

# ---------------- site pages ----------------
SITE_MAIN = 16
SITE_CONT = 34

def band(site, d):
    return ('        <div style="background: %s; padding: 32px 48px 28px 42px; display: flex; '
     'justify-content: space-between; align-items: center;"><div>'
     '<div style="font: 800 11px %s; letter-spacing: 0.2em; text-transform: uppercase; color: %s; '
     'margin-bottom: 6px;">Site Detail</div>'
     '<div style="font: 700 28px %s; color: #ffffff; letter-spacing: -0.01em;">3008 %s</div></div>'
     '<div style="display: flex; gap: 32px; text-align: right;">'
     '<div><div style="font: 700 26px %s; color: #ffffff;">%d</div>'
     '<div style="font: 400 10px %s; color: %s; margin-top: 2px;">Referrals</div></div>'
     '<div><div style="font: 700 26px %s; color: #ffffff;">%d</div>'
     '<div style="font: 400 10px %s; color: %s; margin-top: 2px;">Completed</div></div>'
     '<div><div style="font: 700 26px %s; color: %s;">%s</div>'
     '<div style="font: 400 10px %s; color: %s; margin-top: 2px;">Completion Rate</div></div>'
     '</div></div>' % (NAVY, F, LILAC, F, site, F, d['n'], F, LILAC, F, d['done'], F, LILAC,
                       F, GREEN, pct(d['done'], d['n']), F, LILAC))

def detail_table(rows):
    tr = ''
    for r in rows:
        opened = (r['status'] != 'Completed')
        tr += ('<tr style="border-bottom: 1px solid #e2e2ee;%s">'
         '<td style="padding: 4px 6px; text-align: center;">%d</td>'
         '<td style="padding: 4px 6px;">%s</td><td style="padding: 4px 6px;">%s</td>'
         '<td style="padding: 4px 6px;">%s</td><td style="padding: 4px 6px;">%s</td>'
         '<td style="padding: 4px 6px;">%s</td><td style="padding: 4px 6px;">%s</td></tr>'
         % (' background: #fdf6e3;' if opened else '', r['day'], r['id'], r['refdate'],
            esc(r['name']), r['dob'], 'Open' if opened else 'Completed',
            r['completed'] or '&#8211;'))
    return ('<table style="width: 100%%; border-collapse: collapse; font: 400 10px %s; color: #33335c;">'
     '<thead><tr style="background: %s; font: 700 9px %s; color: %s; text-transform: uppercase; '
     'letter-spacing: 0.08em;"><td style="padding: 5px 6px; text-align: center;">Day</td>'
     '<td style="padding: 5px 6px;">Referral ID</td><td style="padding: 5px 6px;">Referral Date</td>'
     '<td style="padding: 5px 6px;">Patient Name</td><td style="padding: 5px 6px;">DOB</td>'
     '<td style="padding: 5px 6px;">Status</td><td style="padding: 5px 6px;">Completed</td></tr></thead>'
     '<tbody>%s</tbody></table>' % (F, GREY, F, MID, tr))

def site_shell(num, site, inner):
    return ('<div class="page"><div style="width: 100%%; height: 100%%; background: #ffffff; display: flex; '
     'box-sizing: border-box; font-family: %s;"><div style="width: 56px; background: %s; position: relative; '
     'display: flex; flex-direction: column; justify-content: space-between; align-items: center; '
     'padding: 104px 0 28px; box-sizing: border-box;"><div class="sosmark" style="position: absolute; top: 50px; '
     'left: 50%%; transform: translateX(-50%%); width: 36px; height: 36px;"></div>'
     '<div style="writing-mode: vertical-rl; transform: rotate(180deg); font: 600 11px %s; '
     'letter-spacing: 0.26em; text-transform: uppercase; color: %s;">Site Detail &middot; July 2026</div>'
     '<div style="font: 600 12px %s; color: %s;">%02d</div></div>'
     '<div style="flex: 1; display: flex; flex-direction: column; box-sizing: border-box;">%s</div></div></div>'
     % (F, DEEP, F, LILAC, F, LILAC, num, inner))

def site_foot(site):
    return ('<div style="display: flex; justify-content: space-between; border-top: 1px solid %s; '
     'padding: 12px 48px 38px 42px; font: 400 11px %s; color: %s;">'
     '<div>SOS Mobile Medical Care, Monthly Partner Utilization - Confidential</div>'
     '<div>3008 %s | July 2026</div></div>' % (LILAC, F, LILAC, site))

num = 6
for site in SITE_ORDER:
    d = SITES[site]
    rows = d['rows']
    done_rows = [r for r in rows if r['status'] == 'Completed']
    prov = [[esc(p), str(c), pct(c, d['done'])] for p, c in d['prov']]
    td = {int(k): v for k, v in d['tat'].items()}
    same = td.get(0, 0)
    lead = d['prov'][0]
    inner = (band(site, d) +
     '<div style="flex: 1; padding: 28px 48px 38px 42px; display: flex; flex-direction: column; '
     'justify-content: flex-start; gap: 20px;">'
     '<div style="background: %s; border-left: 4px solid %s; padding: 14px 18px; font: 400 11px/1.6 %s; '
     'color: #000000;">%s routed %d of the %d July referrals (%s). %d were completed within the month and '
     '%d remained open at the cutoff. %s completed %d of them (%s). %s of the completed evaluations closed '
     'the same business day, and every one closed within one business day.</div>'
     % (GREY, MID, F, site, d['n'], N, pct(d['n'], N), d['done'], d['open'],
        esc(lead[0]), lead[1], pct(lead[1], d['done']), pct(same, d['done'])) +
     '<div style="display: grid; grid-template-columns: 1.1fr 1fr; gap: 24px;">'
     '<div>' + rule('Evaluations by Provider') +
     table(['Provider', 'Count', '% of Site'], prov, widths=['l', 'r', 'r'], fontsize='10.5px',
           bodypad='5px 8px', headpad='6px 8px', total=['TOTAL', str(d['done']), '100%']) + '</div>'
     '<div>' + rule('Turnaround') +
     '<div style="display: flex; flex-direction: column; gap: 6px; font: 400 10.5px %s; color: #000000;">'
     '<div style="display: flex; justify-content: space-between;"><div>Same business day</div>'
     '<div style="font-weight: 600;">%d &middot; %s</div></div>'
     '<div style="display: flex; justify-content: space-between;"><div>Next business day</div>'
     '<div>%d &middot; %s</div></div>'
     '<div style="display: flex; justify-content: space-between; font-weight: 700; color: %s; '
     'border-top: 1px solid %s; padding-top: 6px; margin-top: 2px;"><div>TOTAL</div>'
     '<div>%d &middot; %s</div></div></div>'
     % (F, same, pct(same, d['done']), td.get(1, 0), pct(td.get(1, 0), d['done']),
        NAVY, LILAC, sum(td.values()), pct(sum(td.values()), d['done'])) +
     '<div style="background: %s; border-left: 4px solid %s; padding: 12px 14px; margin-top: 14px; '
     'font: 400 11px/1.6 %s; color: #33335c;">Every completed evaluation at this site closed within one '
     'business day of the referral.</div>' % (GREY, GREEN, F) +
     '</div></div>'
     '<div style="display: flex; flex-direction: column;">' + rule('Referral and Evaluation Detail') +
     detail_table(rows[:SITE_MAIN]) + '</div>'
     '<div style="flex: 1 0 0;"></div></div>' + site_foot(site))
    PAGES.append(site_shell(num, site, inner))
    num += 1
    rest = rows[SITE_MAIN:]
    while rest:
        chunk, rest = rest[:SITE_CONT], rest[SITE_CONT:]
        body = '\n'.join([
         '          <div><div style="font: 800 11px %s; letter-spacing: 0.2em; text-transform: uppercase; '
         'color: %s; margin-bottom: 6px;">Site Detail</div>'
         '<div style="font: 700 28px %s; color: %s; letter-spacing: -0.01em;">3008 %s</div></div>'
         % (F, MID, F, NAVY, site),
         '          <div>' + rule('Referral and Evaluation Detail (Continued)') +
         detail_table(chunk) + '</div>',
         spacer(), footer('3008 %s | July 2026' % site)])
        PAGES.append(shell(num, 'Site Detail &middot; July 2026', body, mark_top=56, spine_pad=110))
        num += 1
print('site pages ok, next', num, 'total', len(PAGES))

# ---------------- disclaimers ----------------
DISC = [
 ('Scope', 'This report covers Cares/3008 evaluations only. SOS Mobile Medical Care performs no billable '
  'clinical procedures under the 3008 program, so no procedure savings model is applied and no cost '
  'avoidance figure appears anywhere in this report.'),
 ('Referral Source', 'Referral counts are drawn from the SOS referral record for July 2026 and cover every '
  'referral routed to a 3008 site in the period, whether or not an evaluation followed.'),
 ('Completion Source', 'Completions come from the SOS 3008 completion log and are joined to referrals on '
  'referral ID. A referral is counted complete only when a matching completion is on file. All 76 '
  'completions in the period matched a July referral.'),
 ('Site Attribution', 'Each referral and its evaluation are counted at the site the referral was routed to. '
  'The completion log separately records a site at the point of completion, which differs on four July '
  'records. Using referral routing keeps referrals and completions on one denominator.'),
 ('Turnaround', 'Turnaround is measured in business days from referral submission to evaluation completion. '
  'Weekends are excluded, so a Friday referral completed the following Monday is recorded as one business '
  'day, not three calendar days.'),
 ('Provider Names', 'The completion log records some providers in abbreviated form. Abbreviated and full '
  'spellings of the same provider have been consolidated for the provider tables.'),
 ('Dates of Birth', 'Twenty-two July referral records carry a date of birth stored in the wrong century, an '
  'artifact of two-digit year entry. These are displayed corrected in this report. The underlying records '
  'have not been changed.'),
 ('Open Referrals', 'A referral shows as open only because no completion has been recorded against it in the '
  'most recent completion log, dated through 07/31/2026. Referrals received near the end of the period '
  'commonly complete in the following month and are counted in the month the evaluation takes place.'),
 ('Reporting Period', 'This report covers referrals received between 07/01/2026 and 07/31/2026 and '
  'evaluations completed within that same window. Referral volume and completion activity do not reconcile '
  'to each other across a period boundary and are not intended to.'),
 ('Confidentiality', 'This report contains protected health information. It is intended solely for the named '
  'partner and its authorized personnel, and may not be redistributed without the written consent of SOS '
  'Mobile Medical Care.'),
]
items = ''.join(
 '<div style="break-inside: avoid; margin-bottom: 9px;">'
 '<div style="font: 700 9px %s; letter-spacing: 0.08em; text-transform: uppercase; color: %s; '
 'border-bottom: 1px solid %s; padding-bottom: 2px; margin-bottom: 4px;">%s</div>%s</div>'
 % (F, NAVY, LILAC, h, t) for h, t in DISC)
body = ('          <div>\n'
 '            <div style="font: 800 12px %s; letter-spacing: 0.2em; text-transform: uppercase; color: %s; '
 'margin-bottom: 6px;">Reference</div>\n'
 '            <div style="font: 700 26px %s; color: %s; letter-spacing: -0.01em;">Disclaimers</div>\n'
 '          </div>\n'
 '          <div style="column-count: 2; column-gap: 24px; font: 400 8.8px/1.42 %s; color: #000000;">%s</div>\n'
 % (F, MID, F, NAVY, F, items)) + spacer() + '\n' + footer(FOOT)
PAGES.append(shell(num, SPINE, body, mark_top=52, spine_pad=106))

head = open('tpl/_head.html').read()
head = head.replace('<title>MPU Empath July 2026</title>', '<title>MPU InnoVage July 2026</title>')
head = head.replace('Empath', PARTNER)
out = head + '\n'.join(PAGES) + open('tpl/_tail.html').read()
open('MPU_InnoVage_July_2026.html', 'w').write(out)
print('WROTE', len(PAGES), 'pages', len(out), 'bytes')
