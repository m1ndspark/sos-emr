# Partner_Contracts

- Display name: Partner Contracts
- .ds line: 4199
- Fields (excluding sections): 8
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Partner_Link | Partner Link | picklist | Partners |
| Partner_Location_Link | Partner Location Link | picklist | - |
| Partner_Contract_Upload | Partner Contract Upload | upload file | - |
| Partner_Contract_Effective_Date | Partner Contract Effective Date | date | - |
| Partner_Contract_Term_Date | Partner Contract Term Date | date | - |
| Partner_Contract_Status | Partner Contract Status | radiobuttons | - |
| Contract_Notes | Contract Notes | richtext | - |
| System_Fields_Section | System Fields Section | section | - |
| Partner_Contract_ID_Stamp_Generator | Partner Contract ID Stamp Generator | text | - |

## Workflows

### Partner_Contract_Branch_M

- Display: Partner Contract Branch Match
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 36337
- Fields read: Partner_Link, Partner_Location_Link
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Locations (ID); read Partner_Locations (Partner_Link)

### Partner_Contract_ID_Stamp

- Display: Partner Contract ID Stamp Generator
- Record event: on add
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 36318
- Fields read: ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

## Reverse index

Every item that references a field of this form.

- Partner_Contracts.Partner_Link: workflow Partner_Contracts/Partner_Contract_Branch_M [read]
- Partner_Contracts.Partner_Location_Link: workflow Partner_Contracts/Partner_Contract_Branch_M [read]
- Partner_Contracts.Partner_Contract_Upload: no references
- Partner_Contracts.Partner_Contract_Effective_Date: no references
- Partner_Contracts.Partner_Contract_Term_Date: no references
- Partner_Contracts.Partner_Contract_Status: no references
- Partner_Contracts.Contract_Notes: no references
- Partner_Contracts.Partner_Contract_ID_Stamp_Generator: no references
