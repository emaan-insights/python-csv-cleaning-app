
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CSV Cleaning App",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CSV Data Cleaning App")
st.sidebar.title("CSV Cleaner")
st.sidebar.write("Upload, clean and download your data.")
st.sidebar.info("Your data cleaning workspace")


st.markdown(
    "Clean, explore and prepare your CSV datasets easily."
)

st.divider()


uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:

    if ("df" not in st.session_state or
        st.session_state.get("uploaded_file_name") != uploaded_file.name):

        original_df = pd.read_csv(uploaded_file)

        st.session_state.original_df = original_df.copy()
        st.session_state.df = original_df.copy()
        st.session_state.uploaded_file_name = uploaded_file.name

    if st.button("Reset Dataset"):
        st.session_state.df = st.session_state.original_df.copy()
        st.success("Dataset restored to original version!")
        st.dataframe(st.session_state.df)

    df = st.session_state.df

    st.subheader("Uploaded Data")
    st.dataframe(df)

    st.subheader("Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Rows", df.shape[0])

    with col2:
        st.metric("Total Columns", df.shape[1])

    st.subheader("Missing Values")
    st.write(df.isnull().sum())
    if st.button("Remove Rows with Missing Values"):
        st.session_state.df = st.session_state.df.dropna()
        st.success("Rows with missing values removed successfully!")
    if st.button("Fill Missing Values with 0"):
        st.session_state.df = st.session_state.df.fillna(0)
        st.success("Missing values filled successfully!")
        st.subheader("Missing Values After Cleaning")
        st.write(st.session_state.df.isnull().sum())

        st.subheader("Select Columns")

    selected_columns = st.multiselect(
        "Choose columns to keep:",
        st.session_state.df.columns.tolist(),
        default=st.session_state.df.columns.tolist()
    )

    if st.button("Apply Column Selection"):
        st.session_state.df = st.session_state.df[selected_columns]
        st.success("Column selection applied!")
        st.dataframe(st.session_state.df)

    st.subheader("Duplicate Records")
    st.write("Total Duplicate Rows:", df.duplicated().sum())

    if st.button("Remove Duplicate Rows"):
        st.session_state.df = df.drop_duplicates()
        st.success("Duplicate rows removed successfully!")

    if st.button("Clean Column Names"):
        df = st.session_state.df.copy()

        df.columns = df.columns.str.strip().str.replace(
            r'(?<!^)(?=[A-Z])', '_', regex=True
        ).str.lower()

        st.session_state.df = df
        st.success("Column names cleaned successfully!")

    st.subheader("Updated Dataset")
    st.dataframe(st.session_state.df)

    csv = st.session_state.df.to_csv(index=False)

    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )