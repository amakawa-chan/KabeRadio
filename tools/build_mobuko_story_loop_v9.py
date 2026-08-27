#!/usr/bin/env python3
"""Build Mobuko's v9 limited-animation story clips from full-frame cels."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOTS = [ROOT / "assets" / "mobuko-radio", ROOT]
OUT = ROOT
FPS = 24
SIZE = (1280, 720)


def asset(name: str) -> Path:
    for root in ASSET_ROOTS:
        path = root / name
        if path.exists():
            return path
    raise FileNotFoundError(name)


def load(name: str) -> Image.Image:
    with Image.open(asset(name)) as image:
        return image.convert("RGB").resize(SIZE, Image.Resampling.LANCZOS)


def hold(sequence: list[Image.Image], image: Image.Image, frames: int) -> None:
    sequence.extend([image] * frames)


def reversible(
    base: Image.Image,
    transitions: list[Image.Image],
    pose: Image.Image,
    transition_hold: int,
    pose_hold: int,
) -> list[Image.Image]:
    sequence: list[Image.Image] = []
    for cel in [base, *transitions]:
        hold(sequence, cel, transition_hold)
    hold(sequence, pose, pose_hold)
    for cel in [*reversed(transitions[:-1]), base]:
        hold(sequence, cel, transition_hold)
    return sequence


def encode(name: str, frames: list[Image.Image]) -> Path:
    frame_dir = OUT / f"_tmp_{name}"
    if frame_dir.exists():
        shutil.rmtree(frame_dir)
    frame_dir.mkdir(parents=True)
    for index, frame in enumerate(frames):
        frame.save(frame_dir / f"frame_{index:05d}.png", compress_level=1)

    output = OUT / f"{name}.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", str(frame_dir / "frame_%05d.png"),
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output),
        ],
        check=True,
    )
    shutil.rmtree(frame_dir)
    print(f"{output.name}: {len(frames) / FPS:.2f}s ({len(frames)} frames)")
    return output


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    base = load("mobuko-radio-listening.png")
    notebook = [load(f"mobuko-radio-notebook-v9-{i:02d}.png") for i in range(1, 6)]
    yawn = [load(f"mobuko-radio-yawn-v9-{i:02d}.png") for i in range(1, 3)]
    headphones = [load(f"mobuko-radio-headphones-v9-{i:02d}.png") for i in range(1, 6)]
    window = [load(f"mobuko-radio-window-v9-{i:02d}.png") for i in range(1, 3)]
    headband = [load(f"mobuko-radio-headband-v9-{i:02d}.png") for i in range(1, 4)]

    notebook_action: list[Image.Image] = []
    for cel, frames in zip(
        [base, *notebook, base], [48, 24, 36, 20, 20, 96, 48], strict=True
    ):
        hold(notebook_action, cel, frames)

    yawn_action: list[Image.Image] = []
    for cel, frames in zip(
        [base, yawn[0], yawn[1], yawn[0], base], [48, 24, 72, 24, 48], strict=True
    ):
        hold(yawn_action, cel, frames)

    headphones_action: list[Image.Image] = []
    for cel, frames in zip(
        [base, headphones[0], headphones[1], headphones[2]], [48, 16, 20, 24], strict=True
    ):
        hold(headphones_action, cel, frames)
    for _ in range(2):
        for cel in [headphones[3], headphones[2], headphones[4], headphones[2]]:
            hold(headphones_action, cel, 24)
    for cel, frames in zip(
        [headphones[1], headphones[0], base], [20, 16, 48], strict=True
    ):
        hold(headphones_action, cel, frames)

    window_action: list[Image.Image] = []
    for cel, frames in zip(
        [base, window[0], window[1], window[0], base], [48, 20, 120, 20, 48], strict=True
    ):
        hold(window_action, cel, frames)

    headband_action: list[Image.Image] = []
    for cel, frames in zip(
        [base, headband[0], headband[1], headband[2], base], [48, 20, 28, 72, 48], strict=True
    ):
        hold(headband_action, cel, frames)

    drink = [load(f"mobuko-radio-drink-v8-{i:02d}.png") for i in range(1, 5)]
    stretch = [load(f"mobuko-radio-stretch-v7-{i:02d}.png") for i in range(1, 4)]
    cheek = [load(f"mobuko-radio-cheek-v5-{i:02d}.png") for i in [1, 3, 5, 6]]
    glance = [
        load("mobuko-radio-glance-25-source.png"),
        load("mobuko-radio-glance-50-source.png"),
        load("mobuko-radio-glance-75-source.png"),
        load("mobuko-radio-glance-smile-source.png"),
    ]

    drink_action = reversible(base, drink, drink[-1], 12, 60)
    stretch_action = reversible(base, stretch, stretch[-1], 14, 72)
    cheek_action = reversible(base, cheek, cheek[-1], 8, 72)
    glance_action = reversible(base, glance, glance[-1], 5, 48)

    clips = {
        "mobuko-radio-notebook-v9": notebook_action,
        "mobuko-radio-yawn-v9": yawn_action,
        "mobuko-radio-headphones-v9": headphones_action,
        "mobuko-radio-window-v9": window_action,
        "mobuko-radio-headband-v9": headband_action,
    }
    for name, frames in clips.items():
        encode(name, frames)

    story: list[Image.Image] = []
    actions = [
        notebook_action,
        yawn_action,
        drink_action,
        headphones_action,
        window_action,
        headband_action,
        stretch_action,
        cheek_action,
        glance_action,
    ]
    for action in actions:
        hold(story, base, 184)
        story.extend(action)
    hold(story, base, 5)
    assert len(story) == 3600, len(story)
    encode("mobuko-radio-story-loop-v9", story)


if __name__ == "__main__":
    main()
