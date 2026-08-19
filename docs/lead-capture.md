# Lead capture: one row per entry in a Google Sheet

Ten minutes, once. No API keys stored anywhere, no third-party service, no monthly cost.

## How it fits together

```
browser  ->  POST /api/lead  ->  POST LEAD_WEBHOOK_URL  ->  Apps Script  ->  row in the sheet
                (flattens to                                    |
                 fixed columns)                                 +-> alert email to you
                                                                +-> pre-drafted reply in Gmail
```

Column order is defined once, in `FIELDS` at the top of `api/lead.js`. The API sends the field names alongside the values, so the sheet writes its own header row the first time a lead arrives. Adding a question later means adding one entry to `FIELDS`; nothing in the sheet needs configuring.

## Setup

**1. Create the sheet.** New Google Sheet, name it `Fairway leads`. Leave it empty.

**2. Add the script.** Extensions > Apps Script. Delete whatever is in `Code.gs` and paste in `tools/sheet-webhook.gs` from this repo.

**3. Set three values at the top of the script.**

- `NOTIFY_EMAIL` where the alert goes
- `SHARED_SECRET` any long random string, this is what stops strangers writing to your sheet
- `CREATE_DRAFT` leave as `true` to get the reply pre-drafted in Gmail

**4. Deploy.** Deploy > New deployment > type Web app.

- Description: anything
- Execute as: **Me**
- Who has access: **Anyone**

Google will ask you to authorise the script, including Gmail access for the draft. Approve it. Copy the `/exec` URL it gives you.

The "Anyone" setting is required because Vercel calls the URL without a Google login. The URL is unguessable and the secret check rejects anything without it. To rotate, redeploy and update the env var.

**5. Wire it to Vercel.** Project `fairway` > Settings > Environment Variables:

| Name | Value |
|---|---|
| `LEAD_WEBHOOK_URL` | the `/exec` URL from step 4 |
| `LEAD_SHARED_SECRET` | the same string as `SHARED_SECRET` |

Redeploy so the function picks them up.

**6. Test.** Run through the quiz with your own email. Within a few seconds you should have a row in the sheet, an alert email, and a draft sitting in Gmail waiting to be edited.

## What lands in each row

Identity and contact, all nine answers including the free-text ones, the computed range and dilution figures, the hook variant and UTM source, and coarse location. Then three empty columns for the review workflow: `status`, `reviewer_notes`, `sent_at`.

Location comes from Vercel's edge headers, which resolve country, region and city from the request. No IP address is ever stored, and nothing is read client side. It is still personal data once attached to an email address, so the privacy line on the site should mention it before this goes live in the EU or UK.

## Working the sheet

Sort by `timestamp_utc`, filter `status = new`. The review loop is: read the row, open the Gmail draft, correct the number if it is wrong, send, then set `status` to `sent` and fill `sent_at`.

Two columns are worth watching from day one. `type` separates completed leads from partials and later additions. And every time a reviewer overrides the computed range, that is calibration data for the comp table described in `docs/reveal-engine.md`.

## If you outgrow it

The same webhook shape works with Airtable, Make, Zapier or a Postgres endpoint. Only `LEAD_WEBHOOK_URL` changes. Move when you want per-lead status views, attachments or more than one person working the queue; a spreadsheet is genuinely fine for the first few hundred.
