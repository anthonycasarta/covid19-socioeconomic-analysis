import io
import shutil
import zipfile
from pathlib import Path

import requests


def copy_csv_files_from_repo_to_volume(
    repo_path: str,
    volume_root_path: str,
) -> None:
    source_dir = Path(repo_path)
    destination_root = Path(volume_root_path)

    if not source_dir.is_dir():
        raise FileNotFoundError(
            f"Repository data directory does not exist: {source_dir}"
        )

    for source_file in source_dir.glob("*.csv"):
        file_stem = source_file.stem

        if file_stem.endswith("_metadata"):
            dataset_name = file_stem.removesuffix("_metadata")
            content_type = "metadata"
        else:
            dataset_name = file_stem
            content_type = "data"

        destination_path = (
            destination_root / dataset_name / content_type / source_file.name
        )

        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copyfile(
            source_file,
            destination_path,
        )


def unzip_response_content(
    response_content: bytes,
) -> dict[str, bytes]:
    extracted_files = {}

    with zipfile.ZipFile(io.BytesIO(response_content)) as archive:
        for member_name in archive.namelist():
            file_name = Path(member_name).name

            if file_name and file_name.endswith(".csv"):
                extracted_files[file_name] = archive.read(member_name)

    return extracted_files


def get_response_content_from_url(url: str) -> bytes:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.content


def write_response_content_as_file_to_path(
    response_content: bytes, path: str, file_name: str, file_extension: str
) -> None:
    destination_path = Path(path) / f"{file_name}.{file_extension}"
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    destination_path.write_bytes(response_content)
