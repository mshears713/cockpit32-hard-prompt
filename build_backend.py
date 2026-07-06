from __future__ import annotations

import base64
import csv
import hashlib
import io
import os
import zipfile
from pathlib import Path

NAME = "cockpit32"
VERSION = "0.1.0"
DIST = f"{NAME}-{VERSION}.dist-info"


def _wheel_bytes() -> bytes:
    rows: list[tuple[str, str, str]] = []
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as wheel:
        def write(path: str, data: bytes) -> None:
            wheel.writestr(path, data)
            digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
            rows.append((path, f"sha256={digest}", str(len(data))))

        for file in Path("src/cockpit32").rglob("*.py"):
            write(str(file.relative_to("src")), file.read_bytes())
        write(f"{DIST}/METADATA", f"Metadata-Version: 2.3\nName: {NAME}\nVersion: {VERSION}\nRequires-Python: >=3.11\n".encode())
        write(f"{DIST}/WHEEL", b"Wheel-Version: 1.0\nGenerator: cockpit32-local-backend\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
        write(f"{DIST}/entry_points.txt", b"[console_scripts]\ncockpit32=cockpit32.cli:main\n")
        record_path = f"{DIST}/RECORD"
        output = io.StringIO()
        writer = csv.writer(output, lineterminator="\n")
        for row in rows:
            writer.writerow(row)
        writer.writerow((record_path, "", ""))
        wheel.writestr(record_path, output.getvalue().encode())
    return buffer.getvalue()


def build_wheel(wheel_directory: str, config_settings=None, metadata_directory=None) -> str:
    filename = f"{NAME}-{VERSION}-py3-none-any.whl"
    Path(wheel_directory).mkdir(parents=True, exist_ok=True)
    Path(wheel_directory, filename).write_bytes(_wheel_bytes())
    return filename


def build_editable(wheel_directory: str, config_settings=None, metadata_directory=None) -> str:
    return build_wheel(wheel_directory, config_settings, metadata_directory)


def prepare_metadata_for_build_wheel(metadata_directory: str, config_settings=None) -> str:
    dist = Path(metadata_directory) / DIST
    dist.mkdir(parents=True, exist_ok=True)
    (dist / "METADATA").write_text(f"Metadata-Version: 2.3\nName: {NAME}\nVersion: {VERSION}\nRequires-Python: >=3.11\n", encoding="utf-8")
    return DIST
