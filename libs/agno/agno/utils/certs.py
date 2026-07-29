from pathlib import Path

import requests


def download_cert(cert_url: str, filename: str = "cert.pem") -> str:
    """
    Downloads a CA certificate bundle if it doesn't exist locally.

    Args:
        cert_url (str): URL to download the certificate bundle from.
        filename (str): Name to save the certificate file as, relative to ./certs.

    Returns:
        str: Path to the certificate file
    """
    cert_dir = Path("./certs")
    cert_path = cert_dir / filename

    # Create directory if it doesn't exist
    cert_dir.mkdir(parents=True, exist_ok=True)

    # Download the certificate if it doesn't exist
    if not cert_path.exists():
        response = requests.get(cert_url)
        response.raise_for_status()

        with open(cert_path, "wb") as f:
            f.write(response.content)

    return str(cert_path.absolute())
