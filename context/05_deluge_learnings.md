# Deluge Learnings (Creator)

Source: Deluge/Creator module and the May 8 session log. Creator behavior wins
over generic Deluge docs.

CONFIRMED WORKS
- zoho.loginuserid returns the full email. Use this for all employee lookups.
- matches("regex") works in On User Input.
- replaceAll("-", "") strips specific characters.
- Escape regex special characters with a double backslash, e.g. replaceAll for an
  open parenthesis must escape it as \\(.
- subString(0, 3) works.
- update v_Rec inside a loop is the confirmed Sequence_Tracker update pattern.
- enable FieldName; enables a disabled field.
- disable FieldName; makes a field read-only.
- if(condition) with parentheses works in On User Input.
- Record fetches return collections and require a for-each loop.
- cancel submit requires no message string in v6.

CONFIRMED DOES NOT WORK
- zoho.loginuser returns the org name, not the email. Do not use for lookups.
- An unescaped open parenthesis in replaceAll fails (regex special character).
- update FormName[ID == v_SeqID.toLong()] is unreliable. Use the loop pattern.
- getPrefix() / getSuffix() do not work. Use subString() instead.
- cancel submit in On User Input does not work. It is available on Validate only.
- Real-time keystroke input masking is not possible in Creator. On User Input
  fires on blur, not on keypress. Best available UX is format-on-blur plus
  placeholder text.

SEQUENCE GENERATION PATTERN (REUSABLE)
- Query by the 3-letter prefix code, not the long display name.
  Example: Sequence_Tracker[Object_Prefix == "MPR"]
- Update with update v_Rec inside the loop.
- Typical fields: a long descriptive name (display only), a 3-letter prefix code
  (all queries use this), a numeric sequence (starts at 1001), a lock status.
- "Stamp" means Creator's native 19-digit system ID only. Never use the word
  stamp for custom human-readable IDs.

OAUTH / CUSTOM API
- Creator Custom API requires BOTH scopes: ZohoCreator.report.READ and
  ZohoCreator.customapi.EXECUTE. Report read alone gives an invalid scope error.

CREDENTIALS
- Runtime secrets live in Zoho Connections, invoked by connection name so the
  value never appears in a field, record, export, or script.
- Human and infrastructure logins live in a password manager.
- Never store secrets in a Creator form, field, or record, or in this repo.

================================================================================
DEPENDENT LOOKUP FILTER / DEPENDENT DROPDOWN  (PROVEN 2026-07-02)
================================================================================
Filter a child lookup by a parent selected on the SAME form (e.g. show only the
selected partner's locations in Partner_Location_Link on Partner_Rates):
- Child lookup field -> Field Properties -> Choices -> check "Set filter" -> criteria:
    Field    = "ID" nested UNDER the parent-lookup heading (e.g. under "Partner Link")
    Operator = equals
    Value    = input.<ParentLookupLinkName>   e.g.  input.Partner_Link   (TYPE it)
- KEY: the value box accepts a TYPED field reference  input.<FieldLinkName>  (not just static text).
- Lookup fields do NOT appear as top-level filter criteria; drill into the lookup heading and pick its ID.
- An EMPTY Set filter (checkbox on, no criteria row) applies NO filtering -> shows everything.
- Mirrors Zoho KB "Dynamically Filter Lookup Options Based on Another Lookup Field's Selection"
  (their example: Asset Name filtered by ID equals input.Category).

================================================================================
LOOKUP DISPLAY FIELD MUST BE RELIABLY POPULATED  (2026-07-02)
================================================================================
Symptom: a lookup dropdown shows "No matches found" (or blanks) even for records
that clearly exist and pass the filter.
Cause: the lookup's DISPLAY field was set to a value that is empty on the target
records. Example - Partner_Location_Link display set to Partner_Location_Label,
but that label is populated only by the Location Label Generator (On Success,
Created/Edited); existing locations created earlier had a BLANK label (backfill
never run) -> the dropdown had nothing to display -> "No matches".
Fix: set the lookup display to an always-populated field (Partner Loc Name), OR
run the backfill so the label field is filled before using it as a display field.
Rule: only use a generator-populated field as a lookup DISPLAY after its backfill
has run for all existing records.
