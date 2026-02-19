#!/usr/bin/env python3
"""Run Codex screening on multiple batch directories in parallel.

Uses ProcessPoolExecutor to run `codex exec` on each batch directory.
Creates .codex-done on success or .codex-failed on failure for each batch.

Usage:
    python3 run-codex-batches.py \
        --batch-dirs dir1,dir2,dir3 \
        [--max-workers 4] \
        [--timeout 300]
"""

import argparse
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


def run_single_batch(batch_dir: str, timeout: int) -> tuple[str, bool, float, str]:
    """Run codex exec on a single batch directory.

    Returns (batch_dir, success, elapsed_seconds, message).
    """
    batch_path = Path(batch_dir)
    prompt_file = batch_path / "prompt.md"
    done_marker = batch_path / ".codex-done"
    fail_marker = batch_path / ".codex-failed"

    # Clean up old markers
    for marker in [done_marker, fail_marker]:
        marker.unlink(missing_ok=True)

    if not prompt_file.exists():
        msg = f"prompt.md not found in {batch_dir}"
        fail_marker.touch()
        return (batch_dir, False, 0.0, msg)

    start = time.monotonic()
    try:
        with open(prompt_file, "r") as f:
            prompt_content = f.read()

        result = subprocess.run(
            [
                "codex", "exec",
                "--full-auto",
                "--skip-git-repo-check",
                "-C", str(batch_path),
                "-",
            ],
            input=prompt_content,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = time.monotonic() - start

        if result.returncode == 0:
            done_marker.touch()
            return (batch_dir, True, elapsed, "OK")
        else:
            fail_marker.touch()
            stderr_tail = result.stderr[-500:] if result.stderr else "(no stderr)"
            return (batch_dir, False, elapsed, f"exit code {result.returncode}: {stderr_tail}")

    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - start
        fail_marker.touch()
        return (batch_dir, False, elapsed, f"timeout after {timeout}s")
    except Exception as e:
        elapsed = time.monotonic() - start
        fail_marker.touch()
        return (batch_dir, False, elapsed, str(e))


def main():
    parser = argparse.ArgumentParser(
        description="Run Codex screening on multiple batch directories in parallel."
    )
    parser.add_argument(
        "--batch-dirs",
        required=True,
        help="Comma-separated list of absolute paths to batch directories",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="Maximum parallel Codex processes (default: 4)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Per-batch timeout in seconds (default: 300)",
    )
    args = parser.parse_args()

    batch_dirs = [d.strip() for d in args.batch_dirs.split(",") if d.strip()]
    total = len(batch_dirs)

    if total == 0:
        print("No batch directories provided.", file=sys.stderr)
        sys.exit(1)

    print(f"Starting Codex screening: {total} batches, max_workers={args.max_workers}, timeout={args.timeout}s")

    completed = 0
    failed = 0

    with ProcessPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {
            executor.submit(run_single_batch, bd, args.timeout): bd
            for bd in batch_dirs
        }

        for future in as_completed(futures):
            batch_dir, success, elapsed, msg = future.result()
            batch_name = Path(batch_dir).name
            completed += 1

            if success:
                print(f"[{completed}/{total}] {batch_name}: DONE in {elapsed:.0f}s")
            else:
                failed += 1
                print(f"[{completed}/{total}] {batch_name}: FAILED ({msg})")

    print(f"\nCodex screening complete: {total - failed}/{total} succeeded, {failed} failed")
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
