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

## The figure columns are empty until the founder presses a button

This is the part to read before you work the sheet, because it changes what a row means.

Daniil, 6 September 2026: "we only take a record of the company data (profile, website), without storing the numbers. Then he gets the reveal based on the numbers he put in (we still do not see any financials at that point). Then if the user wants to have his numbers and ff reviewed, he presses a button and it comes through to us, in which case he would specifically agree for us to see it."

So a normal lead row now arrives with the figure columns blank. What is in it:

- the company profile: stage, sector, the sector chips, the website, the company name, how they charge, and the country the edge header resolved
- two ratios: the growth rate and the gross margin. These are percentages and the engine needs them to choose the comparable companies, which is why the page says we receive them rather than claiming we receive nothing
- the contact details: email and phone
- the concern chips, the hook variant and the UTM source

What is not in it, until the founder presses "Send my figures for the banker review" on their result page: revenue in any form, ARR, whether they are profitable, the size of the round they are raising, their timing, EBITDA, their last round, the free-text notes they wrote, and any link they gave us.

**The gate is on the server, not only in the page.** `api/lead.js` blanks every column in `FIGURE_COLUMNS` unless the body carries `consent.figures === true`. If a future change to the page starts sending figures again, the sheet still gets nothing and the Vercel log carries a line saying how many fields were refused. A boundary held at one end only is a boundary that lasts until the next hurried edit.

**Three new columns at the end of the row.** `figures_consent` is `yes` on a row the founder consented to and empty otherwise, so you can sort on it to find the rows you may read numbers in. `consent_at` is the timestamp. `consent_wording` is the exact sentence they clicked, stored beside the figures so that what they agreed to is a matter of record rather than of memory.

**A consented send is a second row, not an edit.** It arrives with `type` set to `figures` and the same `lead_id` as the original row. Filter on the lead id to see both. This uses the `type` column the sheet already had.

**What holds it up.** `reveal-request.js` in the repo root is the only place in the product that builds a request body, and it builds every one of them by looping over a named allowlist. Check 15 in `tools/check_all.sh` runs that code with a sentinel value in every figure the quiz collects and then looks for those values in the request bodies, in the Vercel log line, and in the prompt that goes to the model. It fails if it finds one.

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

The profile and the two ratios, identity and contact, the concern chips, the hook variant and UTM source, and coarse location. Then three empty columns for the review workflow: `status`, `reviewer_notes`, `sent_at`, and the three consent columns described above.

The figure columns are still in the sheet, in the positions they have always been in, and they are empty on a row with no consent. They were left in place rather than removed so that an existing sheet keeps every column where it is and old rows still line up under their own headers.

Location comes from Vercel's edge headers, which resolve country, region and city from the request. No IP address is ever stored, and nothing is read client side. It is still personal data once attached to an email address, so the privacy line on the site should mention it before this goes live in the EU or UK.

## Working the sheet

Sort by `timestamp_utc`, filter `status = new`. The review loop is: read the row, open the Gmail draft, correct the number if it is wrong, send, then set `status` to `sent` and fill `sent_at`.

Two columns are worth watching from day one. `type` separates completed leads from partials, later additions, and the `figures` rows a founder consented to. And every time a reviewer overrides the computed range, that is calibration data for the comp table described in `docs/reveal-engine.md`.

**The free 24-hour read needs the figures, so it needs the button.** A row with `figures_consent` empty is a founder who has seen their comparable companies and has not asked for a person to look at their numbers. There is nothing to review on that row and it should not sit in the queue as though there were.

## If you outgrow it

The same webhook shape works with Airtable, Make, Zapier or a Postgres endpoint. Only `LEAD_WEBHOOK_URL` changes. Move when you want per-lead status views, attachments or more than one person working the queue; a spreadsheet is genuinely fine for the first few hundred.
