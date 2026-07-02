from typing import List

from agno.utils.log import log_debug, log_info, log_warning


def run_shell_command(args: List[str], tail: int = 100) -> str:
    """Run a shell command and return its output.

    On success, returns the last `tail` lines of stdout. On failure (either a
    non-zero return code or an exception raised while launching the process),
    returns a string prefixed with `"Error: "` instead of raising.

    Args:
        args: The command and its arguments, e.g. `["ls", "-la"]`.
        tail: Maximum number of trailing stdout lines to return.

    Returns:
        The command's trailing stdout output, or an `"Error: ..."` message
        describing the failure.
    """
    log_info(f"Running shell command: {args}")

    import subprocess

    try:
        result = subprocess.run(args, capture_output=True, text=True)
        log_debug(f"Result: {result}")
        log_debug(f"Return code: {result.returncode}")
        if result.returncode != 0:
            return f"Error: {result.stderr}"

        # return only the last n lines of the output
        return "\n".join(result.stdout.split("\n")[-tail:])
    except Exception as e:
        log_warning(f"Failed to run shell command: {str(e)}")
        return f"Error: {e}"
