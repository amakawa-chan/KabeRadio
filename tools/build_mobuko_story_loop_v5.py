from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets" / "mobuko-radio"
if not ASSET_ROOT.exists():
    ASSET_ROOT = ROOT

BASE_PATH = ASSET_ROOT / "mobuko-radio-listening.png"
WRITING_EARLY_PATH = ASSET_ROOT / "mobuko-radio-writing-early-source.png"
WRITING_MID_PATH = ASSET_ROOT / "mobuko-radio-writing-mid-source.png"
WRITING_FINAL_PATH = ASSET_ROOT / "mobuko-radio-writing-source.png"
BLINK_PATH = ASSET_ROOT / "mobuko-radio-blink.png"
CHEEK_PATHS = [
    ASSET_ROOT / f"mobuko-radio-cheek-v5-{index:02d}.png"
    for index in range(1, 7)
]
GLANCE_25_PATH = ASSET_ROOT / "mobuko-radio-glance-25-source.png"
GLANCE_50_PATH = ASSET_ROOT / "mobuko-radio-glance-50-source.png"
GLANCE_75_PATH = ASSET_ROOT / "mobuko-radio-glance-75-source.png"
GLANCE_FINAL_PATH = ASSET_ROOT / "mobuko-radio-glance-smile-source.png"

OUTPUT_SIZE = (1280, 720)
FPS = 24
FRAME_DIR = ROOT / "_tmp_mobuko_story_v5"
CHEEK_WORK_DIR = ROOT / "_tmp_mobuko_cheek_v5"


def load(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    if image.size != OUTPUT_SIZE:
        image = image.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
    return image


def add_steps(
    frames: list[Image.Image], keyframes: list[Image.Image], hold: int
) -> None:
    for keyframe in keyframes:
        frames.extend(keyframe.copy() for _ in range(hold))


def write_concat_entry(handle, path: Path, duration: float | None = None) -> None:
    escaped = path.resolve().as_posix().replace("'", "'\\''")
    handle.write(f"file '{escaped}'\n")
    if duration is not None:
        handle.write(f"duration {duration:.3f}\n")


def render_smooth_cheek_frames(base: Image.Image) -> list[Image.Image]:
    """Render one slow, monotonic cheek-rest cycle with motion interpolation."""
    if CHEEK_WORK_DIR.exists():
        shutil.rmtree(CHEEK_WORK_DIR)
    key_dir = CHEEK_WORK_DIR / "keys"
    out_dir = CHEEK_WORK_DIR / "frames"
    key_dir.mkdir(parents=True)
    out_dir.mkdir()

    key_images = [base, *(load(path) for path in CHEEK_PATHS)]
    key_paths: list[Path] = []
    for index, image in enumerate(key_images):
        path = key_dir / f"key-{index:02d}.png"
        image.save(path, compress_level=1)
        key_paths.append(path)

    # Duplicate endpoints separate the still holds from the 0.4-second moves.
    # Forward and return use the exact same cels in reverse, preventing a
    # second finger-opening cycle that could read as a beckoning gesture.
    concat_path = CHEEK_WORK_DIR / "cheek-sequence.txt"
    with concat_path.open("w", encoding="utf-8", newline="\n") as handle:
        write_concat_entry(handle, key_paths[0], 1.5)
        write_concat_entry(handle, key_paths[0], 0.4)
        for path in key_paths[1:-1]:
            write_concat_entry(handle, path, 0.4)
        write_concat_entry(handle, key_paths[-1], 3.0)
        write_concat_entry(handle, key_paths[-1], 0.4)
        for path in reversed(key_paths[1:-1]):
            write_concat_entry(handle, path, 0.4)
        write_concat_entry(handle, key_paths[0], 1.5)
        write_concat_entry(handle, key_paths[0])

    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_path),
            "-vf",
            (
                f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:"
                "me_mode=bidir:vsbmc=1,format=rgb24"
            ),
            str(out_dir / "frame-%04d.png"),
        ],
        check=True,
    )
    return [load(path) for path in sorted(out_dir.glob("frame-*.png"))]


def main() -> None:
    base = load(BASE_PATH)
    writing_early = load(WRITING_EARLY_PATH)
    writing_mid = load(WRITING_MID_PATH)
    writing_final = load(WRITING_FINAL_PATH)
    blink = load(BLINK_PATH)
    glance_25 = load(GLANCE_25_PATH)
    glance_50 = load(GLANCE_50_PATH)
    glance_75 = load(GLANCE_75_PATH)
    glance_final = load(GLANCE_FINAL_PATH)
    cheek_frames = render_smooth_cheek_frames(base)

    frames: list[Image.Image] = []
    add_steps(frames, [base], hold=48)
    add_steps(
        frames,
        [
            base,
            writing_early,
            writing_mid,
            writing_final,
            writing_mid,
            writing_early,
            base,
        ],
        hold=8,
    )
    add_steps(frames, [base], hold=36)
    add_steps(frames, [base, blink, base], hold=4)
    add_steps(frames, [base], hold=36)

    # One cheek-rest readjustment per loop, with a three-second settled hold.
    frames.extend(cheek_frames)
    add_steps(frames, [base], hold=48)

    add_steps(frames, [base, glance_25, glance_50, glance_75, glance_final], hold=6)
    add_steps(frames, [glance_final], hold=48)
    add_steps(frames, [glance_final, glance_75, glance_50, glance_25, base], hold=6)
    add_steps(frames, [base], hold=72)

    if FRAME_DIR.exists():
        shutil.rmtree(FRAME_DIR)
    FRAME_DIR.mkdir()
    for index, frame in enumerate(frames):
        frame.save(FRAME_DIR / f"frame-{index:04d}.png", compress_level=1)

    print(f"created {len(frames)} frames ({len(frames) / FPS:.2f}s) in {FRAME_DIR}")
    print(f"cheek motion: {len(cheek_frames)} interpolated frames")
    print("cheek frequency: once per loop; endpoint hold: 3.0s")


if __name__ == "__main__":
    main()
