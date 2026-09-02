# Work order for Fable: audit the gross and net labels

**From Daniil, 1 September 2026. This is a task to complete today, not a document to review.**

You are being asked to do one thing and produce one file. Read this, do the work, write the file,
report the four numbers at the bottom. If you finish early, the second job at the end is next.

---

## Why this matters, in one paragraph

Every multiple in our database is a valuation divided by a revenue figure. If the revenue figure
includes money that belongs to somebody else and we treat it as if it does not, the multiple is
wrong by roughly ten times, and a founder gets a valuation range that is off by an order of
magnitude. Razorpay sat in our fintech file at 67.6x on that exact error for four days. We now have
a field recording which kind each row is. **Nobody has ever checked whether the field is right.**
That is your job.

---

## The one rule you are applying

**Does the revenue line contain money that belongs to somebody else?**

- **YES, it contains other people's money → GROSS.** A freight broker's revenue holds the carrier's
  fee. A staffing platform's revenue holds the worker's wage. A payments processor reporting
  "total revenue" before interchange holds the card networks' money.
- **NO, the company keeps it → NET.** A marketplace commission. A software subscription. **And a
  first-party retailer, which buys stock and resells it: it keeps the whole sale price, so its
  revenue is NET in our sense even though the number looks huge next to a commission.**

The test is ownership, not size. A big number is not gross. A small number is not net.

---

## What to do, per row

The tool `python3 tools/audit_basis_period.py` prints 41 rows where the label asserts a basis that
the quoted wording never actually states. They are listed at the end of this file so you do not have
to run anything to start.

For each row:

1. **Open the source.** The URL is in `data/private-rounds.csv`, column `revenue_source_url`.
   The row is identified by company name and date.
2. **Read what the revenue line actually is.** Not the headline. The definition. For an Indian
   company, "revenue from operations" needs the note that says what is in it. For a payments
   company, find out whether interchange is in or out.
3. **Decide: GROSS, NET, or CANNOT TELL.** "Cannot tell" is a valid and useful answer. It means the
   source does not say, and the row should stop pricing until it does.
4. **Write down the sentence that made you decide**, word for word, with the URL.

**Do not change any file.** Write your verdicts into the new file described below. Somebody applies
them afterwards, deliberately, so that a wrong call by you is one reviewable step rather than a
silent edit to live data.

---

## The file you produce

`docs/basis-audit-verdicts-1sep.md`, one section per row, in this shape:

```
### Pine Labs, May-21, 30.3x
Current label: NET_REVENUE
Verdict: GROSS_REVENUE
Source read: https://... (the exact URL you opened)
The sentence that decided it: "Revenue from operations of Rs 721 crore, which includes
   Rs 402 crore of payment processing charges recovered from merchants and paid to networks."
Confidence: high
What changes if I am right: the multiple moves from 30.3x to roughly 12x, and it stops
   dragging the fintech median upward.
```

That last line is required on every row. If you cannot say what breaks when the label is wrong, you
have not finished thinking about the row.

---

## Where to start, because the order matters

Do these nine first. They are the ones where the same kind of business genuinely reports both ways,
so an archetype rule cannot decide them and a wrong call is expensive:

| Row | Current label | The specific question |
|---|---|---|
| dLocal, Apr-21, 48.0x | NET | "Total revenues" for a cross-border processor. Is this before or after network and processing costs? Daniil expects net; confirm it. |
| Pine Labs, May-21, 30.3x | NET | Indian payments. Does "revenue from operations" include pass-through interchange? |
| Marqeta, May-20, 14.3x | GROSS | Card issuing. Marqeta's own S-1 defines net revenue after card network costs. Which one is the $300m? |
| Zepz, Aug-21, 14.8x | GROSS | Remittances. Is the round announcement's figure send volume revenue or the company's take? |
| Delhivery, May-21, 5.97x | GROSS | Indian logistics, "revenue from operations". |
| Xpressbees, Feb-22, 8.94x | GROSS | Same question, same phrase. |
| Shiprocket, Aug-22, 16.03x | GROSS | Same question, same phrase. If these three disagree with each other, one of them is wrong. |
| Jobandtalent, Dec-21, 2.08x | GROSS | Staffing. The worker's wage should be in there, which makes it gross. Confirm from the source. |
| Loadsmart, Nov-20, 4.0x | GROSS | Freight broking. The carrier's fee should be in there. Confirm. |

Then work the rest of the 41 in any order. **The three Indian logistics rows are the highest value
in the list**: they carry the same phrase, they are labelled the same way, and if that label is
wrong all three multiples are wrong together, which would move a whole sector.

---

## When you are done, report exactly these four numbers

1. How many rows you read the source for.
2. How many labels were correct.
3. How many were wrong, and the total effect on the multiples (which ones move, and to what).
4. How many you could not decide, and what each one would need.

Nothing else. Not a summary of the method, not a restatement of the rules.

---

## The 41 rows

Run `python3 tools/audit_basis_period.py` for the live list with wording attached. As of 1
September it is:

Calendly Jan-21 · Invisible Technologies Sep-25 · Scale AI Jun-25 · Mailchimp Sep-21 · Semrush
Nov-25 · Mews Jan-26 · Jasper Oct-22 · Wolt Nov-21 · Gopuff Jul-21 · Marqeta May-20 · dLocal Apr-21
· Zepz Aug-21 · Pine Labs May-21 · Delhivery May-21 · Xpressbees Feb-22 · Shiprocket Aug-22 ·
Creditas Dec-25 · Creditas Jul-22 · Jobandtalent Dec-21 · Creditas Dec-20 · Loadsmart Nov-20 ·
Marqeta May-19 · Zepz Oct-24 · Vinted Apr-26 · Quince Mar-26 · OLIPOP Feb-25 · Vinted Oct-24 ·
Meesho May-24 · SHEIN Jan-24 · Flipkart Jul-23 · SHEIN May-23 · Huel Nov-22 · Liquid Death Oct-22 ·
Meesho Sep-21 · Flipkart Jul-21 · Klaviyo May-21 · StockX Apr-21 · Harry's Mar-21 · Savage X Fenty
Feb-21 · Away May-19 · Glossier Mar-19

One more row is flagged separately on period rather than basis: **Loadsmart Feb-22**, labelled LTM
while its own wording says "projecting to double in the next 12 months", which is forward. Same
treatment.

---

## If you finish the 41

**Second job: the 100 inferred rows.** Every private row carries `revenue_basis_source`. 18 say
STATED, meaning the source used the words. **100 say INFERRED**, meaning somebody read the basis off
the business model without checking. The 41 above are the subset where the tool could detect the
gap. The other 59 are inferred rows the tool cannot flag, and they are no safer.

Same method, same output file, and again start with payments and delivery, because those are the two
sectors where the same kind of business reports both ways.

**Third job, if there is time: 37 of our 108 priced private rounds are excluded from every range**
(`in_medians` is false). That is a third of our private evidence pricing nobody. Some exclusions are
certainly right. Nobody has checked that all of them are. List each one with the reason it is out
and whether the reason holds.
