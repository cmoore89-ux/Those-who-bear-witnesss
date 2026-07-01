from __future__ import annotations

import streamlit as st
from lorekeeper import (
    CANON_PATHS,
    FOLDER_RECOMMENDATIONS,
    PROJECT_ROOT,
    ai_chat,
    append_canon_update,
    archive_text,
    basic_lore_extract,
    ensure_project,
    import_uploaded_file,
    list_chapters,
    read_context,
    save_chapter,
)

st.set_page_config(page_title="Those Who Stood Studio", page_icon="📜", layout="wide")
ensure_project()

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1200px;}
    [data-testid="stSidebar"] {min-width: 250px;}
    .tws-card {border: 1px solid rgba(128,128,128,.25); border-radius: 14px; padding: 1rem; margin: .5rem 0;}
    .small-note {font-size: .9rem; opacity: .8;}
    textarea {font-size: 1rem !important;}
    @media (max-width: 800px) {
      .block-container {padding-left: .8rem; padding-right: .8rem;}
      [data-testid="column"] {width: 100% !important; flex: 1 1 100% !important;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📜 Those Who Stood Studio")
st.caption("A phone-friendly writing, canon, import, and Lorekeeper workspace.")

with st.sidebar:
    st.header("Project")
    st.write(f"Root: `{PROJECT_ROOT}`")
    page = st.radio(
        "Go to",
        ["Home", "Lorekeeper Chat", "Write Chapter", "Import Current Lore", "Canon Manager", "Folder Planner", "Project Files"],
    )

if page == "Home":
    st.subheader("Welcome")
    st.markdown(
        """
        This version is designed to be deployed as a web app so you can open it from Safari on iPhone.

        **Recommended workflow:**
        1. Import old chats/notes into **Archive / Source Material**.
        2. Save chapters in **01 - Novel / Chapters**.
        3. Promote only confirmed details into **Canon Bible**.
        4. Track retcons and name changes in **Continuity Log**.
        """
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Chapters", len(list_chapters()))
    c2.metric("Canon Files", len(CANON_PATHS))
    c3.metric("Folders", len(FOLDER_RECOMMENDATIONS))

elif page == "Lorekeeper Chat":
    st.subheader("💬 Lorekeeper Chat")
    st.write("Ask for a chapter, canon update, folder recommendation, continuity check, or worldbuilding help.")

    include_chapters = st.toggle("Include chapter text in context", value=False, help="Turn on for continuity checks. Leave off for faster replies.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask the Lorekeeper...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            answer = ai_chat(prompt, read_context(include_chapters=include_chapters))
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

elif page == "Write Chapter":
    st.subheader("📖 Write Chapter")
    title = st.text_input("Chapter title", value="Chapter 1 - The First Step")
    body = st.text_area("Chapter text", height=420, placeholder="Write or paste your chapter here...")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Chapter", type="primary", use_container_width=True):
            path = save_chapter(title, body)
            st.success(f"Saved: {path.relative_to(PROJECT_ROOT)}")
    with col2:
        if st.button("Extract Suggested Canon Updates", use_container_width=True):
            updates = basic_lore_extract(body)
            st.session_state.pending_updates = updates
            st.success("Suggested updates generated.")

    if "pending_updates" in st.session_state:
        st.markdown("### Suggested Canon Updates")
        for section, update in st.session_state.pending_updates.items():
            st.markdown(f"**{section}**")
            edited = st.text_area(f"Update for {section}", value=update, key=f"pending_{section}")
            if st.button(f"Append to {section}", key=f"append_{section}"):
                append_canon_update(section, edited)
                st.success(f"Updated {section}")

elif page == "Import Current Lore":
    st.subheader("📥 Import Current Lore")
    st.write("Use this to preserve our current campaign notes, chapter drafts, and lore before cleaning them into novel canon.")

    tab1, tab2 = st.tabs(["Paste text", "Upload files"])
    with tab1:
        title = st.text_input("Import title", value="Legacy chat extract")
        source_type = st.selectbox("Source type", ["Chat export", "Campaign notes", "Chapter draft", "Worldbuilding notes", "Other"])
        pasted = st.text_area("Paste existing lore/chapter material", height=360)
        c1, c2 = st.columns(2)
        if c1.button("Archive Only", use_container_width=True):
            path = archive_text(title, pasted, source_type)
            st.success(f"Archived safely: {path.relative_to(PROJECT_ROOT)}")
        if c2.button("Archive + Suggest Canon", type="primary", use_container_width=True):
            path = archive_text(title, pasted, source_type)
            st.session_state.pending_updates = basic_lore_extract(pasted)
            st.success(f"Archived safely: {path.relative_to(PROJECT_ROOT)}")

    with tab2:
        files = st.file_uploader("Upload .md, .txt, .docx export text, or notes", accept_multiple_files=True)
        if st.button("Import Uploaded Files", type="primary"):
            imported = []
            for f in files or []:
                imported.append(import_uploaded_file(f.name, f.getvalue()))
            if imported:
                st.success("Imported and archived:\n" + "\n".join(str(p.relative_to(PROJECT_ROOT)) for p in imported))
            else:
                st.info("No files selected.")

elif page == "Canon Manager":
    st.subheader("📚 Canon Manager")
    section = st.selectbox("Canon section", list(CANON_PATHS.keys()))
    path = CANON_PATHS[section]
    content = path.read_text(encoding="utf-8")
    edited = st.text_area(section, value=content, height=520)
    if st.button("Save Canon File", type="primary"):
        path.write_text(edited, encoding="utf-8")
        st.success(f"Saved {section}")

elif page == "Folder Planner":
    st.subheader("📁 Folder Planner")
    st.write("Recommended structure for this project:")
    for folder in FOLDER_RECOMMENDATIONS:
        st.markdown(f"- `{folder}`")

    if st.button("Create Recommended Folders", type="primary"):
        for folder in FOLDER_RECOMMENDATIONS:
            (PROJECT_ROOT / folder).mkdir(parents=True, exist_ok=True)
        st.success("Folders created inside the project.")

elif page == "Project Files":
    st.subheader("🗂 Project Files")
    st.markdown("### Chapters")
    chapters = list_chapters()
    if not chapters:
        st.info("No chapters saved yet.")
    for chapter in chapters:
        with st.expander(str(chapter.relative_to(PROJECT_ROOT))):
            st.markdown(chapter.read_text(encoding="utf-8"))

    st.markdown("### Canon Files")
    for name, path in CANON_PATHS.items():
        st.markdown(f"- **{name}** — `{path.relative_to(PROJECT_ROOT)}`")
