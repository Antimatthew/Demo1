import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Explorer", layout="centered")
st.title("CSV File Explorer")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of Data")
    st.dataframe(df.head(20))

    st.subheader("Summary Statistics")
    st.write(df.describe(include='all'))

    st.subheader("Column Chart Preview")
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) > 0:
        chart_col = st.selectbox("Select numeric column to chart", numeric_cols)
        st.line_chart(df[chart_col])
    else:
        st.info("No numeric columns found to chart.")
else:
    st.info("Please upload a CSV file to get started.")
