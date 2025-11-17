from pathlib import Path

ROOM_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".avif"}


def get_room_images_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "static" / "images"


def list_room_images() -> list[str]:
    images_dir = get_room_images_dir()
    if not images_dir.exists():
        return []

    return sorted(
        [
            path.name
            for path in images_dir.iterdir()
            if path.is_file() and path.suffix.lower() in ROOM_IMAGE_EXTENSIONS
        ]
    )
