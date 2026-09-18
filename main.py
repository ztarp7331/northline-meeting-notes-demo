#!/usr/bin/env python3
"""CLI: turn meeting notes into action items + follow-up email drafts via Claude."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # optional for --show-sample
    def load_dotenv(*_a, **_k):
        return False


from prompts import SYSTEM_PROMPT, build_user_prompt

DEFAULT_MODEL = "claude-sonnet-4-20250514"


def resolve_api_key() -> str | None:
    """Prefer CLAUDE_API_KEY; accept ANTHROPIC_API_KEY as alias."""
    return os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")


def read_notes(path: str | None) -> str:
    """Read meeting notes from a file path, or from stdin if path is None/-."""
    if path is None or path == "-":
        if sys.stdin.isatty():
            print(
                "Error: no notes file provided and stdin is a TTY.\n"
                "Pass a file path, or pipe notes via stdin.",
                file=sys.stderr,
            )
            sys.exit(1)
        return sys.stdin.read()

    notes_path = Path(path)
    if not notes_path.is_file():
        print(f"Error: notes file not found: {notes_path}", file=sys.stderr)
        sys.exit(1)
    return notes_path.read_text(encoding="utf-8")


def call_claude(notes: str, model: str, api_key: str) -> str:
    """Call Anthropic Messages API and return the assistant text."""
    # Imported here so `--help` works even before the package is installed.
    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": build_user_prompt(notes),
            }
        ],
    )

    parts: list[str] = []
    for block in message.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    return "\n".join(parts).strip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description=(
            "Turn meeting notes into structured action items and "
            "draft follow-up emails using the Claude API."
        ),
    )
    parser.add_argument(
        "notes_file",
        nargs="?",
        default=None,
        help="Path to meeting notes (.txt). Omit or use '-' to read from stdin.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Claude model id (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--show-sample",
        action="store_true",
        help="Print examples/sample_output.md and exit (no API call).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.show_sample:
        sample = Path(__file__).resolve().parent / "examples" / "sample_output.md"
        if not sample.is_file():
            print(f"Error: sample output not found at {sample}", file=sys.stderr)
            return 1
        print(sample.read_text(encoding="utf-8"), end="")
        return 0

    api_key = resolve_api_key()
    if not api_key:
        print(
            "Error: missing API key.\n"
            "Set CLAUDE_API_KEY in your environment or in a .env file "
            "(see .env.example).\n"
            "ANTHROPIC_API_KEY is also accepted as an alias.\n"
            "Or run with --show-sample to preview example output without an API call.",
            file=sys.stderr,
        )
        return 1

    notes = read_notes(args.notes_file)
    if not notes.strip():
        print("Error: meeting notes are empty.", file=sys.stderr)
        return 1

    try:
        output = call_claude(notes, model=args.model, api_key=api_key)
    except Exception as exc:  # noqa: BLE001 — surface SDK/network errors cleanly
        print(f"Error calling Claude API: {exc}", file=sys.stderr)
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
