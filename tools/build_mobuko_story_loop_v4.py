from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets" / "mobuko-radio"
if not ASSET_ROOT.exists():
    # Keep the script runnable in the original local workspace layout too.
    ASSET_ROOT = ROOT

BASE_PATH = ASSET_ROOT / "mobuko-radio-listening.png"
WRITING_EARLY_PATH = ASSET_ROOT / "mobuko-radio-writing-early-source.png"
WRITING_MID_PATH = ASSET_ROOT / "mobuko-radio-writing-mid-source.png"
WRITING_FINAL_PATH = ASSET_ROOT / "mobuko-radio-writing-source.png"
BLINK_PATH = ASSET_ROOT / "mobuko-radio-blink.png"
CHEEK_STAGE_PATHS = [
    ASSET_ROOT / "mobuko-radio-cheek-15-source.png",
    ASSET_ROOT / "mobuko-radio-cheek-30-source.png",
    ASSET_ROOT / "mobuko-radio-cheek-45-source.png",
    ASSET_ROOT / "mobuko-radio-cheek-60-source.png",
    ASSET_ROOT / "mobuko-radio-cheek-75-source.png",
    ASSET_ROOT / "mobuko-radio-cheek-90-source.png",
]
CHEEK_TARGET_PATH = ASSET_ROOT / "mobuko-radio-cheek-rest-target-v3.png"
GLANCE_25_PATH = ASSET_ROOT / "mobuko-radio-glance-25-source.png"
GLANCE_50_PATH = ASSET_ROOT / "mobuko-radio-glance-50-source.png"
GLANCE_75_PATH = ASSET_ROOT / "mobuko-radio-glance-75-source.png"
GLANCE_FINAL_PATH = ASSET_ROOT / "mobuko-radio-glance-smile-source.png"
FRAME_DIR = ROOT / "_tmp_mobuko_story_v4"
OUTPUT_SIZE = (1280, 720)


def load(path: Path, size: tuple[int, int] | None = None) -> Image.Image:
    image = Image.open(path).convert("RGB")
    if size and image.size != size:
        image = image.resize(size, Image.Resampling.LANCZOS)
    return image


def add_steps(
    frames: list[Image.Image],
    keyframes: list[Image.Image],
    hold: int,
) -> None:
    """Append complete, clean frames without local compositing or blending."""
    for keyframe in keyframes:
        frames.extend(keyframe.copy() for _ in range(hold))


def main() -> None:
    base = load(BASE_PATH)
    writing_early = load(WRITING_EARLY_PATH, base.size)
    writing_mid = load(WRITING_MID_PATH, base.size)
    writing_final = load(WRITING_FINAL_PATH, base.size)
    blink = load(BLINK_PATH, base.size)
    cheek_stages = [load(path, base.size) for path in CHEEK_STAGE_PATHS]
    cheek_target = load(CHEEK_TARGET_PATH, base.size)
    glance_25 = load(GLANCE_25_PATH, base.size)
    glance_50 = load(GLANCE_50_PATH, base.size)
    glance_75 = load(GLANCE_75_PATH, base.size)
    glance_final = load(GLANCE_FINAL_PATH, base.size)

    frames: list[Image.Image] = []

    # 30 frames idle.
    add_steps(frames, [base], hold=30)
    # Writing uses complete source images as stepped animation cels.
    add_steps(
        frames,
        [base, writing_early, writing_mid, writing_final,
         writing_mid, writing_early, base],
        hold=6,
    )
    add_steps(frames, [base], hold=18)
    # Blink is also a clean two-cel cut, with no eye-only overlay.
    add_steps(frames, [base, blink, base], hold=6)
    add_steps(frames, [base], hold=18)

    # The supplied cheek-rest image is the exact endpoint. All six generated
    # intermediate images are full-frame cels; no mask or crossfade is used.
    cheek_path = [base, *cheek_stages, cheek_target, *reversed(cheek_stages), base]
    add_steps(frames, cheek_path, hold=4)
    add_steps(frames, [base], hold=18)

    # Gaze and smile remain complete full-frame cels as well.
    add_steps(frames, [base, glance_25, glance_50, glance_75, glance_final], hold=4)
    add_steps(frames, [glance_final], hold=24)
    add_steps(frames, [glance_final, glance_75, glance_50, glance_25, base], hold=4)
    add_steps(frames, [base], hold=68)

    # 336 frames at 24 fps = 14 seconds. Start and end are the same full frame.
    assert len(frames) == 336, len(frames)
    FRAME_DIR.mkdir(exist_ok=True)
    for old in FRAME_DIR.glob("frame-*.png"):
        old.unlink()
    for index, frame in enumerate(frames):
        if frame.size != OUTPUT_SIZE:
            frame = frame.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
        frame.save(FRAME_DIR / f"frame-{index:04d}.png", compress_level=1)

    print(f"created {len(frames)} complete frames in {FRAME_DIR}")
    print("mode: full-frame stepped cels; no local compositing; no crossfade")


if __name__ == "__main__":
    main()
