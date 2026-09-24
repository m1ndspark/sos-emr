# SOS Referral Partner Field Convention

How the partner is recorded on `Referrals_Main`. Established 2026-09-23
(Session 52) from the correctly shaped rows of the September referral export.

## The four columns

Every referral carries the partner in four columns. Example, the Tidewell
branch of Empath:

| Export column | Value |
|---|---|
| Partner Organization | `Empath` |
| Partner Branch/Location | `Tidewell` |
| Partner Branch | `Empath - Tidewell` (the full label) |
| Partner Lookup | `Empath` |

Partner Branch holds the full label. Partner Organization and Partner Lookup
hold the organization. Partner Branch/Location holds the branch part.

## Deriving the four from the full label

Split the full label on the FIRST `" - "` only:

- left of it: Partner Organization and Partner Lookup
- right of it: Partner Branch/Location
- the whole label: Partner Branch

Splitting on the first separator, not every separator, is what keeps
multi-part branch names intact:

| Full label | Organization | Branch/Location |
|---|---|---|
| `Empath - Suncoast - HIL` | `Empath` | `Suncoast - HIL` |
| `Empath - Suncoast - PIN` | `Empath` | `Suncoast - PIN` |

This reproduces the clean September rows exactly.

## Normalisation rule

A value beginning `Suncoast - ` is an Empath branch written without its
organization. Prefix it with `Empath - ` before splitting:
`Suncoast - PIN` becomes `Empath - Suncoast - PIN`.

## Canonical labels

Twelve canonical full labels were derived from the clean September rows. The
September fix file confirms these nine in use:

- `AccentCare - Pasco`
- `Empath - Marion`
- `Empath - Polk`
- `Empath - Suncoast - HIL`
- `Empath - Suncoast - PIN`
- `Empath - Tidewell`
- `Empath - Trustbridge`
- `InnoVage - Orlando`
- `InnoVage - Tampa`

> The full twelve are not listed in the Session 52 log, and the fix file only
> shows the labels its 46 rows needed. Complete this list from the September
> export before relying on it.

**`AccentCare - Broward` is a valid thirteenth label.** It exists in
`Partner_Locations` as an active location (code BRO) but was absent from
September traffic apart from REF-1545, which resolved to it.

## September 2026 correction

- Export: 107 rows, 47 columns. 60 correctly shaped. 47 had the full label in
  Partner Organization, with Partner Branch and Partner Lookup empty.
- 46 of the 47 resolved with the rules above. REF-1500 was blank on all four
  columns and could not be resolved (open).
- `Referrals_Partner_Fix_Sept2026.xlsx`, 46 rows, Referral ID plus the four
  partner columns, headers matching the export exactly. **The import of the 46
  corrected rows succeeded on the first try.**
