# Opus, night of 5 into 6 September. The six to-dos, done, and three things for Daniil.

Worked from a fresh clone of origin in the cloud. No git command was run on the laptop, read-only
or otherwise. The commit command is at the foot and it is `git add -A`.

**Origin had moved past the status document.** The status file says origin is at `d1f8966`. It is
at `6433348`: two more commits landed at 23:21 and 23:22 (investor round two, three control
transactions, and the floor ruling applied). Everything below is measured against `6433348`.

---

## The headline

**Gate 90 to 95 of 102.** Five fixtures flip to PASS: clera, nursa, paymentkit, standout, tsenta.
Nothing regresses. The suite is green on all fifteen checks except check 1, which still fails on the
public pull alone, deliberately, because it is not loaded.

All five flip for the same reason, and it is the reason your 23:35 ruling named: their private lane
was full of rounds priced on gross revenue, and the quiz only ever asked for net.

---

## 1. The quiz asks for both net and gross revenue, and the engine uses both

**What was wrong, in numbers.** Of 320 private rounds, 78 are priced on a gross figure and 66 of
those hold a usable multiple and sit in the medians. Every one of them was unreachable, because the
engine assumed every founder answers on net. Across the 102 fixtures, 41 of them have a gross round
sitting inside the peer set the matcher already picked for them, 105 such rounds in total. Six of
the twelve gate failures had a private lane made entirely or mostly of gross rounds.

**What the quiz asks now.** Every fork that asks for revenue asks for both figures. That is eight
forks: software, marketplace, consumer subscription, exchange, ecommerce, payments, media, delivery.
The gross question is optional in all of them, so nobody is blocked, and a founder who gives one
figure is served on that one, exactly as you ruled.

Lending is the one fork that does not ask, and that is deliberate rather than an omission: a lender
is not asked for revenue at all, on the long-standing reasoning that revenue on a lending business
contains interest earned on borrowed money and scales with leverage rather than with value. A fork
that does not ask for revenue cannot ask which revenue. The 13 gross rounds sitting in lending
archetypes are therefore still unused, and that is now a named item rather than an accident.

The wording the founder sees, shared by all eight forks so they cannot drift apart:

> Plain words: GROSS revenue is everything that passes through you before you pay out the part that
> was never yours. NET revenue is the part you keep. Answer both and you get two ranges instead of
> one, each built only from rounds priced the same way as the figure it uses, because a gross
> multiple applied to a net number is wrong by roughly your take rate. We hold 66 rounds priced on
> gross revenue that a net-only answer cannot reach.

Each fork adds one line of its own on top: the payments fork says "before interchange and scheme
fees are paid out", the marketplace fork "if you book the whole transaction rather than your
commission", ecommerce "before returns and discounts", and the software fork says to leave it blank
if ARR is the whole of what you bill and keep, which for most software businesses it is.

**What the engine does with it.** A second reading, `REVENUE_GROSS`, alongside the net one. The
founder's gross figure is compared only against rounds priced on gross, the net figure only against
rounds priced on net, and they produce two separate ranges with two separate labels.

**Rule B3 is not loosened, and this is the part worth checking me on.** Gross still never bands with
net. Splitting the two into their own ranges is what makes using the gross rounds safe: they can now
be used without ever being averaged into a net figure. Six new assertions in check 9 hold that in
place, and they fail loudly if it ever stops being true:

- a net row answers the net range and is silent in the gross one
- a gross row answers the gross range and is silent in the net one
- a row with no basis label reads as net-equivalent, answers the net range, and is **not** swept
  into the gross one, so no round is ever counted twice
- the gross figure takes the same period conversion as the net one (95 growing 60 per cent is 152)
- each range multiplies by its own founder figure, never the other one

Check 14, new tonight, re-checks the last of those across all 102 fixtures from the assembled
payload: 32 lanes now offer both readings side by side, and no company appears in both.

**Private lane only, and this is a limit you should know about.** The listed files carry no basis
column at all: 513 rows with nothing recording whether their revenue is gross or net. That is the
known hole already on the post-launch list. Offering a listed gross range would mean relabelling 513
rows nobody has read, which is inventing a fact, so a founder's gross figure meets private rounds
only until that hole is filled. Written into the rulebook as B3a.

**Which range a founder actually sees, since I asked this badly the first time.** They see the net
range if they gave a net figure, the gross range if they gave a gross figure, and both if they gave
both. That is your rule and it is what the engine does: `founder_metric_for` returns nothing when a
figure is absent, so an unanswered measure is never priced. It was true before tonight and it is
true now.

**Check 8 is the separate thing, and it is settled at 95.** The scoreboard is not a founder. Its 102
test companies give no figures at all, and by your 3-Sep ruling it uses no revenue anywhere: it asks
whether we can narrow the world to a defensible comparable set, not what that set values the company
at. Applying the founder rule to it literally would score every fixture at zero lanes, the net ones
included. So it counts comparables found, and the four gross rounds sitting in nursa's archetype are
comparables we hold. Measured the other way, gated on an answered question, it reads 90. One line
reverts it if you want that instead. Worth knowing before you decide: the six companies it turns on
(Mercor, Micro1, Jobandtalent, Incredible Health, Juspay, Cashfree) all disclose gross because that
is their own market's convention, so a real founder in those lanes will usually have the number.

---

## 2. The No-comps list, and rule A12 part 3

The word "register" is gone from the code and the rulebook. Check 8 now prints a section headed
**THE NO-COMPS LIST** with both kinds of entry under it:

```
THE NO-COMPS LIST: every test company the database could not answer
  2 lanes served on a label   |   7 of 102 fixtures not served at all

  KIND 1  SERVED ON A LABEL, NOT ON EVIDENCE      14 comparables across 2 lanes
  KIND 2  NO COMPARABLES AT ALL                    7 of 102 fixtures, each with its reason
```

Two counts and not one sum, because a fixture can be in both at once (ultrasonium is rescued on its
private lane and fails the gate anyway), and an inflated brief is a worse brief.

A12 part 3 is rewritten to your 23:10 wording: four marches on 8, 11, 15 and 18 September of 30 to
40 new test companies each, the list resolved in **one bulk pass** after the 18 September march and
before launch, and no lane-by-lane chasing in between. The rule now says in as many words that a
proposal to pull data outside that one pass is the rule telling you to stop.

A12 part 2 is restated as what the code actually does: the fallback opens for a lane holding **fewer
than two priced comparables**, and what it admits is **kept only if it adds a priced name**. The old
wording was looser than the thing it described.

A11 had a heading and no body. It now says that hardware is filed under what it sells rather than
under a hardware archetype, and it records the uncomfortable live consequence: ultrasonium, a metal
manufacturer, carries Owned-Inventory Retail, and on that label the fallback offered it Moove,
Quince, Olive & June and Flink. It fails the gate anyway so nothing wrong reaches a founder, but the
rule is doing worse work there than elsewhere and the tagging review has it.

---

## 3. The thin-lane diagnosis no longer contradicts itself

It printed "12 thin lanes, 0 genuine sourcing requests" on the same evening a pull into those lanes
moved eight fixtures from FAIL to PASS. The cause: any held name stood a sourcing request down, even
a name the relevance gate rightly bars. Docker for paymentkit and Zepz for tash were counted as
reasons not to source.

A name is now a candidate only if sourcing is not what stands between it and the founder. The
headline is three numbers instead of one:

```
SOURCING requests (3)      no name in the file clears the rules for that lane
   goldfish / secondary, honen / secondary, levelten / private
AWAITING A RULING (8)      a related, priced name we hold ranks below the lane cut
MATCHER questions (1)      a usable name is in the file and is not being shown
```

---

## 4. The dates

The raw public-pull file and `docs/public-pull-verdicts-4sep.md` both said 4 September. Both first
exist in commit `224ec60`, made at **21:28 UK on 5 September**, and no earlier commit contains
either. The header also claimed a 21:45 transcription time, which is later than the commit carrying
it, so it was written ahead of the clock as well as on the wrong day. Both now say 5 September and
claim no exact minute, because the commit gives an upper bound and not a moment.

**The file names still say `2026-09-04` and `4sep`, deliberately.** They are referenced by the
MANIFEST, by check 1, by the verdicts document and by the status document, and they are the names
you know this pull by. Renaming would break four references to fix a label, so the correction is
written inside the record instead.

---

## 5. The fix list is wired into the page

`recommendations.js` now has its mount (`recommendation-blocks`) and its script tag in `index.html`,
above the investor block, so a founder reads what moves their range before they read who to take it
to. The CSS was already there. Like `investors.js`, nothing calls the renderer yet: that is the
wiring, below.

---

## 6. Engine to reveal: started

`selector/reveal_payload.py`, one function that assembles the whole reveal in one pass over the
engine, and `tools/check_reveal_payload.py` as **check 14**.

Today the football field is drawn from figures typed into the HTML, `investors.js` and
`recommendations.js` each expect their own payload from their own builder, and the honesty strings
reach nobody at all. Four sources means four chances for the page to show a range from one run and a
caveat from another.

One object now carries every lane on every basis with the founder's own figure beside each, the
honesty caveats split into inline and behind-the-disclosure, the fix list, both investor layers, and
the named comparables behind each lane. Every lane comes from **one** selection run, because letting
each block select its own peers is how a range and the investor list behind it end up describing
different companies.

Across all 102 fixtures:

```
BUILT     102 of 102 profiles assembled without an exception
HONESTY    96 carry at least one caveat  (these reach a founder for the first time)
FIX LIST  101 carry at least one dimension
INVESTORS 102 carry at least one callable house
NET+GROSS  32 lanes offer both revenue readings side by side, never merged
```

Two things are deliberately absent. **No price:** the payload carries multiples and the founder's
metric, and multiplying is the page's job, so the arithmetic the founder sees is the arithmetic the
hover explains. **No locking:** rule E8 says a locked lane is absent from the payload rather than
blurred, so the free and paid tiers are two different objects. The lock ruling is still open, so this
builds the whole payload and `lanes()` is the one place the free-tier filter will go once you rule.
Nothing there guesses at it.

---

## Golden moved, and here is the reason, as the rule requires

93 of 102 fixtures changed. **Nothing that was recorded before moved in value.** I checked every
fixture key by key: zero fixtures had any change outside `all_ranges`.

Two things happened inside `all_ranges`. It **gained** the private `REVENUE_GROSS` entry wherever a
gross round prices, which is the point of the change. It **lost** a `listed` sub-dict that was pure
duplication: for a fork with one listed basis, `all_ranges['listed']['REVENUE']` restated
`core_range` line for line, peer table and all, and it reached nothing, because the gate reads
`all_ranges` under the lane keys core, secondary and private and never under listed. Each lane is
now recorded only when that lane holds more than one reading, which is what the comment above it
always meant. The nine lending and exchange fixtures that already carried `all_ranges` on both lanes
are byte-identical to before.

Count in, count out: 102 fixtures before, 102 after. No data row was touched by any of this. The
private and listed CSVs are unchanged.

---

## Three things for you

**1. The gate number, settled 6 Sep.** Your rule is the product rule: the gross range shows when the
founder gives the gross number, the net range when they give the net number, both when they give
both. **The engine already does exactly that and never did anything else**: `founder_metric_for`
returns nothing when a figure is absent, so an unanswered measure is never priced.

My question was about check 8 and I framed it badly. Check 8 is not a founder. Its 102 test companies
give NO figures at all, and by your 3-Sep ruling it uses no revenue anywhere: it asks whether we can
narrow the world to a defensible comparable set, not what that set would value the company at.
Applying the product rule to it literally would score every fixture at zero lanes, including the net
ones. So it counts comparables found: the four gross rounds sitting in nursa's archetype are evidence
we hold, and it counts them. **Gate 95.** One line reverts it to 90 if you would rather the
scoreboard counted only what a net-only founder could reach; the six companies it turns on
(Mercor, Micro1, Jobandtalent, Incredible Health, Juspay, Cashfree) all disclose gross as their own
market's convention, so a real founder in those lanes will usually have the number.

**2. `basis_compatible()` was dead code. DELETED on your word, 6 Sep 00:20 UK.** It was defined,
documented at length, and **called from nowhere**, so the gross-versus-net fence was enforced
entirely by `basis_mult()` and has been all along. Four documents described the dead function as the
fence, which is the actual danger: a function that looks load-bearing, reads as load-bearing and is
documented as load-bearing gets trusted eventually by someone who does not check whether it runs.

Nothing was lost. Everything it knew is now written into `basis_mult`, including the two things it
learned the hard way in August: the lender guard, without which all four lender fixtures silently
emptied within minutes of it being switched on, and the rule that an absent basis is not a mismatch.
`basis_mult`'s docstring now says in as many words that it is the only fence and that changing it is
changing rule B3. The two 31-August documents that describe the deleted function keep their text and
carry a dated correction at the top, because they are the record of what was believed then; the live
instruction in `docs/brief-for-fable-basis-and-period.md` is corrected outright, since it told a
future session to wire a deleted function onto the listed lane.

Suite re-run after the deletion: golden 0 of 102 moved, gate still 95, only check 1 red.

**3. Three of the four held rows are already released.** Your `6433348` tonight set Moss (14.29x),
Restaurant365 (10.0x) and AuditBoard (15.0x) back into the medians. Only Udemy is still held
(`in_medians` false, 1.29x), which matches its being a different question: no standalone price. So
open decision 1 in the status box is closed except for Udemy.

---

## What is still open from the original list, and not done

- **The taxonomy rule** (catch-all archetypes need an industry match too). Ruling yours, build after
  the pilot, and Fable's matching to-do measures it first.
- **`tools/investor_check.py`** still refuses a callable house with no published cheque. Ten-line
  change, waiting on your word that the check follows your 2-September ruling.
- **Wix's archetype.**
- **The third growth definition** (CY+1 to CY+3), the last blocker on loading the public pull and
  the reason check 1 is red.

---

## The commit

Superseded by the block at the foot of the status document, which covers both sessions. Nothing
here was run on your machine.

---

# Second session, 6 September morning: your five rulings, applied

Suite after everything below: **gate 95 of 102, golden 0 of 102 moved, only check 1 red** (the
public pull, still unloaded). Fifteen checks.

## 1. A founder who gives no numbers at all

Your words: "what if the user does not want to give us the numbers at all? Then we should be able
just to show the peers and how they trade."

**Mostly already true, and worth saying why.** A range counts the comparable rounds that exist; only
turning it into a VALUE needs the founder's own figure. So all 102 fixtures, which carry no numbers
whatever, already produced charts. The count before this morning:

| chart | reached |
|---|---|
| public peers | 99 of 102 |
| private peers, net | 92 |
| private peers, gross | 37 |
| **private peers, per user** | **6** |

**The per-user one was the gap and it was a real one.** It opened only for five consumer archetypes,
or for a founder who had already typed a user count, so a founder who gives nothing almost never saw
it. But 48 fixtures hold two or more rounds in their own picked set priced per customer, per
merchant or per subscriber. The evidence was there and the profile was deciding.

It now also opens where the founder's OWN picked rounds can price it, two rounds minimum, which is
the same evidence test everything else uses and the same one that opened the gross lane. **Per-user
6 to 54 of 102. Fixtures able to show three or four charts, 33 to 63. Only 3 fixtures are left with
a single chart.** The payload carries a `charts` list in your reading order (public, private net,
private gross, private per user), each entry saying how many names stand behind it, the low, mid and
high, and whether a founder figure exists to price it.

**One thing you should rule on, and it is the first item on your list below.** The per-user charts
are far noisier than the revenue ones. Median high-to-low spread: 3.4x on the revenue charts, 33x on
the per-user ones, and the widest is 20,588x (unifold, two names). Everything above 6x already
renders as SCATTER rather than a clean band, so nothing dishonest reaches a founder, but a bar chart
with a 20,000x spread is not a comparison. My recommendation is a ceiling of about 100x, which would
stop 11 of the 56 count charts being drawn.

## 2. The free tier

Built as `build(prof, tier='free')`: public lane complete and free, every other lane blurred, and on
hover the comparable **names and round dates** with no multiples.

**This amends rule E8 and I want that in front of you rather than buried.** E8 said a locked lane is
ABSENT from the payload, never blurred. You have ruled that the names should be shown. So the rule
now splits the two halves: the NAMES are shown, the FIGURES still never leave the engine. A locked
lane in the free payload carries its shape, its size, its names and their dates, and no multiple, no
low, mid or high, and no founder value. The blur the founder sees is drawn over nothing, so there is
nothing to inspect. That keeps the half of E8 that mattered ("a lock that can be picked in ten
seconds tells a founder what we think of them") while doing what you asked.

Check 14 now walks all 102 free payloads and fails if any figure appears behind the lock, in the
lanes, in the charts, or in the lead range. The lead was the one I nearly missed: it carries the
private range through a second door.

**A gap this found.** The private lane has never carried a hover table at all. Only the listed lane
did. Nobody noticed while nothing read a payload, and your ruling is what needed it: hovering a
blurred private range must show names, and there was no list to show. It has one now, with the round
date beside each name, which a listed multiple does not need and a round does ("Vanta, Jul-23").

## 3. The growth definition, and what it unblocks

You said: CY+1 to CY+3 is 2026 to 2028, so CY+1 is the current year.

**I tested it rather than taking it on trust, because a year's error here silently corrupts the
growth bands.** The pull carries the year-on-year series beside the CAGR, so the window can be
recovered from the numbers:

| what was compounded | reproduces the printed CAGR on |
|---|---|
| the CY+2 and CY+3 rates, two years from the CY+1 level | **16 of 16 rows** |
| three years, CY+1 through CY+3 | 2 of 16 |
| two years from the CY+0 level | 2 of 16 |

So the printed CAGR spans two years starting at the CY+1 level, which on your convention is the
current year: the current year to two years out. **That is the same window as the other files' CY+0
to CY+2.** Two naming conventions, one measure.

**Which means a comment in the engine was wrong.** It said the two CAGRs were "anchored a year
apart" and "NOT the same measure", and that belief is what wrote the blocker into the raw file's
header in the first place. Corrected, with the measurement written into it. Nothing downstream was
broken by it: `g_rank` already accepted both.

**The pull is no longer blocked on a ruling. It is blocked only on the work of loading it, and I
have deliberately not rushed that at the end of a long session.** It is not a paste: the 14 rows
that load are a mixed bag (payments, business services, healthcare, learning, data) that fits no
existing peers file cleanly, so it needs a new file pair wired into the loader, 14 tag rows written
by hand, a MANIFEST row, and the leverage flag on Claritev and Skillsoft. It is the first item on my
list. The project's worst week started with a data load done in a hurry.

## 4. `investor_check.py`, explained and fixed

**What it is.** A reporting tool, not a gate on the product. It reads `data/investors.csv` and says
which investor rows are complete enough to show a founder. Its output is a sourcing list: the rows
it refuses are the rows somebody needs to go and finish.

**What was wrong.** It still enforced the rule you replaced on 3 September. Your ruling then was
that a house which has not published a first-cheque range is a fund with a sparse website, not an
inactive fund: benchmark.com is two office addresses, thrivecap.com is one sentence, and both led
seed rounds this year. The ENGINE has applied that since the day you said it. This check never did.
So the same suite run has been contradicting itself: `investors.py` renders 156 callable houses,
`investor_check.py` said 138.

**Fixed.** A missing cheque is now a soft note and the card says "First cheque not published".
**Refusals 18 to 5.** The five that remain all fail on a missing stage band, which is the half of
your ruling that still holds the line.

**One gap left, named not fixed, and it is on your list.** The engine does not require a stage band
at all, so it renders 156 against the check's 151. Your ruling says the stage band is what holds the
line, but a house that publishes no stage has not claimed one, which is the same argument that
unblocked the cheque and the geography. Either the engine starts filtering or the check stops
refusing. Five houses: Canaan, Founderful, Haystack, Techstars, Town Hall Ventures.

## 5. Udemy, released

You asked why it was held, and said to value an all-share deal on the acquirer's share price at the
transaction.

**It was held because the note said "no standalone price exists in the release". That note was
wrong, and reading the release again is what shows it.** From the 8-K exhibit already cited in the
row:

> "Udemy stockholders will receive 0.800 shares of Coursera common stock for each share of Udemy
> common stock"
>
> "Based on the closing prices of Coursera and Udemy common stock on **December 16, 2025**, the
> implied equity value of the combined company is approximately **$2.5 billion**."
>
> "existing Udemy stockholders are expected to own approximately **41%** of the combined company, on
> a fully diluted basis"

**So the figure we already hold is your method, written the other way round.** The $2.5bn is struck
on the acquirer's own market price on the transaction date, in the release's own words. 41 per cent
of it, $1,025m, is the market value of the stock consideration. It is arithmetic on two figures the
company published together, not a model.

**The one thing I am not glossing over**, and it is written into the row: the purest form of the
same calculation is 0.800 × Udemy fully diluted shares × Coursera's 16-Dec-2025 close. The release
states neither the share count nor the closing price, so that form cannot be computed from it. The
two should agree closely, because the $2.5bn was struck on those same closes, but they are not
identical constructions: the 41 per cent is a fully diluted split of the combined company. If anyone
later finds both figures and they disagree materially, this row is the one that is wrong.

Applied by `tools/apply_udemy_ruling_6sep.py`, idempotent. **268 rows in, 268 out, one changed, none
dropped.** The multiple, the denominator and every source URL are untouched.

**It prices on the GROSS lane only** (marketplace revenue booked gross of instructor payouts), so
under B3a it reaches a founder who gives a gross figure and no other. It now sits in five fixtures'
picked sets: honen, inato, bloomy, wondering, befreed.

## And the pricing, which needed no change

You said nothing contradicts, and you are right: free is the 24-hour banker read confirming the
comparables make sense, $250 unblocks the full field including private tiers and DCF, $750 is the
valuation presentation. I had it filed as a launch blocker on a misreading. It is off the list, and
the three tiers are now written into rule E8 in your words.

## The taxonomy, which is yours only in the sense of pasting a prompt

Yes: Fable does the work, and the only thing needed from you is to start that session with the
prompt, which is written out in full in the status document under "Fable, to-do". You rule on the
taxonomy afterwards, on Fable's measurement rather than on my description of it.

## SM&CR

Parked on your word. It does not gate the pilot: the fallback already written in stands, so the
pilot runs and invoices when compliance clears, and the date does not move.
