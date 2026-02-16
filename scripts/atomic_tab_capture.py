#!/usr/bin/env python3
import argparse
import csv
import json
import re
import subprocess
import sys
import time
from pathlib import Path


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def parse_urls(args):
    jobs = []
    if args.input:
        with open(args.input, encoding="utf-8", newline="") as f:
            rd = csv.DictReader(f)
            for r in rd:
                jobs.append((r.get("source", "unknown"), r.get("page", ""), r["url"]))
    for item in args.url:
        # format: source|page|url
        parts = item.split("|", 2)
        if len(parts) != 3:
            raise ValueError(f"Invalid --url format: {item}")
        jobs.append((parts[0], parts[1], parts[2]))
    return jobs


def extract_titles(snapshot_text):
    titles = []
    for m in re.finditer(r'heading "([^"]+)"', snapshot_text):
        t = m.group(1).strip()
        if len(t) < 12:
            continue
        if "nui.aria" in t.lower():
            continue
        titles.append(t)
    return titles


def main():
    ap = argparse.ArgumentParser(description="Atomic tab capture via OpenClaw browser CLI")
    ap.add_argument("--profile", default="chrome")
    ap.add_argument("--input", help="CSV file with source,page,url")
    ap.add_argument("--url", action="append", default=[], help="source|page|url")
    ap.add_argument("--output", required=True)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--sleep", type=float, default=0.4)
    args = ap.parse_args()

    jobs = parse_urls(args)
    if not jobs:
        print("No URLs provided. Use --input or --url", file=sys.stderr)
        return 2

    rows = []
    errors = []

    for source, page, url in jobs:
        snapshot = None
        for attempt in range(1, args.retries + 1):
            rc, out, err = run(["openclaw", "browser", "--browser-profile", args.profile, "open", url, "--json"])
            if rc != 0:
                errors.append((source, page, "open", attempt, (err or out).strip()))
                time.sleep(args.sleep)
                continue

            target_id = json.loads(out).get("targetId")
            rc, snap, serr = run([
                "openclaw", "browser", "--browser-profile", args.profile,
                "snapshot", "--target-id", target_id, "--format", "ai", "--depth", "2"
            ])
            run(["openclaw", "browser", "--browser-profile", args.profile, "close", target_id])

            if rc == 0:
                snapshot = snap
                break

            errors.append((source, page, "snapshot", attempt, (serr or snap).strip()))
            time.sleep(args.sleep)

        if snapshot is None:
            continue

        for title in extract_titles(snapshot):
            rows.append({"source": source, "page": page, "title": title, "url": url})

    # dedupe by source+title
    uniq = []
    seen = set()
    for r in rows:
        k = (r["source"], re.sub(r"\s+", " ", r["title"].lower()).strip())
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["source", "page", "title", "url"])
        wr.writeheader()
        wr.writerows(uniq)

    print(f"captured={len(uniq)}")
    print(f"errors={len(errors)}")
    for e in errors[:20]:
        print("ERR", e[0], e[1], e[2], e[3], e[4][:140].replace("\n", " | "))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
