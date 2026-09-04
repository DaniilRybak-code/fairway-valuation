# The service shell: what was decided 3-Sep, and what is still blocking

Daniil's answers tonight: no entity registered yet, retention "14 or 30 days?", price a flat 750,
Stripe link later. Here is what each one means for the live page and what is still open.

## 1. Entity: you can trade without one, but not without a name and an address

Trading as a sole trader in England and Wales needs no registration at Companies House. You
register for Self Assessment with HMRC and you can invoice and be paid. Stripe onboards sole
traders. **So yes, the pilot can run without a company.**

What you cannot do is leave the page saying nothing about who is behind it. The disclaimer
currently reads "operated by [COMPANY NAME], registered in England and Wales, company number
[COMPANY NUMBER]", which is written for a company you do not have. For a sole trader the
consumer regulations want a real name and a geographic address for service, not a PO box and not
just an email.

**Ready to paste, on your word:**

> Fairway is a service of Daniil Rybak, trading as Fairway, [address for service]. Contact
> [email].

**Two things to settle before that goes live:**

- **An address for service.** Your home address becomes public if you use it. A registered office
  or virtual office service is about £50 a year and solves it. This is the practical reason most
  people incorporate early, not the tax.
- **The ICO fee.** A sole trader processing personal data for a business generally has to pay the
  ICO data protection fee. Tier 1 is around £52 a year. It takes ten minutes online.

**The item I would check before either of those.** You are an MD in fintech coverage under SM&CR.
Charging founders for valuation analysis is an outside business interest, and it sits close to
what you cover. Whatever the answer is, it is your compliance team's to give, and it gates whether
you can take the first £750 at all. Worth resolving before the address and the ICO fee, because
those are wasted if the answer is no. I am not a lawyer and this is not legal advice.

## 2. Retention: 14 and 30 days are both wrong, and for the same reason

They are lead-capture numbers. You are selling a paid analysis that a founder will argue from in
front of investors for months. Delete their file in 14 days and you cannot answer "why did you say
8x" in week three, and you have no record if they later say the analysis was negligent.

**Three clocks, not one:**

| what | how long | why that length |
|---|---|---|
| Quiz answers from someone who never buys | **90 days** | Long enough to follow up a warm lead, short enough to defend as necessary. This is the number 14 or 30 was reaching for. |
| The file behind a paid engagement: inputs, the analysis, the reviewer's notes | **6 years from delivery** | The limitation period for a contract claim in England and Wales. Standard for professional services, and the file is your defence if the work is ever challenged. |
| De-identified figures used to calibrate the comp table | **kept** | Once identifiers are stripped it is no longer personal data, so the storage limitation does not bite. Say so plainly rather than leaving it implied. |

**One caution on the third row.** Revenue plus sector plus month plus round size can identify a
single startup even with the name removed. To rely on "de-identified" you have to actually
de-identify: band the revenue, drop the month to a quarter, and never keep the website. Otherwise
it is still personal data on a six-year clock like everything else.

**Ready to paste, on your word:** replace `[RETENTION PERIOD]` with

> 90 days if you do not go on to buy a review, and six years from delivery if you do, which is how
> long we may need the file if the work is ever questioned. Figures we keep to calibrate our
> comparables are stripped of anything identifying you first.

## 3. Price: 750, and two things it breaks

Noted as the flat fee. Two consequences, both small and both live today:

- **The page says the product is free.** The meta description ends "Reviewed by former bulge
  bracket bankers. Free." That is the line search engines and link previews show. It has to change
  the day a price appears, or the first paying founder arrives having been told otherwise.
- **Currency.** You wrote 750 without one. The page already asks the founder to pick USD, EUR, GBP
  or CAD for the ranges, so a bare number will be read in whichever they picked. £750 and $750 are
  not the same offer. **This is the one thing I need from you before I can write the price in.**

**Not a problem yet:** VAT. The UK registration threshold is £90,000, which at £750 is 120
engagements. Below that you do not charge it. Worth a line in the terms saying the price includes
any VAT where applicable, so you never have to re-quote.

**Worth deciding at the same time,** because the page has to say one of them: is the £750 taken
before the review or after the founder sees it? Before is cleaner to build and normal for a fixed
fee. After converts better in a pilot and gives you a refund-free way to fix a bad review.

## 4. Stripe: agreed, later

Nothing here blocks. A payment link is a day of work whenever you want it, and the page can carry
a price with a "pay on delivery, invoice by email" flow for a pilot of five to ten founders
without any payment rail at all.

## What is actually blocking, in order

1. **The employer answer.** Everything below is wasted if it is no.
2. **Currency on the 750.** One word from you and the price goes on the page.
3. **An address for service.** £50 a year, and the disclaimer cannot go live without it.
4. **The ICO fee.** Ten minutes.

Items 2, 3 and 4 together are under an hour. Item 1 is not in your control and is the one to start.

---

# DECIDED, 4 September 2026

Daniil's answers to the three open items above, in his own words, applied.

1. **Price: 750 USD.** Not GBP. The page asks the founder to pick a currency for their ranges, so
   the price has to be written as $750 or "750 USD" and never as a bare 750. The meta description
   ending "Free." changes on the same deploy.
2. **Entity: none.** Sole trader. The disclaimer written for a company is replaced.
3. **Address for service: 29 Westbourne Terrace, London W2 3UN.** His home address, chosen over the
   £50-a-year registered office. It will be public on the live page and in the repo.

The disclaimer is therefore ready except for one field, the contact email:

> Fairway is a service of Daniil Rybak, trading as Fairway, 29 Westbourne Terrace, London W2 3UN.
> Contact [email].

Still open from this document: the ICO data protection fee (about £52, ten minutes), the SM&CR
answer, and whether the fee is taken before or after the founder sees the review.
