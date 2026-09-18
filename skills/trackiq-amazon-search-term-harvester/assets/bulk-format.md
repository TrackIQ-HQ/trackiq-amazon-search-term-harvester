# The Amazon bulk sheet

The sheet Amazon accepts under **Sponsored Products → Bulk operations**. One
row per new target. Sheet name `Sponsored Products Campaigns`.

| Column | New keyword | ASIN query (product target) |
|---|---|---|
| Product | `Sponsored Products` | `Sponsored Products` |
| Entity | `Keyword` | `Product Targeting` |
| Operation | `create` | `create` |
| Campaign ID | destination campaign | destination campaign |
| Ad Group ID | destination ad group | destination ad group |
| Keyword ID | *blank* — Amazon assigns | *blank* |
| Keyword Text | the query, trimmed, lowercased | *blank* |
| Product Targeting Expression | *blank* | `asin="B0XXXXXXXX"` |
| Match Type | `exact` | *blank* |
| State | `enabled` | `enabled` |
| Bid | suggested bid, 2dp | suggested bid, 2dp |
| TrackIQ reason | why this row exists | why this row exists |

## Rules the upload enforces

- **Keyword ID must be blank on a create.** A populated ID makes it an update
  against a keyword that does not exist, and the row fails.
- **Campaign ID and Ad Group ID are mandatory.** There is no "put it wherever"
  option. This is why the destination is a user input — see `assets/pulls.md`.
- **Bid must be above the marketplace minimum** (US: $0.02) and inside any
  campaign bid rules already in force.
- Match type `exact` on a keyword row; blank on a product target.
- Text is matched case-insensitively by Amazon, but send it lowercased and
  trimmed so the file is diffable between runs.

## The reason column

Amazon ignores any column it does not recognise, so the reason rides along
harmlessly and the file stays auditable. Keep it. A reviewer who cannot see why
a row is there will not upload the file, and they are right not to.

## Before uploading

1. Open it. Look at ten rows.
2. Check the campaign and ad group IDs are the ones intended — a transposed ID
   creates keywords in the wrong place and it is invisible until ACOS moves.
3. Upload to the Bulk Operations page and read the validation result before
   confirming. Amazon reports row-level errors; fix and re-upload rather than
   confirming a partial file.
4. Add each promoted term as a **negative exact** in the campaign that served
   it. The search term data does not say which campaign that was, so this step
   is manual. Skipping it leaves the new keyword bidding against its own source.
