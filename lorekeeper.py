from __future__ import annotations

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Iterable

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

PROJECT_ROOT = Path(__file__).parent / "sample_project"
ARCHIVE_ROOT = PROJECT_ROOT / "Archive" / "Source Material"
IMPORTS_ROOT = PROJECT_ROOT / "Imports"

CANON_PATHS = {
    "Canon Bible": PROJECT_ROOT / "Canon" / "Canon Bible.md",
    "Characters": PROJECT_ROOT / "Canon" / "Characters" / "Characters Index.md",
    "Locations": PROJECT_ROOT / "Canon" / "Locations" / "Locations Index.md",
    "System": PROJECT_ROOT / "Canon" / "System" / "System Rules.md",
    "Guild": PROJECT_ROOT / "Canon" / "Guild" / "Those Who Stood.md",
    "Timeline": PROJECT_ROOT / "Timeline" / "Timeline.md",
    "Continuity Log": PROJECT_ROOT / "Continuity" / "Continuity Log.md",
}

DEFAULT_FILES = {
    "Canon Bible": "# Canon Bible\n\n## Confirmed Core Canon\n\n- World name: Asterra\n- People trapped/arriving in the world are known as Delvers\n- Main character: Corin\n- Guild: Those Who Stood\n- Origin phrase/guild predecessor: Those Who Bore Witness\n\n## Open Questions\n\n- What are the Anchors?\n- What is the true purpose of the System?\n- How much of Highland Plague remains as legacy/campaign identity versus Corin as novel canon?\n",
    "Characters": "# Characters Index\n\n## Corin\n- Main character.\n- Formerly derived from the campaign identity Highland Plague.\n- A Delver with unusual access to the System.\n\n## Lyra\n- Half-elf companion and trusted confidante.\n- Early 30s, red hair, petite athletic build.\n\n## Gareth\n- Practical leader and organiser within the guild.\n",
    "Locations": "# Locations Index\n\n## Asterra\n- The world in which the story takes place.\n\n## Corin\n- Replacement name for the earlier Highland/Highland-related place naming direction where applicable.\n",
    "System": "# System Rules\n\n## Known Rules\n\n- The world behaves partly like a game environment.\n- Mana, progression, Delver mechanics, and hidden mechanics exist.\n- Corin has unusual/backdoor-style interaction with the System, inherited from the campaign concept.\n",
    "Guild": "# Those Who Stood\n\n## Doctrine\n\n- No single figurehead.\n- Shared witness, shared responsibility.\n- Observe, adapt, overcome.\n- The guild grew from people gathered around a shared experience rather than a heroic leader.\n",
    "Timeline": "# Timeline\n\n## Legacy Campaign Origins\n\n- Highland Plague enters the death-game-like world.\n- Lyra becomes a key guide and confidante.\n- Gareth emerges as an organiser and expedition leader.\n- Those Who Bore Witness forms as a guild philosophy.\n\n## Novel Continuity\n\n- Highland Plague is adapted into Corin.\n- The world is renamed Asterra.\n- Players are reframed as Delvers.\n- The guild name becomes Those Who Stood.\n",
    "Continuity Log": "# Continuity Log\n\nUse this to track contradictions, retcons, name changes, and decisions that need review.\n\n## Known Adaptation Changes\n\n- Highland Plague → Corin.\n- Those Who Bore Witness → Those Who Stood.\n- SAO-inspired language should be transformed into original terminology.\n",
}

FOLDER_RECOMMENDATIONS = [
    "00 - Vision & Philosophy",
    "01 - Novel",
    "02 - Worldbuilding",
    "03 - The System",
    "04 - Characters",
    "05 - Guild",
    "06 - Locations",
    "07 - Floors and Regions",
    "08 - Creatures",
    "09 - Magic and Combat",
    "10 - Lore",
    "11 - Images and References",
    "12 - Notes and Ideas",
    "Archive/Source Material",
    "Continuity",
    "Imports",
]


def ensure_project() -> None:
    for path in CANON_PATHS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    for name, content in DEFAULT_FILES.items():
        path = CANON_PATHS[name]
        if not path.exists():
            path.write_text(content, encoding="utf-8")
    for folder in FOLDER_RECOMMENDATIONS:
        (PROJECT_ROOT / folder).mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / "01 - Novel" / "Chapters").mkdir(parents=True, exist_ok=True)


def safe_filename(name: str) -> str:
    safe = "".join(c for c in name if c.isalnum() or c in " -_()").strip().replace(" ", "_")
    return safe or f"Untitled_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def list_chapters() -> List[Path]:
    ensure_project()
    chapters = list((PROJECT_ROOT / "01 - Novel" / "Chapters").glob("*.md"))
    chapters += list((PROJECT_ROOT / "Novel").glob("*.md")) if (PROJECT_ROOT / "Novel").exists() else []
    return sorted(set(chapters))


def save_chapter(title: str, body: str) -> Path:
    ensure_project()
    path = PROJECT_ROOT / "01 - Novel" / "Chapters" / f"{safe_filename(title)}.md"
    path.write_text(f"# {title}\n\n{body.strip()}\n", encoding="utf-8")
    return path


def archive_text(title: str, body: str, source_type: str = "manual paste") -> Path:
    ensure_project()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = ARCHIVE_ROOT / f"{stamp}_{safe_filename(title)}.md"
    path.write_text(f"# {title}\n\n_Source: {source_type}_\n_Imported: {datetime.now().isoformat(timespec='seconds')}_\n\n{body.strip()}\n", encoding="utf-8")
    return path


def import_uploaded_file(filename: str, data: bytes) -> Path:
    ensure_project()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = IMPORTS_ROOT / f"{stamp}_{safe_filename(filename)}"
    path.write_bytes(data)
    archive_copy = ARCHIVE_ROOT / path.name
    shutil.copy2(path, archive_copy)
    return path


def read_markdown_files(paths: Iterable[Path], max_chars: int = 120_000) -> str:
    parts = []
    total = 0
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        chunk = f"\n\n--- FILE: {path.relative_to(PROJECT_ROOT)} ---\n{text}"
        if total + len(chunk) > max_chars:
            break
        parts.append(chunk)
        total += len(chunk)
    return "".join(parts)


def read_context(include_chapters: bool = False) -> str:
    ensure_project()
    sections = []
    for name, path in CANON_PATHS.items():
        sections.append(f"## {name}\n{path.read_text(encoding='utf-8')}")
    if include_chapters:
        sections.append("## Chapters" + read_markdown_files(list_chapters(), max_chars=80_000))
    return "\n\n".join(sections)


def append_canon_update(section: str, update: str) -> None:
    ensure_project()
    path = CANON_PATHS.get(section)
    if not path:
        raise ValueError(f"Unknown section: {section}")
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with path.open("a", encoding="utf-8") as f:
        f.write(f"\n\n## Update - {stamp}\n\n{update.strip()}\n")


def basic_lore_extract(chapter_text: str) -> Dict[str, str]:
    words = chapter_text.split()
    capitalised = sorted({w.strip('.,!?;:\"()[]') for w in words if w[:1].isupper() and len(w) > 2})
    names = ", ".join(capitalised[:30]) if capitalised else "None detected"
    return {
        "Canon Bible": f"Review needed. Possible new canon from latest material. Notable terms: {names}",
        "Timeline": "Add a timeline entry summarising the latest chapter or imported scene's main event.",
        "Characters": f"Possible character/location terms to review: {names}",
        "Continuity Log": "Review whether this material belongs to legacy campaign canon, novel canon, or both.",
    }


def ai_chat(user_message: str, project_context: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "AI key not configured yet. Local Lorekeeper suggestion:\n\n"
            "- Save/import the material first so it is preserved.\n"
            "- Add confirmed facts to Canon Bible.\n"
            "- Add plot movement to Timeline.\n"
            "- Update affected character, location, guild, or system files.\n"
            "- Put retcons/name changes in the Continuity Log.\n\n"
            f"Your request was: {user_message}"
        )

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            messages=[
                {"role": "system", "content": "You are the Lorekeeper for the novel project Those Who Stood. Help write, organise, preserve canon, and flag continuity issues. Treat source imports as preserved legacy material until the user promotes them to novel canon. Be concise and practical."},
                {"role": "user", "content": f"PROJECT CONTEXT:\n{project_context}\n\nUSER REQUEST:\n{user_message}"},
            ],
        )
        return response.choices[0].message.content or "No response returned."
    except Exception as exc:
        return f"AI call failed: {exc}"
