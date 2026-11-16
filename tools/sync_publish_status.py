#!/usr/bin/env python3
"""Sync episodes/*/production.json publish flags from publication.json.

publication.json (written by the upload pipeline) is the source of truth for
publication state. production.json is created with publish=false/false as
initial values and must be synced after an episode is actually published.

Rules (conservative, evidence-based):
- youtube -> true only when publication.json youtube.actualPrivacy is
  "public", or "private" with a publishAt in the past.
- spotify -> true only when publication.json spotify.status is "published".
- Flags are only ever flipped false -> true. A production flag that is true
  while publication.json does not prove publication is reported as a
  warning and left untouched for a human to check.
- Episodes without publication.json (or without the relevant section) are
  left untouched.

Usage:
    python3 tools/sync_publish_status.py [--dry-run]
"""

import datetime
import json
import os
import re
import sys

EPISODES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "episodes")


def youtube_is_public(pub: dict, now: datetime.datetime) -> bool | None:
    yt = pub.get("youtube")
    if not yt:
        return None
    if yt.get("actualPrivacy") == "public":
        return True
    if yt.get("actualPrivacy") == "private" and yt.get("publishAt"):
        return datetime.datetime.fromisoformat(yt["publishAt"]) <= now
    return False


def spotify_is_published(pub: dict) -> bool | None:
    sp = pub.get("spotify")
    if not sp:
        return None
    return sp.get("status") == "published"


def flip_flag(text: str, key: str) -> str:
    """Flip `"key": false` to `"key": true` inside the publish block only."""
    pattern = re.compile(r'("publish"\s*:\s*\{[^}]*?"' + key + r'"\s*:\s*)false', re.DOTALL)
    new_text, n = pattern.subn(r"\g<1>true", text, count=1)
    if n != 1:
        raise ValueError(f"could not locate publish.{key}=false exactly once")
    return new_text


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    now = datetime.datetime.now(datetime.timezone.utc)
    changed, warnings = [], []

    for name in sorted(os.listdir(EPISODES_DIR)):
        folder = os.path.join(EPISODES_DIR, name)
        prod_path = os.path.join(folder, "production.json")
        pub_path = os.path.join(folder, "publication.json")
        if not os.path.isdir(folder) or not os.path.exists(prod_path):
            continue
        if not os.path.exists(pub_path):
            continue
        with open(prod_path, encoding="utf-8") as f:
            prod_text = f.read()
        prod = json.loads(prod_path and prod_text)
        with open(pub_path, encoding="utf-8") as f:
            pub = json.load(f)

        publish = prod.get("publish", {})
        yt = youtube_is_public(pub, now)
        sp = spotify_is_published(pub)

        new_text = prod_text
        flips = []
        for key, truth in (("youtube", yt), ("spotify", sp)):
            if truth is True and publish.get(key) is not True:
                new_text = flip_flag(new_text, key)
                flips.append(key)
            elif truth is False and publish.get(key) is True:
                warnings.append(f"{name}: production publish.{key}=true but publication.json does not show it published (left unchanged)")

        if flips:
            changed.append((name, flips))
            if not dry_run:
                with open(prod_path, "w", encoding="utf-8") as f:
                    f.write(new_text)

    for name, flips in changed:
        print(f"{'WOULD CHANGE' if dry_run else 'CHANGED'}: {name} ({', '.join(flips)}: false -> true)")
    for w in warnings:
        print(f"WARNING: {w}")
    print(f"done: {len(changed)} file(s) {'to change' if dry_run else 'changed'}, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
