# The pull sequence

## 0. Account and inputs

`list_marketplaces` first — several TrackIQ MCPs can be connected with
identical tool names. Never print `account_id`.

Then ask for:

| Input | Default | What it is |
|---|---|---|
| Break-even ROAS | 2.0x | 1 / gross margin. The bar a term must clear. |
| Minimum orders | 3 | below this the ROAS is one lucky sale |
| Window | 60 days | long enough for orders to accumulate per term |
| Destination ad group | **none** | see step 3 — this is the hard part |

## 1. Search terms

```
get_search_terms(account_id, start_date, end_date, limit=500)
```

Returns per query: `ad_type`, `query`, `impressions`, `clicks`, `spend`,
`sales`, `orders`, `units`, `acos`, `roas`, `cpc`, `ctr`, `cvr`.

Use a **60-day window**, longer than the sweeper's 30. Cutting a loser needs
recent evidence; promoting a winner needs enough orders to trust the rate, and
most terms convert too rarely to judge in a month.

Paginate until a page returns fewer rows than the limit.

## 2. Existing targets — the dedupe source

```
get_targets(account_id, start_date, end_date, limit=500)
```

Returns `target_id`, `ad_group_id`, `record_type`, `target_type`,
`targeting_text`, `match_type`, `state`, `bid`, plus performance.

- `target_type: "KEYWORD"` rows carry the keyword in `targeting_text`.
- `target_type: "PRODUCT"` rows have `targeting_text: null` — they are ASIN
  targets, not keywords. Exclude them from the keyword dedupe set, and use them
  for the ASIN-query dedupe instead.

Build the set of existing keyword texts, lowercased and trimmed. **Include
paused keywords.** A keyword that exists in a paused state still blocks a clean
add and, more importantly, somebody paused it on purpose — proposing it again
without acknowledging that is how a harvester loses trust.

## 3. The missing campaign — read this before promising anything

`get_search_terms` returns **no `campaign_id` and no `ad_group_id`.** The
query, its spend and its orders, and nothing about where it happened.

That means the skill **cannot** work out which auto campaign a term came from,
or which ad group its exact-match version belongs in. The bulk file needs an
ad group ID in every row, and there is no data path to it.

Two honest ways through, in order of preference:

**A. Ask.** Show the harvested list grouped by product theme and ask the user
which ad group each group goes to. `get_ad_groups` gives the list of ad groups
with their campaign IDs and names to choose from:

```
get_ad_groups(account_id, start_date, end_date, limit=200)
```

**B. One destination.** If the user names a single ad group — often a dedicated
"harvested exact" ad group — put every row there. Say plainly on the report
that all terms were routed to one place and the client may want to split them.

**Never** infer a destination from a campaign name that happens to contain a
similar word. Getting this wrong creates keywords in the wrong ad group where
they bid against the client's own campaigns, and it is invisible until the ACOS
moves.

## 4. Optional context

- `get_campaigns` — to name the campaigns behind the ad groups when presenting
  choices to the user
- `get_search_query_performance` — the SQP view of the same terms, for search
  volume beside conversion. Note it is weekly, Sunday to Saturday, and
  ingestion is intermittent; missing weeks are normal.
