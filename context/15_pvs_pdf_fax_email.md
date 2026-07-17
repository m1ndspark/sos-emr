# PVS PDF, Fax Dispatch, and SendGrid Email Infrastructure

First established 2026-07-16 (Session 18, covering July 15-16 work). Records the
provider resolver on Imaging_Orders, the PVS Visit X-Ray group, the PVS-to-PDF
template and send architecture, the Fax_Address_Book directory, and the SendGrid
email stack. Live app is source of truth.

--------------------------------------------------------------------------------
1. IMAGING_ORDERS - PROVIDER AUTO-RESOLVE (BUILT + VERIFIED)
--------------------------------------------------------------------------------
Provider is the logged-in user, resolved like Referrals_Main. Match
Employees[Employee_Email == zoho.loginuserid && Employee_Status == "Active"].
Covers admins (@sosmmc.com) and portal providers (@sosreferrals.com) since
Employee_Email equals the login email for all. Active gate is the real guard: a
departed employee still matching by email could otherwise sign a live order.

  Workflow 1 - "Imaging Order Provider Stamp", On Load:
    v_Email = zoho.loginuserid;
    for each v_Emp in Employees[Employee_Email == v_Email && Employee_Status == "Active"]
    { input.Provider_Signature_Link = v_Emp.ID; input.Provider_NPI = v_Emp.Provider_NPI;
      input.Employee_Phone = v_Emp.Employee_Phone; }
    disable Provider_Signature_Link; disable Provider_NPI; disable Employee_Phone;
    NOTE: provider is a LOOKUP (Provider_Signature_Link), set by = v_Emp.ID, not a
    text Provider_Name field (which does not exist).

  Workflow 2 - "Imaging Order Provider Gate", On Validate (Create AND Edit):
    blocks submit if no active match, message:
    "Your provider profile is inactive or not found. Contact an admin."

  Employees side: Provider_NPI field added (link name Provider_NPI). Employee_Phone
  is a native Phone field; Employee_Status is Radio Active/Inactive.

  DELUGE LEARNING (confirmed live): do NOT use typed variable declarations in the
  body. `string v_Email = ...` throws "Improper Statement at line 1". Use untyped
  `v_Email = ...`. Function-signature parameter types are fine (standalone funcs).

--------------------------------------------------------------------------------
2. PVS - VISIT X-RAY GROUP (FIELDS BUILT; reveal workflow PENDING)
--------------------------------------------------------------------------------
SOS ORDERS x-rays; vendors perform them. The PVS documents the ORDER only (what,
date, why). Results arrive later and, because the PVS locks at finalize, go in the
addendum. Three X-ray contexts on the PVS, all separate:
  - Group A (referral-inbound): Reason_for_X_Ray_Request, Upload_XRay_Request_Files.
    The partner's "an x-ray may be needed" flag + any file they sent. KEEP.
  - Group B (X-Ray Only section): Imaging_Type_Order, Imaging_Order_Indication,
    Imaging_Order_Date, Imaging_Files_Upload. Gated by Type_of_Entry = X-Ray Order.
  - NEW Visit X-Ray group (this session): documents an x-ray ordered DURING a
    Patient Visit. Gated by Type_of_Entry = Patient Visit, revealed by a yes/no.

  Fields built: Visit_XRay_Section; XRay_Ordered_This_Visit (Radio No/Yes);
  Visit_XRay_Type (Single Line); Visit_XRay_Order_Date (Date); Visit_XRay_Indication
  (Multi Line). Fields 3-5 Default Hide On Load.

  CARRY - reveal workflow "Visit XRay Reveal", On User Input of XRay_Ordered_This_Visit:
    show/hide Visit_XRay_Type, Visit_XRay_Order_Date, Visit_XRay_Indication on Yes/No.

--------------------------------------------------------------------------------
3. PVS -> PDF (template BUILT; generation + storage PENDING)
--------------------------------------------------------------------------------
Mechanism: Creator Record/Print Template (report Print & PDF > Create > Blank >
Encounter_PatientVisit), HTML-editable. NOT the Zoho Forms PDF editor (different
product). Field map in PVS_PDF_Field_Map.md; HTML in PVS_template_full.html.

  Layout: SOS logo (Image element) + 4-column header field table (borders #ddd =
  rgb(221,221,221); label cols white-space:nowrap width:1%; value cols fill) +
  "Clinical Note: ${Clinical_Note_Type}" + ${Final_Clinical_Note}
  (white-space:pre-wrap) + single-line signature with 25px top margin:
  "Electronically signed by: ${Employee_Full_Name} ${Employee_Title} on ${Visit_Completion_Date}".

  DECISIONS:
  - SOAP note stays a SINGLE field (Final_Clinical_Note). Providers dictate one
    narrative from the car; section headers live inside the text. AI SOAP
    structuring deferred (AWS pipeline not built).
  - Conditional PVS fields are driven by Type_of_Entry (block-level) and controlling
    fields like Additional_Charges/Diversion (line-level). The drag-drop template
    cannot branch, so the PVS PDF stays SINGLE-PURPOSE: the Patient Visit clinical
    note only. X-ray and lab ORDERS are their own documents (Imaging_Orders).
  - The PVS record is the universal audit event (every visit of every type is a PVS
    row, matched to Referral_Link; no-referral rows flagged manually). Type tracking
    is a reporting need, not a PDF need.
  - PDF credit limits (Zoho One): generate ONCE and store; never regenerate on
    re-send.
  - Charges/diversion are internal billing data; confirm they do NOT print on the
    partner-facing note (keeps template clean).

  SEND ARCHITECTURE (single console):
  - Finalize locks the PVS (portal users are read-only via page permissions; only
    the two admins can edit via Reports - that IS the lock) and generates + stores
    the PDF, then redirects (openUrl) into the send console pre-filled.
  - Console is the ONE send hub: attachment source is EITHER a PVS lookup (pulls the
    stored PDF) OR a file upload; recipients are fax (from Fax_Address_Book or manual)
    and/or email (to the referral contact); handles initial sends and re-sends; keeps
    a send log. From is always SOS; email "to" is the referral contact.
  - Referral-inbound attachments are stored (WorkDrive), not auto-sent.
  - Storage: PDFs and uploads go to Zoho WorkDrive (BAA-covered), link stored on the
    record, keeping the Creator DB lean (~250 PVS/month and growing).

--------------------------------------------------------------------------------
4. FAX_ADDRESS_BOOK (BUILT + SEEDED)
--------------------------------------------------------------------------------
Single shared directory for ALL outbound faxes (PVS notes, imaging/lab orders,
results). Standalone/flat by decision (fewest inputs); NOT linked to Partners.
Vendors are never Partners (vendors deliver care and can bill the partner directly;
partners originate referrals and sign agreements).

  Fields: Recipient_Details_Section; Recipient_Name (Single Line); Fax_Number
  (Single Line, raw digits e.g. 18136971390); Recipient_Category (Radio: Hospice,
  PACE, Clinic, Hospital, Vendor, Group, Contact); Recipient_Status (Radio
  Active/Inactive, initial Active); Recipient_Notes (Multi Line, user reference only).

  Seed: Fax_Address_Book_Import.csv, 33 of 37 filled by branch-keyword match from the
  SRFax export; 4 had no source line (AccentCare Hernando, InnoVage Orlando, Chapters
  LifePath, Heartworks IV). "Add from send form" (SRFax-style save-to-book) is a
  console feature for later.

--------------------------------------------------------------------------------
5. EMAIL INFRASTRUCTURE - SENDGRID (BUILT + VERIFIED)
--------------------------------------------------------------------------------
sosreferrals.com is SendGrid domain-authenticated (SPF + s1/s2 DKIM + DMARC all
verified). App sends AS notifications@sosreferrals.com. Cloudflare Email Routing
forwards notifications@ -> neil.heird@sosmmc.com (Cloudflare holds MX). Zoho Mail
was dropped for sosreferrals.com (portal @sosreferrals.com logins are Creator portal
users, unaffected).

  Creator connection: sendgrid_connection (built-in SendGrid connector, Enabled, On
  for SOS Referrals App). The Test button fails on ALL custom connections here (known
  local quirk); a real send is the test.

  Reusable function send_via_sendgrid(pTo, pSubject, pMessage) - POSTs SendGrid v3
  mail/send via sendgrid_connection, From notifications@sosreferrals.com, content
  type text/html, info sgResponse. VERIFIED. This is the shared send path for the
  monitor now and the PVS-note/console emails later.

  run_schema_monitor rewritten: all 5 Zoho sendmail blocks -> send_via_sendgrid()
  calls. VERIFIED (email received on a real schema change).
  ROOT CAUSE of the earlier "runs, commits, no email": Zoho sendmail requires an
  approved sender; sosmmc has 2 approved DOMAINS but no approved SENDERS, so Zoho
  silently dropped every send. SendGrid connection bypasses this entirely.
  DELUGE SYNTAX: an email address in Zoho sendmail `from` must be a quoted string;
  unquoted `from :neil.heird@sosmmc.com` throws Improper Statement.

--------------------------------------------------------------------------------
6. OPS NOTES
--------------------------------------------------------------------------------
  - Schema monitor pushes to GitHub; the LOCAL repo needs `git pull` to see updates
    (recurring gotcha when verifying schema before building).
  - run_schema_monitor was never archived in the repo before this session; now added.
  - OPEN: Added_User = zoho.loginuser stores the org name, not the runner; should be
    zoho.loginuserid (cosmetic, already in the learnings).

--------------------------------------------------------------------------------
7. CARRY-FORWARD
--------------------------------------------------------------------------------
  1. Visit XRay Reveal workflow (On User Input of XRay_Ordered_This_Visit).
  2. Backfill Provider_NPI on Employees.
  3. DM_Full_Name computed field + backfill on Referrals_Main; DM_Phone explicit map
     in the Imaging_Orders pull-lock.
  4. Imaging_Orders S5 (Exam & Clinical) and S6 (Vendor & Transmit) fields + the two
     rollups (Ordered_Exam_Print, Order_ICD_Print).
  5. Imaging_Orders patient-section pull-lock workflow.
  6. Imaging_Vendors directory form.
  7. PVS PDF: finalize-lock + generate + WorkDrive store + redirect to console.
  8. Send console build (PVS lookup / upload, fax + email, re-send, send log).
  9. AWS pipeline (Transcribe Medical + Bedrock) -> one-shot "structure my note"
     action (replaces manual ChatGPT paste; PHI leaves BAA today, interim directive).
  10. Rename repo folder X_Ray_Orders -> Imaging_Orders.
  11. Exam_Catalog laterality decision.
  12. Fix Added_User -> zoho.loginuserid in the monitor.
  13. Read-only monitoring agent + STATE.md start-of-session digest (design topic).
  14. Zoho Mail DNS cleanup for sosreferrals.com (later, low-risk).
