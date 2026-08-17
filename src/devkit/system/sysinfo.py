import os
import platform
import shutil
import socket


def _format_size(num_bytes: float) -> str:
    # Converts a raw byte count into a human-readable string (KB/MB/GB...).
    # The final return outside the loop is a fallback for the (unlikely)
    # case of a disk larger than 1024 TB.
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} PB"


def run(path: str) -> None:
    # socket.gethostname() returns the machine's network hostname — the
    # same name usually shown in the terminal prompt.
    hostname = socket.gethostname()

    # platform.system()/release()/machine() combined describe the OS in one
    # readable line, e.g. "Linux 6.14.0-29-generic (x86_64)".
    os_summary = f"{platform.system()} {platform.release()} ({platform.machine()})"

    python_version = platform.python_version()

    # os.cpu_count() can return None if the core count can't be determined
    # (rare, but possible) — fall back to a placeholder instead of printing
    # the literal "None".
    cpu_cores = os.cpu_count() or "unknown"

    # shutil.disk_usage() reports stats for the whole partition/filesystem
    # that contains `path`, not just that specific folder. It raises
    # FileNotFoundError if `path` doesn't exist — left to propagate as-is,
    # same MVP philosophy as hash.py.
    total, used, free = shutil.disk_usage(path)
    percent_used = used / total * 100
    disk_label = f"Disk ({path})"

    # ":<17" left-pads every label to the same width, so the ":" separators
    # line up in a column regardless of how long each label is.
    print(f"{'Hostname':<17}: {hostname}")
    print(f"{'Operating System':<17}: {os_summary}")
    print(f"{'Python':<17}: {python_version}")
    print(f"{'CPU cores':<17}: {cpu_cores}")
    print(f"{disk_label:<17}: {_format_size(free)} free / {_format_size(total)} total ({percent_used:.0f}% used)")
