#!/usr/bin/env python3
"""「モブ子の放送局」エピソード索引の再生成スクリプト。

episodes/<key>/ の publication.json / README.md / script.md と notes/<key>/、
site/intros/<key>.mp3 の有無から site/episode-index.json と
site/episode-index.js を作り直す。

掲載ゲート（仕様どおり）:
  - publication.json の youtube.actualPrivacy が "public"、または
    "private" かつ publishAt が現在時刻以前（予約公開済み）
  - かつ YouTube oEmbed が 200 を返す（実際に公開到達可能）
pr.txt は表示・共有用の prText として掲載する。新形式の introAudio は PR文、読み上げ版、MP3 が生成時の記録と一致するとき設定する。

使い方: python3 site/tools/build_episode_index.py [--root <repo root>]
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from generate_pr_intro import paired_intro_is_current, read_pair

SITE_BASE = "https://amakawa-chan.github.io/KabeRadio"


def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def extract_title(readme_path):
    if not readme_path.exists():
        return None
    for line in readme_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def extract_description(script_path):
    """## Episode Description セクションの原文（プレーンテキスト）。無ければ None。"""
    if not script_path.exists():
        return None
    text = script_path.read_text(encoding="utf-8")
    m = re.search(r"^## Episode Description\s*$", text, re.M)
    if not m:
        return None
    rest = text[m.end():]
    end = re.search(r"^## ", rest, re.M)
    section = rest[: end.start()] if end else rest
    lines = section.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    description = "\n".join(line.rstrip() for line in lines).strip()
    return description or None


def oembed_public(youtube_url):
    """Return (availability, YouTube title); keep candidates on network failure."""
    api = "https://www.youtube.com/oembed?url=" + urllib.parse.quote(
        youtube_url, safe=""
    ) + "&format=json"
    req = urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            if res.status != 200:
                return False, None
            try:
                title = json.load(res).get("title")
            except (ValueError, AttributeError):
                title = None
            return True, title
    except urllib.error.HTTPError as e:
        if e.code in (400, 401, 403, 404):
            return False, None
        return None, None
    except Exception:
        return None, None


def episode_number(youtube_title, spotify_number):
    match = re.match(r"^\s*【壁ラジ】\s*[#＃]([0-9]{1,9})(?![0-9])", youtube_title or "")
    if match and int(match[1]) > 0:
        return int(match[1])
    if re.fullmatch(r"[0-9]{1,9}", str(spotify_number)) and int(spotify_number) > 0:
        return int(spotify_number)
    return None


def build(root):
    episodes_dir = root / "episodes"
    notes_dir = root / "notes"
    intros_dir = root / "site" / "intros"
    now = datetime.now(timezone.utc)
    entries, skipped = [], []

    for ep_dir in sorted(episodes_dir.iterdir()):
        if not ep_dir.is_dir():
            continue
        pub_path = ep_dir / "publication.json"
        if not pub_path.exists():
            continue
        try:
            pub = json.loads(pub_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            skipped.append((ep_dir.name, "publication.json parse error"))
            continue
        yt = pub.get("youtube") or {}
        video_id = yt.get("videoId")
        if not video_id:
            continue
        youtube_url = yt.get("url") or f"https://www.youtube.com/watch?v={video_id}"
        published_raw = yt.get("publishAt") or yt.get("uploadedAt")
        published_dt = parse_dt(published_raw)
        publish_at_dt = parse_dt(yt.get("publishAt"))

        privacy = yt.get("actualPrivacy")
        candidate = privacy == "public" or (
            privacy == "private" and publish_at_dt is not None and publish_at_dt <= now
        )
        if not candidate:
            # 記録上は非公開でも、実際には公開されている取りこぼしを検出して知らせる
            if oembed_public(youtube_url)[0] is True:
                print(
                    f"warning: RECORD MISMATCH {ep_dir.name}: publication.json says "
                    f"actualPrivacy={privacy} but the video is publicly reachable. "
                    "Fix publication.json to list it.",
                    file=sys.stderr,
                )
            skipped.append((ep_dir.name, f"not public (actualPrivacy={privacy})"))
            continue
        verdict, youtube_title = oembed_public(youtube_url)
        if verdict is False:
            skipped.append((ep_dir.name, "oEmbed: not reachable as public"))
            continue
        if verdict is None:
            print(f"warning: oEmbed check inconclusive for {ep_dir.name}; kept",
                  file=sys.stderr)

        sp = pub.get("spotify") or {}
        ep_num = episode_number(youtube_title or yt.get("title"), sp.get("episodeNumber"))

        display, speech = read_pair(ep_dir)
        intro = intros_dir / f"{ep_dir.name}.mp3"
        has_pair_files = (ep_dir / "pr.txt").exists() or (ep_dir / "pr-speech.txt").exists()
        if has_pair_files:
            has_intro = paired_intro_is_current(intro, display, speech)
        else:
            has_intro = intro.exists() and not intro.with_suffix(".sha256").exists()
        if ep_num is None or not has_intro:
            missing = ", ".join(name for name, absent in (
                ("episode number", ep_num is None), ("intro audio", not has_intro)
            ) if absent)
            print(f"warning: station incomplete {ep_dir.name}: {missing}", file=sys.stderr)
        entries.append(
            {
                "schemaVersion": 1,
                "episodeKey": ep_dir.name,
                "episodeNumber": ep_num,
                "title": extract_title(ep_dir / "README.md"),
                "description": extract_description(ep_dir / "script.md"),
                "prText": display,
                "introAudio": f"intros/{ep_dir.name}.mp3" if has_intro else None,
                "youtubeUrl": youtube_url,
                "spotifyUrl": sp.get("episodeUrl"),
                "noteUrl": (
                    f"{SITE_BASE}/notes/{ep_dir.name}/"
                    if (notes_dir / ep_dir.name).is_dir()
                    else None
                ),
                "publishedAt": published_raw,
                "_sort": published_dt or datetime.min.replace(tzinfo=timezone.utc),
            }
        )

    entries.sort(key=lambda e: e["_sort"], reverse=True)
    for e in entries:
        del e["_sort"]
    return entries, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="repo root (default: script's ../..)")
    args = ap.parse_args()
    root = Path(args.root) if args.root else Path(__file__).resolve().parents[2]

    entries, skipped = build(root)
    payload = json.dumps(entries, ensure_ascii=False, indent=1)
    (root / "site" / "episode-index.json").write_text(payload + "\n", encoding="utf-8")
    (root / "site" / "episode-index.js").write_text(
        "window.EPISODE_INDEX = " + payload + ";\n", encoding="utf-8"
    )
    print(f"listed: {len(entries)}")
    for key, reason in skipped:
        print(f"skipped: {key} ({reason})")


if __name__ == "__main__":
    main()
