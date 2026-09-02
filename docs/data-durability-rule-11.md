# Data durability protocol, rule 11
2 September 2026, Opus. **For Fable to fold into the protocol in `Fairway_tracker.md`** — that
file is yours and I have not edited it.

## The rule

**11. A transcription schema must carry every column the source has.** When a screenshot or a
workbook is transcribed, the target file gets a column for each column in the source, even the
ones the immediate task does not need. A column that is dropped at transcription time is lost
silently, because it is neither written down nor visibly missing. If a column genuinely cannot
be read, it goes in as an empty column with a header, so the gap is countable.

## What happened, which is why the rule exists

Daniil sent the source columns of his private-transactions sheet twice: in the 16 screenshots of
1 September and again in the 12 of 2 September. Columns AA (valuation source) and AB (revenue /
metric source) were legible in both batches.

Both times the multiples in column Y were transcribed off those same images and the two source
columns beside them were not, because `data/raw/2026-09-01_private-transactions-daniil.csv` had
no field for them. Then he was asked for them a third time, in a pull list, as though they had
never arrived.

The screenshots were fine. The reading was fine. There was nowhere for the data to land, and
nothing counted its absence.

## Why rules 1 to 10 did not catch it

Every existing rule assumes that what arrives is either written down or visibly missing.

- Rule 1 was satisfied: the screenshots were archived to `data/raw/` in the same session and the
  transcription was written before any analysis touched it.
- Rule 2 was satisfied: the manifest row existed, with the row count.
- Rule 8 asks which rows entered a valuation and which did not — it counts ROWS, not COLUMNS.
- Rule 10's handover checks all run over the file as transcribed, so they can only ever see the
  columns that made it in.

A column that was never in the schema is invisible to all of them. That is the hole.

## Fixed

`tools/add_sheet_source_urls_2sep.py` reads both columns off the two screenshot batches already
in `data/raw/` and writes them in. **191 of 191 rows now carry both source URLs.**

The immediate effect: 70 rounds his sheet holds and we do not could not be inserted for want of
a source per figure. They now have one. The remaining work is ours, tagging each company into
the screening vocabulary, not Daniil's.

## Suggested check to add to rule 10

At handover, for every file in `data/raw/` that was transcribed from an image or a workbook:
count the columns in the source and the columns in the transcription, and say the two numbers.
If they differ, name the missing ones and say why.
