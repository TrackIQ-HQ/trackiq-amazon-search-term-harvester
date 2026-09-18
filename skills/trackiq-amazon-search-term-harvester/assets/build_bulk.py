"""Write the Amazon Sponsored Products bulk sheet for harvested search terms.

An accelerant, never a dependency. If this cannot run, assets/method.md has the
full column specification — build the sheet by hand and nothing is lost.

    python build_bulk.py candidates.json out.xlsx

candidates.json is a list of objects:

    {"query": "patio string lights", "orders": 9, "clicks": 61, "spend": 140.2,
     "sales": 412.5, "cpc": 2.30, "bid": 1.94, "max_cpc": 2.59, "kind": "generic",
     "campaign_id": "123...", "ad_group_id": "456..."}

Falls back to CSV when openpyxl is absent.
"""
import json
import sys

COLUMNS = ["Product", "Entity", "Operation", "Campaign ID", "Ad Group ID",
           "Keyword ID", "Keyword Text", "Match Type", "State", "Bid",
           "TrackIQ reason"]


def rows(candidates):
    out = []
    for c in candidates:
        if c.get("kind") == "branded" and not c.get("include_branded"):
            continue
        asin_query = c.get("kind") == "asin"
        roas = c["sales"] / c["spend"] if c["spend"] else 0
        out.append([
            "Sponsored Products",
            "Product Targeting" if asin_query else "Keyword",
            "create",
            c["campaign_id"],
            c["ad_group_id"],
            "",
            c["query"].strip().lower(),
            "" if asin_query else "exact",
            "enabled",
            round(c["bid"], 2),
            "%d orders, %.2fx ROAS, break-even CPC %.2f, current CPC %.2f"
            % (c["orders"], roas, c["max_cpc"], c["cpc"]),
        ])
    return out


def check(candidates, built):
    """The self-check. A bulk file nobody verified is a bulk file nobody uploads."""
    kept = [c for c in candidates
            if not (c.get("kind") == "branded" and not c.get("include_branded"))]
    assert len(built) == len(kept), "row count does not match the kept candidates"

    texts = [r[6] for r in built]
    assert len(texts) == len(set(texts)), "duplicate keyword text in the bulk file"

    for r, c in zip(built, kept):
        assert r[3] and r[4], "every row needs a campaign and ad group ID"
        assert r[5] == "", "Keyword ID must be blank on a create"
        assert r[9] > 0, "no zero or negative bids"
        assert r[9] <= c["cpc"] * 1.5 + 1e-9, "bid above the 1.5x current CPC cap"
    return True


def main(src, dest):
    candidates = json.load(open(src, encoding="utf-8"))
    built = rows(candidates)
    check(candidates, built)

    try:
        from openpyxl import Workbook
    except ImportError:
        import csv
        dest = dest.rsplit(".", 1)[0] + ".csv"
        with open(dest, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(COLUMNS)
            w.writerows(built)
    else:
        wb = Workbook()
        ws = wb.active
        ws.title = "Sponsored Products Campaigns"
        ws.append(COLUMNS)
        for r in built:
            ws.append(r)
        wb.save(dest)

    print("wrote %s: %d rows" % (dest, len(built)))


def demo():
    """Runnable self-check: python build_bulk.py"""
    c = [dict(query="String Lights ", orders=9, clicks=61, spend=140.2, sales=412.5,
              cpc=2.30, bid=1.94, max_cpc=2.59, kind="generic",
              campaign_id="111", ad_group_id="222"),
         dict(query="brandname lights", orders=40, clicks=90, spend=100.0, sales=900.0,
              cpc=1.11, bid=1.50, max_cpc=2.00, kind="branded",
              campaign_id="111", ad_group_id="222")]
    built = rows(c)
    assert len(built) == 1, "branded candidate must be excluded by default"
    assert built[0][6] == "string lights", "keyword text must be trimmed and lowered"
    assert built[0][7] == "exact"
    assert check(c, built)

    c[1]["include_branded"] = True
    assert len(rows(c)) == 2, "opting in must include the branded row"
    print("self-check passed")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        demo()
