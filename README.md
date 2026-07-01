# Those Who Stood Studio

A starter web-app style workspace for writing chapters and maintaining a living canon for *Those Who Stood*.

This version is designed so it can be deployed online and opened from an iPhone, iPad, laptop, or desktop browser.

## What it does now

- Chat-style Lorekeeper panel.
- Chapter writing and saving as Markdown.
- Import page for current lore, campaign notes, and old chapter drafts.
- Preserves imported material in `Archive/Source Material` before any canon changes.
- Canon manager for Canon Bible, Characters, Locations, Guild, System, Timeline, and Continuity Log.
- Folder planner based on the recommended project structure.
- Optional OpenAI API integration.

## Run locally on a computer

1. Install Python 3.11 or newer.
2. Open a terminal in this folder.
3. Run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Use it from iPhone

An iPhone cannot easily run this local Python app by itself. To use it on iPhone, deploy it as a web app.

### Easiest deployment option: Streamlit Community Cloud

1. Create a free GitHub account if you do not have one.
2. Create a new private GitHub repository.
3. Upload these app files to the repository.
4. Go to Streamlit Community Cloud.
5. Connect your GitHub repository.
6. Set the app file to `app.py`.
7. Deploy.
8. Open the generated web link on your iPhone.

## Optional AI setup

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
OPENAI_API_KEY
```

On Streamlit Cloud, add these as app secrets instead of uploading a `.env` file.

Without an API key, the app still works as a structured writing and canon manager, but AI responses use a basic local placeholder.

## Safe import workflow

Use this order to avoid losing continuity:

1. Import existing material into `Archive/Source Material`.
2. Do not overwrite old material.
3. Extract possible canon into suggested updates.
4. Promote only confirmed details into Canon Bible, Timeline, Characters, Locations, Guild, or System.
5. Put name changes and contradictions in Continuity Log.

Known adaptation changes already tracked:

- Highland Plague → Corin.
- Those Who Bore Witness → Those Who Stood.
- SAO-inspired language should be transformed into original terminology.

## Recommended next features

- User login.
- Cloud database.
- Git auto-commit after every chapter save.
- Better AI canon extraction using structured JSON.
- Continuity scanner.
- Character relationship graph.
- Export manuscript to DOCX/PDF.
- Image prompt generator.
