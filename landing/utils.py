from pathlib import Path
import requests
import io
import zipfile



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

def write_response_content_as_csv_to_path(response_content: bytes, path: str, file_name: str) -> None:
    destination_path = Path(path) / f"{file_name}.csv"
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    destination_path.write_bytes(response_content)
