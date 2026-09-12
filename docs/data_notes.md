# HTS Data Notes

## Source

USITC REST export endpoint:
`https://hts.usitc.gov/reststop/exportList?from=X&to=Y&format=JSON&styles=true`

`from`/`to` are HTS number ranges. Use `from=0101&to=9999` to pull everything.

## Raw fields

| Field               | Type               | Notes                                                                                                                                                                                    |
| ------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `htsno`             | string             | Full HTS number, e.g. `"0101.21.00.10"`. **Can be empty string** on grouping/heading rows that have no code of their own.                                                                |
| `indent`            | string (numeric)   | Nesting depth in the tariff hierarchy, starting at `"0"`. Higher number = more deeply nested.                                                                                            |
| `description`       | string             | Text label. On leaf rows this is often terse ("Males", "Other") and only makes sense combined with its ancestors' descriptions.                                                          |
| `superior`          | `"true"` or `null` | Flags a row as a **grouping heading** (no rate of its own, exists to introduce a set of child rows below it). Not a parent-ID reference — see hierarchy note below.                      |
| `units`             | array              | e.g. `["No."]`. Empty array on heading rows.                                                                                                                                             |
| `general`           | string             | Column 1 General (MFN) duty rate. Empty on heading rows; populated on rate-bearing lines.                                                                                                |
| `special`           | string             | Column 1 Special program rate — often a rate plus a parenthetical list of trade program codes, e.g. `"Free (A+,AU,BH,CL,...)"`. Needs parsing later if we want individual program codes. |
| `other`             | string             | Column 2 (non-NTR / non-WTO) duty rate.                                                                                                                                                  |
| `footnotes`         | array or `null`    | Inconsistent — sometimes `[]`, sometimes `null`. Need to normalize when storing.                                                                                                         |
| `quotaQuantity`     | string or `null`   | Same inconsistency as footnotes.                                                                                                                                                         |
| `additionalDuties`  | string or `null`   | Inconsistent typing.                                                                                                                                                                     |
| `addiitionalDuties` | `null`             | **Typo'd duplicate field in USITC's real API** (extra "i"). Appears to always be null/unused — worth double-checking across more records, but likely safe to ignore/drop when storing.   |

## Hierarchy structure — the important part

There is **no parent-ID field**. The hierarchy is implicit, built from the **order of records in the array plus the `indent` value** — it works like a stack:

- A row's parent is the nearest preceding row with a lower `indent` value.
- Example from real data:
  - `0101` (indent 0) — chapter heading
    - `"Horses:"` (indent 1, `htsno` empty, `superior: true`) — grouping label, no code of its own
      - `0101.21.00` (indent 2) — "Purebred breeding animals" — **has rates** (`general: "Free"`, `other: "Free"`)
        - `0101.21.00.10` (indent 3) — "Males" — no rates of its own (statistical suffix only, rate is inherited from parent line)
        - `0101.21.00.20` (indent 3) — "Females" — same

**Implication for the diff engine and schema:** only some rows are actual "rate-bearing" tariff lines; many rows exist purely for structure/grouping or statistical breakdown (e.g. splitting "Males" vs "Females" for import statistics, both under the same duty rate). We'll need to decide whether `line_items` stores _every_ row (safest — nothing gets silently dropped) or only rate-bearing rows. Recommendation: **store every row**, including headings, since a description-wording change on a heading is still a real change worth catching, and we can filter/aggregate at query time rather than losing data at ingestion time.

## Chapter / Section

- **Chapter**: not a separate field — derive from the first 2 digits of `htsno` when present. For rows where `htsno` is blank (like the "Horses:" grouping row), derive chapter from the nearest ancestor's `htsno` instead.
- **Section**: not in the API at all. Sections group chapters (e.g. Section I = Chapters 1–5, live animals & animal products) and must come from a **static lookup table we build ourselves** — only 22 sections, one-time effort.

## Revision / last-modified

No per-line revision or date field exists. Confirmed absent from every record seen so far. Revision tracking happens at the whole-schedule level (USITC's separate "Change Record" page), not per row — this confirms our diffing approach (compare whole snapshots) is the right one, since the data itself gives us no shortcut.

## Open questions / things to verify with more data

- Does `additionalDuties` ever get populated on any row, or is it always empty in practice? (Relevant to Section 301/232 tariffs, which may show up here or in footnotes instead.)
- Confirm `footnotes` inconsistency (`[]` vs `null`) is truly random or tied to something (e.g. older vs newer chapters).
