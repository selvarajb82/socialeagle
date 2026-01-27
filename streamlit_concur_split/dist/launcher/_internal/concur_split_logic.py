import streamlit as st
from collections import defaultdict
import zipfile
import io
import string

# ---------------- CONFIG ----------------
DELIMITER = "|"
REPORT_KEY_INDEX = 19
JOURNAL_AMOUNT_INDEX = 168
# ----------------------------------------

st.set_page_config(
    page_title="Concur File Splitter",
    page_icon="📂",
    layout="wide"
)

st.title("📊 Concur File Splitter")
st.caption("Concur-compliant • Exact splits • Correct EXTRACT")

# ---------- SESSION STATE ----------
if "zip_data" not in st.session_state:
    st.session_state.zip_data = None

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader(
    "Upload Concur input file",
    type=["dat", "txt"]
)

# ---------- SPLIT MODE ----------
split_mode = st.radio(
    "Select split method (only one allowed)",
    ["Max lines per split file", "Number of split files"]
)

if split_mode == "Max lines per split file":
    max_lines = st.number_input(
        "Max lines per split file",
        min_value=1,
        value=810
    )
    num_files = None
else:
    num_files = st.number_input(
        "Number of split files",
        min_value=1,
        value=2
    )
    max_lines = None

# ---------- CORE FUNCTIONS ----------


def parse_input(lines):
    extract_line = next(l for l in lines if l.startswith("EXTRACT|"))
    detail_lines = [l for l in lines if l.startswith("DETAIL|")]
    return extract_line, detail_lines


def group_by_report_key(lines):
    grouped = defaultdict(list)
    for line in lines:
        cols = line.split(DELIMITER)
        grouped[cols[REPORT_KEY_INDEX]].append(line)
    return grouped


def calculate_total(lines):
    total = 0.0
    for l in lines:
        try:
            total += float(l.split(DELIMITER)[JOURNAL_AMOUNT_INDEX])
        except:
            pass
    return total


def rebuild_extract(original_extract, record_count, total_amount):
    cols = original_extract.split(DELIMITER)
    cols[2] = str(record_count)
    cols[3] = f"{total_amount:.4f}"
    return DELIMITER.join(cols)


def split_by_max_lines(grouped, max_lines):
    batches, current, count = [], [], 0

    for group in grouped.values():
        if count + len(group) > max_lines:
            batches.append(current)
            current, count = [], 0
        current.extend(group)
        count += len(group)

    if current:
        batches.append(current)

    return batches


def split_by_exact_file_count(grouped, num_files):
    """
    EXACTLY num_files files.
    Report keys are never split.
    Balanced by record count.
    """
    groups = sorted(grouped.values(), key=len, reverse=True)

    batches = [[] for _ in range(num_files)]
    batch_sizes = [0] * num_files

    for group in groups:
        idx = batch_sizes.index(min(batch_sizes))
        batches[idx].extend(group)
        batch_sizes[idx] += len(group)

    return batches


# ---------- PROCESS ----------
if uploaded_file and st.button("🚀 Split File"):
    try:
        raw_lines = uploaded_file.read().decode("utf-8").splitlines()
        extract_line, detail_lines = parse_input(raw_lines)
        grouped = group_by_report_key(detail_lines)

        if split_mode == "Max lines per split file":
            batches = split_by_max_lines(grouped, max_lines)
        else:
            batches = split_by_exact_file_count(grouped, num_files)

        base_name, ext = uploaded_file.name.rsplit(".", 1)

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for idx, batch in enumerate(batches):
                suffix = string.ascii_uppercase[idx]
                file_name = f"{base_name}_{suffix}.{ext}"

                count = len(batch)
                total = calculate_total(batch)
                new_extract = rebuild_extract(extract_line, count, total)

                content = new_extract + "\n" + "\n".join(batch)
                zipf.writestr(file_name, content)

                st.success(f"✅ {file_name} created")

        st.session_state.zip_data = zip_buffer.getvalue()
        st.info(f"Exactly {len(batches)} files created")

    except Exception as e:
        st.error(str(e))

# ---------- DOWNLOAD ----------
if st.session_state.zip_data:
    st.download_button(
        label="📦 Download split files (ZIP)",
        data=st.session_state.zip_data,
        file_name="concur_split_files.zip",
        mime="application/zip"
    )
