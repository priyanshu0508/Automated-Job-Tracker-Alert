```
| Area | Required change | Root cause | Resolution |
|---|---|---|---|
```

```
| Overview: Budget Flow | Show correct data | Placement/budget data was partly
derived from fallback/guessed campaign-name logic instead of reliable synced
placement metrics. | Dashboard now uses synced placement rows and avoids showing
guessed placement distribution when placement metrics are unavailable. |
```

```
| Overview: Placement Distribution | Show correct placement values | Same root
cause: fallback placement bucketing produced wrong Top of Search/Product
Pages/Rest of Search totals. | Placement distribution now comes from normalized
placement metrics only. |
```

```
| Campaign cards: lakh display | Fix `x,xx,…` style broken display |
Currency/number formatting and constrained card text caused Indian-format
numbers to truncate or display awkwardly. | Formatting was moved to `en-IN` /
INR-aware display and UI font/layout was adjusted. |
```

```
| Campaign table sorting | Sort every metric high-to-low and low-to-high |
Sorting was previously limited, mainly around Spend. | Shared campaign analytics
table now has sortable headers for Spend, Sales, ACOS, ROAS, CTR, CVR, CPC,
Orders, and Trend. |
```

```
| Sponsored Brand data | Correct Sponsored Brand data in campaign
breakdown/spend/sales | Sponsored Brand/SBV ad types were not normalized
robustly, and mixed metric evidence could classify campaigns incorrectly. |
SB/SBV normalization and evidence-based campaign type resolution were added. |
```

```
| Portfolio card/table issues | Same card formatting and sorting fixes on
Portfolio | Portfolio summary and table were not fully aligned; sorting was
partly local/current-page based. | Portfolio now loads summary/table separately,
supports full metric sorting, and uses INR/Indian number formatting. |
```

```
| Portfolio Breakdown & Budget Distribution UI | Better UI with scrolling inside
cards | Wide breakdown content overflowed fixed cards. | Horizontal/contained
scrolling was added where table/card content can exceed card width. |
```

```
| Recommendations performance | Stop slow reloads when switching
tabs | Recommendation queries were refetching/restarting on tab/page changes and
filter state was not persisted well. | Recommendation filters are stored,
previous data is kept, cache/stale timings were added, and window-focus refetch
was disabled. |
```

```
| Recommendation logic | Match backend logic | Some frontend recommendation
behavior/action mapping diverged from backend rule criteria. | Recommendation
application now builds an explicit backend action plan and logs/applies through
backend mutations. |
```

```
| Admin panel | Fetch seller portfolios, INR budget, more than 100 SKUs |
Hardcoded `$`, static/limited portfolio/product loading, and default 100-item
limits. | Admin panel now fetches portfolios, uses INR symbol, requests larger
portfolio page size, and paginates product selection. |
```

```
| Base Level Insights | Multi-select pause/add negative in bulk | Bulk
selection/actions were not available from the Base Level table . | Selection
state, checkboxes, expandable keyword-row selection, and a bulk action bar were
added for pausing selected campaigns and adding selected SP keyword/search-term
values as negatives. |
```

