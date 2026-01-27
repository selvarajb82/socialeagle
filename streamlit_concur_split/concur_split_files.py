import streamlit as st
from collections import defaultdict
from io import BytesIO
import os

st.set_page_config(page_title="DAT File Splitter", page_icon="📂")

st.title("📂 DAT File Splitter (Key-Based)")

st.write(
    "Upload a DAT file and split it into multiple files based on **Column 19** "
    "while keeping the same key values together."
)

# === INPUTS ===
uploaded_file = st.file_uploader(
    "Upload .dat file",
    type=["dat", "txt"]
)

num_files = st.text_input(
    "Number of files to split into",
    value=""
)

# === PROCESSING ===
if uploaded_file and num_files:
    try:
        num_files = int(num_files)
        if num_files <= 0:
            st.error("Number of files must be greater than 0")
            st.stop()
    except ValueError:
        st.error("Please enter a valid number")
        st.stop()

    lines = uploaded_file.read().decode("utf-8").splitlines()
    column_index = 19  # same as your original script

    grouped_data = defaultdict(list)

    for line in lines:
        fields = line.split("|")
        if column_index < len(fields):
            key = fields[column_index].strip()
        else:
            key = "NO_KEY"

        grouped_data[key].append(line)

    unique_keys = list(grouped_data.keys())

    if num_files > len(unique_keys):
        st.error(
            "Number of output files cannot be greater than number of unique keys"
        )
        st.stop()

    # === Distribute groups across files ===
    output_buckets = [[] for _ in range(num_files)]

    for idx, key in enumerate(unique_keys):
        bucket_index = idx % num_files
        output_buckets[bucket_index].extend(grouped_data[key])

    st.success("File successfully split!")

    source_name = os.path.splitext(uploaded_file.name)[0]

    # === DOWNLOAD SECTION ===
    st.subheader("⬇️ Download Split Files")

    for i, bucket in enumerate(output_buckets, start=1):
        output_content = "\n".join(bucket)
        output_bytes = BytesIO(output_content.encode("utf-8"))

        st.download_button(
            label=f"Download {source_name}{i}.dat",
            data=output_bytes,
            file_name=f"{source_name}{i}.dat",
            mime="text/plain"
        )
