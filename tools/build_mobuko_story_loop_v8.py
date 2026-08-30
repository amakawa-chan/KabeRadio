from pathlib import Path
import shutil

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets" / "mobuko-radio"
if not ASSET_ROOT.exists():
    ASSET_ROOT = ROOT

BASE_PATH = ASSET_ROOT / "mobuko-radio-listening.png"
WRITING_PATHS = [
    ASSET_ROOT / "mobuko-radio-writing-early-source.png",
    ASSET_ROOT / "mobuko-radio-writing-mid-source.png",
    ASSET_ROOT / "mobuko-radio-writing-source.png",
]
BLINK_PATH = ASSET_ROOT / "mobuko-radio-blink.png"
CHEEK_PATHS = [
    ASSET_ROOT / "mobuko-radio-cheek-v5-01.png",
    ASSET_ROOT / "mobuko-radio-cheek-v5-03.png",
    ASSET_ROOT / "mobuko-radio-cheek-v5-05.png",
    ASSET_ROOT / "mobuko-radio-cheek-v5-06.png",
]
DRINK_PATHS = [
    ASSET_ROOT / f"mobuko-radio-drink-v8-{index:02d}.png"
    for index in range(1, 5)
]
STRETCH_PATHS = [
    ASSET_ROOT / f"mobuko-radio-stretch-v7-{index:02d}.png"
    for index in range(1, 4)
]
GLANCE_PATHS = [
    ASSET_ROOT / "mobuko-radio-glance-25-source.png",
    ASSET_ROOT / "mobuko-radio-glance-50-source.png",
    ASSET_ROOT / "mobuko-radio-glance-75-source.png",
    ASSET_ROOT / "mobuko-radio-glance-smile-source.png",
]

OUTPUT_SIZE = (1280, 720)
FPS = 24
FRAME_DIR = ROOT / "_tmp_mobuko_story_v8"
DRINK_FRAME_DIR = ROOT / "_tmp_mobuko_drink_v8"
STRETCH_FRAME_DIR = ROOT / "_tmp_mobuko_stretch_v8"


def load(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    if image.size != OUTPUT_SIZE:
        image = image.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
    return image


def add_cels(
    frames: list[Image.Image], keyframes: list[Image.Image], hold: int
) -> None:
    for keyframe in keyframes:
        frames.extend(keyframe.copy() for _ in range(hold))


def write_frames(frames: list[Image.Image], directory: Path) -> None:
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir()
    for index, frame in enumerate(frames):
        frame.save(directory / f"frame-{index:04d}.png", compress_level=1)


def add_reversible_action(
    frames: list[Image.Image],
    base: Image.Image,
    action: list[Image.Image],
    transition_hold: int,
    pose_hold: int,
) -> None:
    add_cels(frames, [base, *action], hold=transition_hold)
    add_cels(frames, [action[-1]], hold=pose_hold)
    add_cels(frames, [*reversed(action[:-1]), base], hold=transition_hold)


def action_preview(
    base: Image.Image,
    action: list[Image.Image],
    transition_hold: int,
    pose_hold: int,
) -> list[Image.Image]:
    frames: list[Image.Image] = []
    add_cels(frames, [base], hold=24)
    add_reversible_action(frames, base, action, transition_hold, pose_hold)
    add_cels(frames, [base], hold=24)
    return frames


def main() -> None:
    base = load(BASE_PATH)
    writing_early, writing_mid, writing_final = [load(path) for path in WRITING_PATHS]
    blink = load(BLINK_PATH)
    cheek = [load(path) for path in CHEEK_PATHS]
    drink = [load(path) for path in DRINK_PATHS]
    stretch = [load(path) for path in STRETCH_PATHS]
    glance_25, glance_50, glance_75, glance_final = [
        load(path) for path in GLANCE_PATHS
    ]

    frames: list[Image.Image] = []
    add_cels(frames, [base], hold=72)
    add_cels(
        frames,
        [base, writing_early, writing_mid, writing_final,
         writing_mid, writing_early, base],
        hold=5,
    )
    add_cels(frames, [base], hold=72)
    add_cels(frames, [base, blink, base], hold=3)
    add_cels(frames, [base], hold=96)

    # Longer drink: compact mug, 2.5-second approach and 2.5-second sip.
    add_reversible_action(frames, base, drink, transition_hold=12, pose_hold=60)
    add_cels(frames, [base], hold=120)

    add_reversible_action(frames, base, cheek, transition_hold=8, pose_hold=72)
    add_cels(frames, [base], hold=120)

    # Longer stretch: slower lift and a three-second overhead hold.
    add_reversible_action(frames, base, stretch, transition_hold=14, pose_hold=72)
    add_cels(frames, [base], hold=120)

    add_cels(
        frames,
        [base, glance_25, glance_50, glance_75, glance_final],
        hold=5,
    )
    add_cels(frames, [glance_final], hold=48)
    add_cels(frames, [glance_75, glance_50, glance_25, base], hold=5)

    # 60 seconds total; the long final rest keeps the loop unobtrusive.
    add_cels(frames, [base], hold=221)
    assert len(frames) == 1440, len(frames)
    write_frames(frames, FRAME_DIR)

    drink_preview = action_preview(base, drink, transition_hold=12, pose_hold=60)
    stretch_preview = action_preview(base, stretch, transition_hold=14, pose_hold=72)
    write_frames(drink_preview, DRINK_FRAME_DIR)
    write_frames(stretch_preview, STRETCH_FRAME_DIR)

    print(f"created {len(frames)} frames ({len(frames) / FPS:.2f}s)")
    print(f"drink preview: {len(drink_preview)} frames")
    print(f"stretch preview: {len(stretch_preview)} frames")
    print("mode: held full-frame cels; no interpolation; no crossfade")


if __name__ == "__main__":
    main()
