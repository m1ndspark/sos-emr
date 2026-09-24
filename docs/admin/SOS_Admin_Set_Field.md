# admin_set_field - Generic Single-Record Field Editor

Built 2026-09-23 (Session 52). The general-purpose repair tool: any single
record, any report, any field present on that report. The fastest route to
fixing one bad value without writing a new function.

> Not in any `.ds` export yet. v52 predates it. Creator is the source of truth
> until a fresh export lands.

## Why it goes through the API

Deluge cannot assign a field by name string. `rec.(v_name) = v_val` is not
valid syntax. A generic editor therefore has to go through the Creator REST API.

## Signature

```
admin_set_field(p_report, p_key_field, p_key_value, p_field, p_value, p_mode)
returns Map
```

| Argument | Meaning |
|---|---|
| `p_report` | report link name to search and update through |
| `p_key_field` | field used to find the record, any field on the report |
| `p_key_value` | value of that key field |
| `p_field` | link name of the field to set |
| `p_value` | new value, always sent as a string (see Limits) |
| `p_mode` | report or apply |

## Modes

- **Report mode** finds the record and returns its current value of `p_field`.
  Writes nothing.
- **Apply mode** does the same, then PATCHes the new value through
  `https://www.zohoapis.com/creator/v2.1/data` + `zoho.appuri`.

It refuses, in either mode, when zero records or more than one record match the
key, and when the target field is not present on the named report.

Run report mode first.

## Connection

| Setting | Value |
|---|---|
| Type | Zoho OAuth |
| Display name | Creator API |
| Link name | `creator_api` |
| Scopes | `ZohoCreator.meta.form.READ`, `ZohoCreator.report.READ`, `ZohoCreator.report.UPDATE` |
| Authorization | same for all environments |
| Connection Access | ON for SOS Referrals App, OFF for SOS Referral Portal |

## Limits

1. **Every value is sent as a string.** There is no typed write.
2. **Dates must be in the app format `MM-dd-yyyy`.**
3. **A lookup field takes the related record's numeric ID**, not its display
   text.
4. **The target field must be present on the report named.** A field that
   exists on the form but not on the report cannot be set through that report.

## Related API limits

- Creator v2.1 `max_records` accepts ONLY 200, 500 or 1000. Any other value
  returns code 9250.
- Deluge has no backslash escape for a double quote, so criteria strings are
  pre-encoded: `%22` for the quote, `%3D%3D` for `==`.

## Proof

REF-1500 `Partner_Organization` was set to a test value, confirmed on the form,
then cleared.
