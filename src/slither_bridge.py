import subprocess
import os

def run_slither(sol_file_path: str) -> str:
    """
    Runs Slither static analysis on a given Solidity file.

    Args:
        sol_file_path (str): Full path to the Solidity contract file.

    Returns:
        str: The combined stdout and stderr output from Slither.
    """
    if not os.path.isfile(sol_file_path):
        return f"[ERROR] File not found: {sol_file_path}"

    try:
        result = subprocess.run(
            ["slither", sol_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=30
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "[ERROR] Slither timed out."
    except Exception as e:
        return f"[ERROR] Failed to run Slither: {str(e)}"
