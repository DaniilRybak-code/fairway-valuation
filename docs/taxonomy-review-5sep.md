# The archetype taxonomy, measured. 5 September 2026

Daniil, 5-Sep: "can we look deeper into the taxonomy and refine it as the first step?"

This is step one: the measurement and a proposal. **Nothing is re-tagged here.** Re-tagging 828 rows
is a decision, not a chore, and it changes what every founder is compared against.

## What we have

34 archetypes across 511 listed and 317 private rows, 1,281 archetype slots in total (each row
carries a primary and often a secondary).

| archetype | slots |
|---|---|
| Vertical Software | 120 |
| Lending & Credit | 111 |
| Data, AI & Developer Tools | 98 |
| Business Applications | 76 |
| Commerce & Payments Software | 69 |
| Third-Party Marketplace | 69 |
| ... 28 more, from 61 down to 4 | |

**The big four carry 32 per cent of all slots.** Dating & Social Network carries 4.

## The problem, in one bucket

These are all tagged **Vertical Software** and they are all in one another's comparable pool:

| company | what it actually is |
|---|---|
| Intercontinental Exchange, B3, JSE | stock and derivatives exchanges |
| Fiserv, FIS, Jack Henry, Alkami | core banking systems |
| Guidewire, FINEOS, CCC | insurance core systems |
| Cars.com, Autotrader | auto classifieds |
| AppFolio | property management |
| Amdocs, Cerillion | telecom billing |
| Intapp, LegalZoom | legal software |
| Kinaxis | supply chain planning |
| Alarm.com | smart home security |
| Constellation Software | a serial acquirer of all of the above |

A founder building restaurant back-office software is in the same archetype as the New York Stock
Exchange. **"Vertical Software" is not an archetype. It is the absence of one**: it says the company
sells software to one industry without saying which, and the whole point of an archetype is to say
what kind of business something is.

`Data, AI & Developer Tools` is the same shape at 98 slots, and it is the bucket that made
GitLab a comparable for a prompt-to-app builder and Perplexity a comparable for a social publishing
API. Both are true statements about the label and neither is true about the businesses.

## The proposal, and it is cheap

**We already hold the missing dimension.** Every row carries an `industry` field: Financial
Services, Healthcare & Life Sciences, Legal & Professional Services, Automotive, Hospitality. For a
catch-all archetype that field is the archetype's missing half.

So rather than splitting 120 rows into eight new archetypes and re-tagging everything:

> **For a defined list of CATCH-ALL archetypes, an archetype match only counts when the industry
> matches too.** Vertical Software plus Hospitality matches Vertical Software plus Hospitality. It
> does not match Vertical Software plus Financial Services.

Candidate catch-all list, to be ruled on: `Vertical Software`, `Data, AI & Developer Tools`,
`Business Applications`, `Cloud & Infrastructure`. Everything else is specific enough to stand on
its own (`Card Issuing & BaaS`, `Cross-Border & FX`, `Online Learning`).

The cost is that a horizontal founder in a catch-all archetype loses matches, which is exactly the
case the archetype fallback now rescues and records.

## What this is not

It is not a re-tag, it is not urgent before the pilot, and it should not be done in the same week as
the launch. It is one ruling and about twenty lines of code, and it is the thing that makes the
relevance gate arguable rather than a blunt instrument.
