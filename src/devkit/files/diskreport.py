# Recursively scans a directory for files and reports the largest / oldest /
# newest ones. Only files are listed (not folders), and the scan is
# recursive by default since this command is read-only — there's no risk of
# reorganizing anything by mistake, unlike `organize`.

import os
from datetime import datetime


def _scan_files(root: str) -> tuple[list[tuple[int, float, str]], list[str]]:
    # Walks `root` recursively and returns (size, mtime, path) for every
    # file found, plus a list of warnings for anything that couldn't be
    # read. Errors are collected instead of raised, so one inaccessible
    # file or folder doesn't abort the whole scan.
    entries: list[tuple[int, float, str]] = []
    warnings: list[str] = []

    def _on_error(error: OSError) -> None:
        # Called by os.walk when it can't list a directory (e.g.
        # permission denied on the folder itself).
        warnings.append(f"{error.filename}: {error.strerror}")

    for dirpath, _dirnames, filenames in os.walk(root, onerror=_on_error):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                stat = os.stat(filepath)
            except OSError as error:
                # Different from _on_error above: this is a per-file
                # failure (e.g. a broken symlink), not a failure to list
                # the containing directory.
                warnings.append(f"{filepath}: {error.strerror}")
                continue
            entries.append((stat.st_size, stat.st_mtime, filepath))

    return entries, warnings


def _format_size(num_bytes: float) -> str:
    # Converts a raw byte count into a human-readable string (KB/MB/GB...).
    # The final return outside the loop is a fallback for the (unlikely)
    # case of a file larger than 1024 TB.
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} PB"


def run(path: str, by: str, order: str, top: int) -> None:
    entries, warnings = _scan_files(path)

    if by == "size":
        entries.sort(key=lambda entry: entry[0], reverse=order == "desc")
    else:
        # Intentionally inverted: a larger st_mtime means a more recent
        # file, but "desc" for --by age is defined as "oldest first". So
        # reverse only needs to flip when order is "asc" (newest first).
        entries.sort(key=lambda entry: entry[1], reverse=order == "asc")

    for size, mtime, filepath in entries[:top]:
        modified = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        # :>10 right-aligns the size so the column stays lined up
        # regardless of unit width (e.g. "4.2 KB" vs "128.0 MB").
        print(f"{_format_size(size):>10}  {modified}  {filepath}")

    if warnings:
        # Deliberate exception to the MVP's "no defensive error handling"
        # rule: `hash` lets FileNotFoundError propagate as-is, but a
        # recursive filesystem walk needs to degrade gracefully instead of
        # crashing on the first permission-denied folder.
        print(f"\n{len(warnings)} item(s) could not be read:")
        for warning in warnings:
            print(f"  {warning}")
