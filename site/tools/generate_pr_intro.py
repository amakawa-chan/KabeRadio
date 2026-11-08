"""Generate a local station intro from the episode's pronunciation script."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path


def read_text(path):
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8-sig").strip() or None


def read_pair(episode):
    display = read_text(episode / "pr.txt")
    speech = read_text(episode / "pr-speech.txt")
    return display, speech


def fingerprint(display, speech, audio):
    payload = [display, speech, hashlib.sha256(audio).hexdigest()]
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode("utf-8")).hexdigest()


def paired_intro_is_current(intro, display, speech):
    if not (display and speech and intro.is_file()):
        return False
    marker = intro.with_suffix(".sha256")
    return read_text(marker) == fingerprint(display, speech, intro.read_bytes())


def atomic_write(path, data):
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temp = Path(handle.name)
    try:
        temp.write_bytes(data)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def generate(root, key, base_url, style):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", key) or ".." in key or key == "welcome":
        raise ValueError("Invalid episode key")
    display, speech = read_pair(root / "episodes" / key)
    if not (display and speech):
        raise ValueError("Nonempty pr.txt and pr-speech.txt are required")

    def post(path, data):
        request = urllib.request.Request(
            base_url.rstrip("/") + path, data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=180) as response:
            return response.read()

    query = post("/audio_query?" + urllib.parse.urlencode({"text": speech, "speaker": style}), b"")
    wav = post("/synthesis?" + urllib.parse.urlencode({"speaker": style}), query)
    result = subprocess.run(
        ["ffmpeg", "-v", "error", "-nostdin", "-i", "pipe:0", "-af",
         "loudnorm=I=-18:TP=-2:LRA=11", "-ar", "44100", "-ac", "1",
         "-b:a", "80k", "-f", "mp3", "pipe:1"],
        input=wav, stdout=subprocess.PIPE, check=True,
    )
    if not result.stdout:
        raise RuntimeError("FFmpeg produced no audio")
    intro = root / "site" / "intros" / f"{key}.mp3"
    intro.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(intro, result.stdout)
    atomic_write(intro.with_suffix(".sha256"), fingerprint(display, speech, result.stdout).encode("ascii"))
    return intro


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--base-url", default="http://127.0.0.1:10101")
    parser.add_argument("--style", type=int, default=888753761)
    args = parser.parse_args()
    print(generate(args.root, args.episode, args.base_url, args.style))
