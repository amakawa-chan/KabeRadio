from pathlib import Path
import shutil

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

# Use only the most legible cheek-rest silhouettes. The omitted cels added
# background/face variation without contributing enough visible hand travel.
CHEEK_PATHS = [
    ASSET_ROOT / "mobuko-radio-cheek-v5-01.png",
    ASSET_ROOT / "mobuko-radio-cheek-v5-03.png",
    ASSET_ROOT / "mobuko-radio-cheek-v5-05.png",
    ASSET_ROOT / "mobuko-radio-cheek-v5-06.png",
]

GLANCE_25_PATH = ASSET_ROOT / "mobuko-radio-glance-25-source.png"
GLANCE_50_PATH = ASSET_ROOT / "mobuko-radio-glance-50-source.png"
GLANCE_75_PATH = ASSET_ROOT / "mobuko-radio-glance-75-source.png"
GLANCE_FINAL_PATH = ASSET_ROOT / "mobuko-radio-glance-smile-source.png"

OUTPUT_SIZE = (1280, 720)
FPS = 24
FRAME_DIR = ROOT / "_tmp_mobuko_story_v6"
CHEEK_FRAME_DIR = ROOT / "_tmp_mobuko_cheek_v6"


def load(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    if image.size != OUTPUT_SIZE:
        image = image.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
    return image


def add_cels(
    frames: list[Image.Image], keyframes: list[Image.Image], hold: int
) -> None:
    """Append complete full-frame cels; never blend adjacent images."""
    for keyframe in keyframes:
        frames.extend(keyframe.copy() for _ in range(hold))


def write_frames(frames: list[Image.Image], directory: Path) -> None:
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir()
    for index, frame in enumerate(frames):
        frame.save(directory / f"frame-{index:04d}.png", compress_level=1)


def main() -> None:
    base = load(BASE_PATH)
    writing_early = load(WRITING_EARLY_PATH)
    writing_mid = load(WRITING_MID_PATH)
    writing_final = load(WRITING_FINAL_PATH)
    blink = load(BLINK_PATH)
    cheek = [load(path) for path in CHEEK_PATHS]
    glance_25 = load(GLANCE_25_PATH)
    glance_50 = load(GLANCE_50_PATH)
    glance_75 = load(GLANCE_75_PATH)
    glance_final = load(GLANCE_FINAL_PATH)

    frames: list[Image.Image] = []

    # Long rests keep every gesture from feeling mechanically repetitive.
    add_cels(frames, [base], hold=96)

    # Limited-animation writing: six image changes per second.
    add_cels(
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
        hold=5,
    )
    add_cels(frames, [base], hold=72)

    # A blink remains deliberately snappy.
    add_cels(frames, [base, blink, base], hold=3)
    add_cels(frames, [base], hold=72)

    # One cheek-rest change: four clean silhouettes, no optical flow and no
    # crossfade. The same cels return in exact reverse order.
    cheek_forward = [base, *cheek]
    cheek_return = [*reversed(cheek[:-1]), base]
    add_cels(frames, cheek_forward, hold=8)
    add_cels(frames, [cheek[-1]], hold=72)
    add_cels(frames, cheek_return, hold=8)
    add_cels(frames, [base], hold=96)

    # Gaze also uses held full-frame cels to match the same animation style.
    add_cels(
        frames,
        [base, glance_25, glance_50, glance_75, glance_final],
        hold=5,
    )
    add_cels(frames, [glance_final], hold=48)
    add_cels(
        frames,
        [glance_75, glance_50, glance_25, base],
        hold=5,
    )

    # Exactly 30 seconds. First and last frames are identical.
    add_cels(frames, [base], hold=103)
    assert len(frames) == 720, len(frames)
    write_frames(frames, FRAME_DIR)

    cheek_preview: list[Image.Image] = []
    add_cels(cheek_preview, [base], hold=24)
    add_cels(cheek_preview, cheek_forward, hold=8)
    add_cels(cheek_preview, [cheek[-1]], hold=72)
    add_cels(cheek_preview, cheek_return, hold=8)
    add_cels(cheek_preview, [base], hold=24)
    write_frames(cheek_preview, CHEEK_FRAME_DIR)

    print(f"created {len(frames)} frames ({len(frames) / FPS:.2f}s)")
    print(f"cheek preview: {len(cheek_preview)} frames")
    print("mode: held full-frame cels; no interpolation; no crossfade")


if __name__ == "__main__":
    main()
