#!/usr/bin/env python3
"""Build blink-added B variants and synchronized A/B comparison clips."""

from __future__ import annotations

import subprocess
from pathlib import Path

from build_mobuko_story_loop_v9 import ROOT, encode, hold, load


def compare(action: str) -> Path:
    original = ROOT / f"mobuko-radio-{action}-v9.mp4"
    blink = ROOT / f"mobuko-radio-{action}-v9-blink.mp4"
    output = ROOT / f"mobuko-radio-{action}-v9-comparison.mp4"
    filters = "[0:v]scale=640:360[a];[1:v]scale=640:360[b];[a][b]hstack=inputs=2[v]"
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(original), "-i", str(blink),
            "-filter_complex", filters, "-map", "[v]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output),
        ],
        check=True,
    )
    return output


def main() -> None:
    base = load("mobuko-radio-listening.png")

    notebook = [load(f"mobuko-radio-notebook-v9-{i:02d}.png") for i in range(1, 6)]
    notebook_blink = load("mobuko-radio-notebook-v9-blink.png")
    notebook_frames = []
    for cel, frames in [(base, 48), (notebook[0], 24), (notebook[1], 18)]:
        hold(notebook_frames, cel, frames)
    hold(notebook_frames, notebook_blink, 2)
    for cel, frames in [
        (notebook[1], 16), (notebook[2], 20), (notebook[3], 20),
        (notebook[4], 96), (base, 48),
    ]:
        hold(notebook_frames, cel, frames)

    window = [load(f"mobuko-radio-window-v9-{i:02d}.png") for i in range(1, 3)]
    window_blink = load("mobuko-radio-window-v9-blink.png")
    window_frames = []
    for cel, frames in [(base, 48), (window[0], 20), (window[1], 58)]:
        hold(window_frames, cel, frames)
    hold(window_frames, window_blink, 2)
    for cel, frames in [(window[1], 60), (window[0], 20), (base, 48)]:
        hold(window_frames, cel, frames)

    headband = [load(f"mobuko-radio-headband-v9-{i:02d}.png") for i in range(1, 4)]
    headband_blink = load("mobuko-radio-headband-v9-blink.png")
    headband_frames = []
    for cel, frames in [(base, 48), (headband[0], 20), (headband[1], 28), (headband[2], 34)]:
        hold(headband_frames, cel, frames)
    hold(headband_frames, headband_blink, 2)
    for cel, frames in [(headband[2], 36), (base, 48)]:
        hold(headband_frames, cel, frames)

    clips = {
        "notebook": notebook_frames,
        "window": window_frames,
        "headband": headband_frames,
    }
    expected = {"notebook": 292, "window": 256, "headband": 216}
    for action, frames in clips.items():
        assert len(frames) == expected[action], (action, len(frames))
        encode(f"mobuko-radio-{action}-v9-blink", frames)
        comparison = compare(action)
        print(f"comparison: {comparison.name}")


if __name__ == "__main__":
    main()
