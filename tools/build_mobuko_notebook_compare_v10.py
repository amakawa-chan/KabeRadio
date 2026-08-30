#!/usr/bin/env python3
"""Build the downward-gaze notebook C variant and A/B/C comparison."""

from __future__ import annotations

import subprocess
from pathlib import Path

from build_mobuko_story_loop_v9 import ROOT, encode, hold, load


def build_c_variant() -> Path:
    base = load("mobuko-radio-listening.png")
    original_first = load("mobuko-radio-notebook-v9-01.png")
    down = [load(f"mobuko-radio-notebook-v10-down-{i:02d}.png") for i in range(1, 6)]
    blink = load("mobuko-radio-notebook-v10-down-blink.png")

    frames = []
    hold(frames, base, 48)
    hold(frames, original_first, 8)
    hold(frames, down[0], 16)
    hold(frames, down[1], 18)
    hold(frames, blink, 2)
    hold(frames, down[1], 16)
    hold(frames, down[2], 20)
    hold(frames, down[3], 20)
    hold(frames, down[4], 96)
    hold(frames, base, 48)
    assert len(frames) == 292, len(frames)
    return encode("mobuko-radio-notebook-v10-down", frames)


def build_comparison(c_variant: Path) -> Path:
    inputs = [
        ROOT / "mobuko-radio-notebook-v9.mp4",
        ROOT / "mobuko-radio-notebook-v9-blink.mp4",
        c_variant,
    ]
    output = ROOT / "mobuko-radio-notebook-v10-abc-comparison.mp4"
    filters = (
        "[0:v]scale=640:360[a];"
        "[1:v]scale=640:360[b];"
        "[2:v]scale=640:360[c];"
        "[a][b][c]hstack=inputs=3[v]"
    )
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(inputs[0]), "-i", str(inputs[1]), "-i", str(inputs[2]),
            "-filter_complex", filters, "-map", "[v]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output),
        ],
        check=True,
    )
    return output


def main() -> None:
    c_variant = build_c_variant()
    comparison = build_comparison(c_variant)
    print(f"C variant: {c_variant.name}")
    print(f"A/B/C comparison: {comparison.name}")
    print("comparison order: left=A original, center=B blink, right=C downward gaze + blink")


if __name__ == "__main__":
    main()
