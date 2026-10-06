---
name: trackiq-amazon-search-term-harvester
description: Finds the Amazon search terms that already convert above break-even but have no keyword of their own, and turns them into an upload-ready Sponsored Products bulk file with exact-match keywords and suggested bids. Checks every candidate against the existing targets so nothing is proposed twice. Use when the user asks about harvesting search terms, promoting search terms to keywords, mining auto campaigns, converting search terms, keyword expansion, what should we add as exact match, or finding new keywords from the search term report.
---

# Search-Term Harvester

The mirror of the Wasted-Spend Sweeper. That one cuts what is not paying;
this one **promotes what already is.**

A search term converting above break-even inside an auto or broad campaign is
being bought at whatever bid the match type happens to produce. Given its own
exact-match keyword it can be bid deliberately.

Output is a branded HTML report plus an Amazon Sponsored Products bulk file.

## Requires

- The TrackIQ MCP, for `list_marketplaces`, `get_search_terms`, `get_targets`
  and `get_ad_groups`.
- **A break-even ROAS** — ask for it. Gross margin divided into 1. Without it
  the report cannot say which terms are worth promoting, only which convert.
  Default 2.0x, labelled an assumption.
- **A destination ad group.** The search-term data carries no campaign or ad
  group, so nothing can be routed automatically. See non-negotiable 1.
- Nothing else. No filesystem, no shell, no internet. `assets/build_bulk.py`
  writes the workbook if a shell is available; the format is in
  `assets/bulk-format.md` either way.
- **Without the MCP:** works from a Search Term Report export plus a keyword
  export for the dedupe.

## First run

Fill in a copy of `assets/account.example.md` saved as account.md beside the
skill. Every TrackIQ skill reads the same file, so an account already set up
for another TrackIQ report needs nothing added here.

If the runtime has no filesystem, print the same block and ask the user to
paste it into their project instructions once.

## Read first

- `assets/pulls.md` — the calls, and the missing-campaign problem
- `assets/method.md` — the four filters, the bid derivation, the dedupe
- `assets/bulk-format.md` — the exact bulk sheet columns Amazon accepts
- `assets/checks.md` — what to verify before anything is uploaded

Copy `assets/report-template.html` and replace every `{{TOKEN}}`.

## Non-negotiables

1. **`get_search_terms` has no campaign_id and no ad_group_id.** A harvested
   term therefore cannot be placed automatically — there is nothing to say which
   campaign it came from. **Ask the user which ad group each group of terms
   should land in**, or produce the bulk file with a single destination they
   name. Never guess an ad group ID; a wrong one either fails the upload or
   silently creates keywords in the wrong place.
2. **Dedupe against `get_targets` before proposing anything.** A term that
   already exists as an exact-match keyword must not be proposed again — the
   upload will either error or create a duplicate that splits the auction
   against itself. Match case-insensitively on trimmed text.
3. **Promote on orders, not on clicks.** A term with 40 clicks and no orders is
   the Sweeper's problem, not this skill's. Require a minimum order count.
4. **Break-even is the bar, not ROAS above 1.** A 1.4x ROAS term is losing money
   on most grocery margins. Use the client's break-even and say what was used.
5. **ASIN-looking queries are not keywords.** Search terms like `b07k8vrtxg` are
   competitors' ASINs typed into search. Route those to **product targeting**,
   not to an exact keyword, and say so. Flag them separately.
6. **Branded terms are separated from generic.** Harvesting your own brand name
   into exact match usually just moves spend around. Show both, default to
   proposing only the generic ones, and let the user opt in to branded.
7. **The suggested bid is derived from the term's own economics**, not from a
   percentage of the current CPC. The arithmetic is in `assets/method.md`.
8. **Nothing is uploaded.** This produces a file a human reviews and applies.
9. **Never print `account_id`.**

## What it pairs with

`trackiq-wasted-spend` is the other half of the same hour's work: run the
sweeper to cut, run the harvester to grow, upload one file. Both write the same
bulk-sheet format, so the two can be combined into a single upload if the
client prefers.

`trackiq-category-priority-keywords` says which terms *should* matter by search
volume. This one says which already do by conversion. Where those two lists
disagree is usually the most interesting conversation in the account.

## Delivery

The output is produced in the chat first. Delivery is the last step and the
method comes from the Delivery block in account.md — never ask per run.

| Method | What to do | Needs |
|---|---|---|
| `in-chat` | Return the report. The default, and the fallback for every other method. | nothing |
| `file` | Write it beside the skill, dated. | a filesystem |
| `slack` | Post the headline findings as text, then upload the file. | a connected Slack tool |
| `n8n` | POST it to the configured webhook. | network access |
| `email` | Hand it to the connected mail tool. | a connected mail tool |

Confirm before the first outward send of a session, fall back to in-chat
loudly when a method is unavailable, and never substitute a different
outward channel.

## Version

`trackiq-amazon-search-term-harvester` v1.0.0 (2026-09-18).

If the user asks whether this skill is current, fetch
`https://trackiq.com/skills/registry.json`, compare the `version` field for
`trackiq-amazon-search-term-harvester`, and if it is newer, give them the download link
and the one-line changelog. Do not fetch at any other time.
