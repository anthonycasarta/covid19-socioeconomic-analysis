from pathlib import Path
import requests

def download_as_csv_from_url_to_path(url: str, path: str, file_name: str) -> None:
    destination_path = Path(path) / f"{file_name}.csv"
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, timeout=60)
    response.raise_for_status()
    destination_path.write_bytes(response.content)
