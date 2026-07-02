import webbrowser
from pathlib import Path

from agno.utils.log import log_error


def open_html_file(file_path: Path) -> None:
    """Open the specified HTML file in the default web browser.

    Args:
        file_path: Path to the HTML file.

    Raises:
        FileNotFoundError: If `file_path` does not resolve to an existing file.
    """
    # Resolve the absolute path
    absolute_path = file_path.resolve()

    if not absolute_path.is_file():
        log_error(f"The file '{absolute_path}' does not exist.")
        raise FileNotFoundError(f"The file '{absolute_path}' does not exist.")

    # Convert the file path to a file URI
    file_url = absolute_path.as_uri()

    # Open the file in the default web browser
    webbrowser.open(file_url)
