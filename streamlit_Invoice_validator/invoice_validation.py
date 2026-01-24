import streamlit as st
import pandas as pd

st.set_page_config(page_title="AP Invoice Validator", page_icon="📄")

st.title("📄 AP Invoice Validation Dashboard")

st.write("Upload invoice data to validate before ERP processing.")

# File upload
uploaded_file = st.file_uploader(
    "Upload Invoice CSV",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Uploaded Data Preview")
    st.dataframe(df)

    # Mandatory columns
    required_columns = [
        "invoice_id",
        "supplier",
        "business_unit",
        "invoice_amount"
    ]

    st.subheader("🔍 Validation Results")

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        st.error(f"❌ Missing columns: {', '.join(missing_columns)}")
    else:
        # Validation logic
        df["error_reason"] = ""

        df.loc[df["supplier"].isna(), "error_reason"] += "Missing Supplier; "
        df.loc[df["business_unit"].isna(), "error_reason"] += "Missing Business Unit; "
        df.loc[df["invoice_amount"] <= 0, "error_reason"] += "Invalid Invoice Amount; "

        valid_df = df[df["error_reason"] == ""]
        error_df = df[df["error_reason"] != ""]

        col1, col2 = st.columns(2)

        with col1:
            st.success(f"✅ Valid Records: {len(valid_df)}")
            st.dataframe(valid_df)

        with col2:
            st.error(f"❌ Error Records: {len(error_df)}")
            st.dataframe(error_df)

        # Download error report
        if not error_df.empty:
            st.download_button(
                "⬇️ Download Error Report",
                error_df.to_csv(index=False),
                file_name="invoice_errors.csv",
                mime="text/csv"
            )
