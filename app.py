#!/usr/bin/env python3
"""Minimal Gradio UI for the meeting-notes demo (BYOK via .env)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from prompts import SYSTEM_PROMPT, build_user_prompt

DEFAULT_MODEL = "claude-sonnet-4-20250514"
ROOT = Path(__file__).resolve().parent
SAMPLE_NOTES = ROOT / "examples" / "sample_meeting_notes.txt"
SAMPLE_OUTPUT = ROOT / "examples" / "sample_output.md"


def resolve_api_key() -> str | None:
    return os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")


def call_claude(notes: str, model: str, api_key: str) -> str:
    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(notes)}],
    )
    parts: list[str] = []
    for block in message.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    return "\n".join(parts).strip()


def generate(notes: str, model: str) -> str:
    notes = (notes or "").strip()
    if not notes:
        return "Paste meeting notes above (or click **Load sample notes**)."

    api_key = resolve_api_key()
    if not api_key:
        return (
            "**No API key found.**\n\n"
            "Set `CLAUDE_API_KEY` (or `ANTHROPIC_API_KEY`) in a `.env` file "
            "(see `.env.example`), then restart this app.\n\n"
            "Meanwhile, click **Show sample output** for a no-key preview."
        )

    try:
        return call_claude(notes, model=model or DEFAULT_MODEL, api_key=api_key)
    except Exception as exc:  # noqa: BLE001
        return f"**Error calling Claude API:** {exc}"


def load_sample_notes() -> str:
    if SAMPLE_NOTES.is_file():
        return SAMPLE_NOTES.read_text(encoding="utf-8")
    return ""


def show_sample_output() -> str:
    if SAMPLE_OUTPUT.is_file():
        return SAMPLE_OUTPUT.read_text(encoding="utf-8")
    return "Sample output file missing."


def build_ui():
    import gradio as gr

    with gr.Blocks(title="Northline Meeting Notes Demo") as demo:
        gr.Markdown(
            "# Northline Meeting Notes Demo\n"
            "**Free portfolio demo — not client work.** BYOK: uses your "
            "`CLAUDE_API_KEY` / `ANTHROPIC_API_KEY` from `.env`."
        )
        notes = gr.Textbox(
            label="Meeting notes",
            lines=14,
            placeholder="Paste raw meeting notes here…",
        )
        model = gr.Textbox(label="Model", value=DEFAULT_MODEL)
        with gr.Row():
            btn_gen = gr.Button("Generate", variant="primary")
            btn_load = gr.Button("Load sample notes")
            btn_sample = gr.Button("Show sample output (no key)")
        output = gr.Markdown(label="Output")

        btn_gen.click(generate, inputs=[notes, model], outputs=output)
        btn_load.click(load_sample_notes, inputs=None, outputs=notes)
        btn_sample.click(show_sample_output, inputs=None, outputs=output)

    return demo


def main() -> None:
    load_dotenv()
    demo = build_ui()
    demo.launch()


if __name__ == "__main__":
    main()
