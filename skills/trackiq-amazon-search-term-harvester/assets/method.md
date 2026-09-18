# Method

## The four filters, in order

A term is a candidate only if it passes all four.

```
1. orders   >= min_orders                       # default 3
2. roas     >= break_even_roas                  # default 2.0
3. text not in existing_keyword_texts           # case-insensitive, trimmed
4. clicks   >= 10                               # enough traffic to have a rate
```

Filter 3 is the one that matters. Everything else is arithmetic; the dedupe is
what stops the skill proposing work the account already did.

Report how many terms were dropped by each filter. "412 terms, 38 converted
above break-even, 21 already exist as keywords, 17 proposed" is a far more
useful summary than a list of seventeen rows, because it shows the account is
mostly already harvested — or that it is not.

## Four kinds of candidate, kept apart

**Generic keywords.** The default proposal. Exact match, new keyword.

**Branded.** The query contains the brand name or an obvious misspelling of it.
These convert brilliantly and harvesting them into exact match usually just
re-buys traffic the brand would win anyway. Show them, total them, and leave
them **unchecked by default**. Let the user opt in.

**ASIN queries.** The query matches `^b0[a-z0-9]{8}$` — a competitor's ASIN
typed into search. These are real and often convert well, but an exact-match
*keyword* on an ASIN string is not how to buy them. Route them to **product
targeting** in the bulk file (`Entity: Product Targeting`), and say why.

**Long queries.** More than six words. Usually a one-off shopper sentence that
will never be searched again. Keep them out of the main proposal; list them as
a curiosity if there are interesting ones.

## The suggested bid

Derive it from the term's own economics, not from a multiple of its CPC:

```
aov          = sales / orders
cvr          = orders / clicks
max_cpc      = aov x cvr / break_even_roas       # the bid that lands at break-even
suggested    = max_cpc x 0.75                    # start below the ceiling
```

`max_cpc` is what a click is worth at break-even given how this term actually
converts. Starting at 75% of it leaves room to raise on evidence — and a new
exact keyword usually converts a little worse than the broad match it came from,
because the broad match was cherry-picking.

**Floor it at the current CPC x 0.5 and cap it at the current CPC x 1.5.** The
formula misbehaves on a term with two orders and a huge AOV, and a bid ten times
the current CPC will spend the client's month in an afternoon.

Show `max_cpc`, the suggested bid and the current CPC side by side. A client who
can see the ceiling will argue about the right number instead of the method,
which is the better argument to have.

## Negative keywords in the source campaign

A term promoted to its own exact keyword should usually be negated in the
campaign it came from, or the two bid against each other.

**This skill cannot do that** — see `assets/pulls.md`. There is no campaign
attached to a search term, so there is nowhere to put the negative. Say this
plainly on the report and in the handover note: *"Each promoted term should be
added as a negative exact in the campaign that originally served it. The search
term data does not say which campaign that was, so it has to be done in the
console."*

Do not quietly omit it. It is the step that makes harvesting work, and a client
who does not know to do it will see their ACOS get worse.

## The bulk file

Amazon Sponsored Products bulk operations, one row per new keyword:

| Column | Value |
|---|---|
| Product | `Sponsored Products` |
| Entity | `Keyword` (or `Product Targeting` for ASIN queries) |
| Operation | `create` |
| Campaign ID | the destination campaign, from the user |
| Ad Group ID | the destination ad group, from the user |
| Keyword ID | **blank** — Amazon assigns it |
| Keyword Text | the query, trimmed and lowercased |
| Match Type | `exact` |
| State | `enabled` |
| Bid | the suggested bid |
| TrackIQ reason | orders, ROAS and the max CPC it was derived from |

Keep the reason column. A bulk file whose rows cannot be explained does not get
uploaded.

`assets/build_bulk.py` writes this if a shell is available. If it cannot run,
the table above is the whole specification — build the sheet by hand.

## What this skill does not do

- **It does not place the negatives.** See above. The data is not there.
- **It does not choose the destination ad group.** That is a user decision
  every time.
- **It does not upload.** A human reviews the file and applies it.
