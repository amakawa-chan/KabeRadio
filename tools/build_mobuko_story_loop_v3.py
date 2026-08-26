from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFilter


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
FRAME_DIR = ROOT / "_tmp_mobuko_story_v3"


def load(path: Path, size: tuple[int, int] | None = None) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    if size and image.size != size:
        image = image.resize(size, Image.Resampling.LANCZOS)
    return image


def make_mask(
    size: tuple[int, int],
    boxes: list[tuple[int, int, int, int]],
    blur: int,
) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    for box in boxes:
        draw.ellipse(box, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(blur))


def localized_variant(
    base: Image.Image, source: Image.Image, mask: Image.Image
) -> Image.Image:
    return Image.composite(source, base, mask)


def eased_values(count: int) -> list[float]:
    if count < 2:
        return [1.0]
    return [
        0.5 - 0.5 * math.cos(math.pi * i / (count - 1))
        for i in range(count)
    ]


def add_path(
    frames: list[Image.Image],
    keyframes: list[Image.Image],
    frames_per_segment: int,
) -> None:
    for start, end in zip(keyframes, keyframes[1:]):
        for amount in eased_values(frames_per_segment):
            frames.append(Image.blend(start, end, amount))


def save_diff(image: Image.Image, name: str) -> None:
    image.convert("RGB").save(ASSET_ROOT / name, compress_level=1)


def main() -> None:
    base = load(BASE_PATH)
    writing_early_source = load(WRITING_EARLY_PATH, base.size)
    writing_mid_source = load(WRITING_MID_PATH, base.size)
    writing_final_source = load(WRITING_FINAL_PATH, base.size)
    blink_source = load(BLINK_PATH, base.size)
    cheek_stage_sources = [load(path, base.size) for path in CHEEK_STAGE_PATHS]
    cheek_target_source = load(CHEEK_TARGET_PATH, base.size)
    glance_25_source = load(GLANCE_25_PATH, base.size)
    glance_50_source = load(GLANCE_50_PATH, base.size)
    glance_75_source = load(GLANCE_75_PATH, base.size)
    glance_final_source = load(GLANCE_FINAL_PATH, base.size)

    writing_mask = make_mask(
        base.size,
        [
            (520, 625, 850, 875),
            (530, 605, 690, 805),
        ],
        blur=12,
    )
    eyes_mask = make_mask(
        base.size,
        [
            (799, 270, 884, 338),
            (898, 270, 982, 338),
        ],
        blur=7,
    )
    cheek_mask = make_mask(
        base.size,
        [
            (750, 340, 915, 525),
            (770, 385, 900, 550),
        ],
        blur=12,
    )
    smile_mask = make_mask(
        base.size,
        [
            (795, 265, 885, 340),
            (895, 265, 985, 340),
            (835, 365, 925, 430),
        ],
        blur=8,
    )

    writing_early = localized_variant(base, writing_early_source, writing_mask)
    writing_mid = localized_variant(base, writing_mid_source, writing_mask)
    writing_final = localized_variant(base, writing_final_source, writing_mask)
    blink = localized_variant(base, blink_source, eyes_mask)
    cheek_stages = [
        localized_variant(base, source, cheek_mask)
        for source in cheek_stage_sources
    ]
    cheek_target = localized_variant(base, cheek_target_source, cheek_mask)
    glance_25 = localized_variant(base, glance_25_source, eyes_mask)
    glance_50 = localized_variant(base, glance_50_source, eyes_mask)
    glance_75 = localized_variant(base, glance_75_source, smile_mask)
    glance_final = localized_variant(base, glance_final_source, smile_mask)

    save_diff(writing_early, "mobuko-radio-diff-writing-early.png")
    save_diff(writing_mid, "mobuko-radio-diff-writing-mid.png")
    save_diff(writing_final, "mobuko-radio-diff-writing.png")
    save_diff(blink, "mobuko-radio-diff-blink.png")
    for stage, image in zip((15, 30, 45, 60, 75, 90), cheek_stages):
        save_diff(image, f"mobuko-radio-diff-cheek-{stage}.png")
    save_diff(cheek_target, "mobuko-radio-diff-cheek-rest-target-v3.png")
    save_diff(glance_25, "mobuko-radio-diff-glance-25.png")
    save_diff(glance_50, "mobuko-radio-diff-glance-50.png")
    save_diff(glance_75, "mobuko-radio-diff-glance-75.png")
    save_diff(glance_final, "mobuko-radio-diff-glance-smile.png")

    FRAME_DIR.mkdir(exist_ok=True)
    for old in FRAME_DIR.glob("frame-*.png"):
        old.unlink()

    frames: list[Image.Image] = []
    frames.extend(base.copy() for _ in range(30))

    # 8 frames per keyframe segment makes the pen movement read as a stroke,
    # not a sudden hand swap.
    add_path(
        frames,
        [base, writing_early, writing_mid, writing_final,
         writing_mid, writing_early, base],
        frames_per_segment=8,
    )
    frames.extend(base.copy() for _ in range(18))

    # A slower 12-frame blink keeps the eyelids from popping.
    add_path(frames, [base, blink, base], frames_per_segment=6)
    frames.extend(base.copy() for _ in range(18))

    # Eight distinct cheek keys plus the supplied target distribute the full
    # hand/wrist movement over a long, connected path. Five frames per segment
    # keeps the 24fps motion smooth without making the pose look floaty.
    cheek_path = [base, *cheek_stages, cheek_target, *reversed(cheek_stages), base]
    add_path(frames, cheek_path, frames_per_segment=5)
    frames.extend(base.copy() for _ in range(18))

    # Four gaze keys distribute the formerly large front-facing change.
    add_path(
        frames,
        [base, glance_25, glance_50, glance_75, glance_final],
        frames_per_segment=6,
    )
    frames.extend(glance_final.copy() for _ in range(24))
    add_path(
        frames,
        [glance_final, glance_75, glance_50, glance_25, base],
        frames_per_segment=6,
    )
    frames.extend(base.copy() for _ in range(50))

    # 336 frames at 24 fps = 14 seconds. The same fixed base frame starts and
    # ends the loop; no full-screen camera motion is introduced.
    assert len(frames) == 336, len(frames)
    for index, frame in enumerate(frames):
        frame = frame.resize((1280, 720), Image.Resampling.LANCZOS)
        frame.convert("RGB").save(
            FRAME_DIR / f"frame-{index:04d}.png",
            compress_level=1,
        )

    print(f"created {len(frames)} frames in {FRAME_DIR}")
    print(f"cheek target diff: {ASSET_ROOT / 'mobuko-radio-diff-cheek-rest-target-v3.png'}")
    print(f"cheek stages: {len(cheek_stages)} intermediate keys")


if __name__ == "__main__":
    main()
