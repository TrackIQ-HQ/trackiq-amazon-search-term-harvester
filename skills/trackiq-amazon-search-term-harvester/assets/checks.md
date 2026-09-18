# Before you send it

## 1. The dedupe

- **Every proposed term was checked against `get_targets`.** This is the one
  that matters; a harvester that re-proposes existing keywords is worse than no
  harvester.
- The comparison was case-insensitive and trimmed on both sides.
- **Paused keywords were included** in the existing set. Somebody paused them
  deliberately.
- The report states how many candidates were dropped as already existing.

## 2. The filters

- The funnel is shown: terms pulled → converted above break-even → already
  existed → proposed. Four numbers, so the client can see whether the account is
  already well harvested.
- Break-even ROAS is stated, with whether it came from the client or is the 2.0x
  default.
- Minimum orders and the window are stated.

## 3. The categories

- Branded terms are separated and **not included in the bulk file by default**.
- ASIN-pattern queries are routed to product targeting, not to exact keywords.
- Queries over six words are held out of the main proposal.
- Each category shows its own count and spend.

## 4. The bids

- Every bid sits between 0.5x and 1.5x the term's current CPC.
- `max_cpc`, the suggested bid and the current CPC appear together on each row.
- No bid is below the marketplace minimum.
- A term with an implausible AOV (one order, huge basket) was not allowed to
  drive a large bid — check the top three bids by hand.

## 5. The destination

- **Every bulk row has a real campaign ID and ad group ID**, supplied by the
  user.
- No destination was inferred from a campaign name.
- If everything went to one ad group, the report says so and suggests splitting.

## 6. The negatives

- The report **states in plain words** that each promoted term needs a negative
  exact in its source campaign, and that this skill cannot place it because the
  search term data carries no campaign.
- This appears in the handover note, not only in a methods footnote.

## 7. The file

- `Keyword ID` is blank on every row.
- No duplicate keyword text.
- Row count matches the proposed count on the report. If the HTML and the
  workbook disagree, one of them was built from a different filter — fix the
  builder, not the number.
- The reason column is populated on every row.

Run `python assets/build_bulk.py` with no arguments; its self-check must pass.

## 8. Render check

```js
({ overflows: document.documentElement.scrollWidth > document.documentElement.clientWidth,
   tables: document.querySelectorAll('table').length,
   rows: [...document.querySelectorAll('table')].map(t => t.querySelectorAll('tbody tr').length),
   logos: [...document.images].map(i => i.naturalWidth > 0) })
```

`overflows` false, `logos` all true, and the proposal table's row count equal to
the number of rows in the workbook. Then look at it; if it will not paint, say
the check was structural.

## 9. Ship

Save as `<client>-search-term-harvest-<YYYY-MM-DD>.html` and
`<client>-harvest-bulk-<YYYY-MM-DD>.xlsx`.

Hand over the workbook and the negative-keyword instruction together. One
without the other makes the account worse.
