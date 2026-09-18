# Northline Scripts — Meeting Notes → Action Items + Follow-ups

**Free demo** (not client work). Paste messy meeting notes, get prioritized action items and draft follow-up emails. You review before anything is sent — no auto-send, no scraping.

Built with Python + Claude (bring your own API key).

## 2-minute try (no API key)

```bash
unzip northline-meeting-notes-demo.zip
cd northline-meeting-notes-demo
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py --show-sample
```

Or: `bash run_demo.sh`

## Live run (your Claude key)

```bash
cp .env.example .env
# set CLAUDE_API_KEY=sk-ant-...
python main.py examples/sample_meeting_notes.txt
```

Optional local UI: `pip install gradio && python app.py`

## Links

| | |
|---|---|
| This repo | `https://github.com/ztarp7331/northline-meeting-notes-demo` |
| Paid unlock ($39) | `https://northline.gumroad.com/REPLACE` — extra prompts, batch mode, hardened examples |
| Custom 48h builds | https://contra.com/s/6goFrYLF-custom-ai-workflow-python-script-in-48-hours-or-for-solopreneur |

## What you get (free)

- CLI: notes file or stdin → markdown Action Items + Follow-up Emails
- `--show-sample` canned output for demos without a key
- Gradio UI (`app.py`) for local tryouts
- MIT license — you keep and modify the code

## Ethics

You supply the notes. Network call is Anthropic only. Drafts are for human review — do not auto-send to clients.

## Requirements

Python 3.10+, `anthropic`, `python-dotenv` (see `requirements.txt`). Optional: `gradio` for the UI.
