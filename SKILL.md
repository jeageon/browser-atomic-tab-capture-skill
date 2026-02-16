---
name: browser-atomic-tab-capture
description: Capture Google Scholar/KAIST (or any search pages) through OpenClaw Chrome Relay using a stable "1 URL = 1 tab" flow (open → snapshot → close). Use when browser automation suffers from `tab not found`, session drops after click/navigate, or when you need deterministic page-by-page title extraction without tab reuse.
---

# Browser Atomic Tab Capture

Use Atomic Tab flow to avoid relay/session drift:
- Open fresh tab for one URL
- Snapshot once
- Close the tab immediately
- Repeat for next URL

## Workflow

1. Build URL list explicitly (e.g., `start=0,10,20` or `offset=0,10,20`)
2. Run `scripts/atomic_tab_capture.py` to collect titles from snapshots
3. Review output CSV (`source,page,title,url`)
4. Compare captured titles with local master dataset (title/DOI normalization step)

## Quick Start

```bash
python3 skills/browser-atomic-tab-capture/scripts/atomic_tab_capture.py \
  --profile chrome \
  --output reports/atomic_capture.csv \
  --url "scholar|0|https://scholar.google.com/scholar?start=0&q=%22C1+assimilation%22+methanol+methylotroph&hl=ko&as_sdt=0,5" \
  --url "scholar|10|https://scholar.google.com/scholar?start=10&q=%22C1+assimilation%22+methanol+methylotroph&hl=ko&as_sdt=0,5" \
  --url "kaist|0|https://kaist-primo.hosted.exlibrisgroup.com/primo-explore/search?query=any,contains,%22C1%20assimilation%22%20methanol%20methylotroph&search_scope=primo_central_scope&vid=KAIST&lang=ko_KR&offset=0"
```

## Preset File Format

Use `--input` with CSV:

```csv
source,page,url
scholar,0,https://scholar.google.com/scholar?start=0&q=%22C1+assimilation%22+methanol+methylotroph&hl=ko&as_sdt=0,5
kaist,0,https://kaist-primo.hosted.exlibrisgroup.com/primo-explore/search?query=any,contains,%22C1%20assimilation%22%20methanol%20methylotroph&search_scope=primo_central_scope&vid=KAIST&lang=ko_KR&offset=0
```

Run:

```bash
python3 skills/browser-atomic-tab-capture/scripts/atomic_tab_capture.py \
  --profile chrome \
  --input reports/atomic_urls.csv \
  --output reports/atomic_capture.csv
```

## Operational Rules

- Never reuse tabs for page transitions during unstable relay periods.
- Do not chain click → navigate → snapshot in the same tab when `tab not found` is observed.
- Keep extraction to headings/titles first; enrich DOI/authors in a second normalization pass.
- If no tab is attached, ask user to click Chrome Relay extension icon on target tab (ON state).

## Resources

### scripts/
- `atomic_tab_capture.py`: deterministic open/snapshot/close collector with retry and CSV output.

### references/
- `incident-format.md`: 6-field incident report format for relay failures.
