import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Function to extract HTML code from URL
def extract_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_code = response.text
            return html_code
        else:
            return "Error: Unable to retrieve HTML"
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit App
def main():
    st.title("Extract HTML Code from URLs")

    # File upload
    uploaded_file = st.file_uploader("Upload XLSX file", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        if 'SELLER_URL' in df.columns:
            # Remove duplicates from SELLER_URL column
            df.drop_duplicates(subset=['SELLER_URL'], inplace=True)

            # Add new column 'HTML' to store HTML code
            df['HTML'] = df['SELLER_URL'].apply(extract_html)

            # Display dataframe with HTML column
            st.write("Extracted HTML code from URLs:")
            st.write(df)

            # Export dataframe to XLSX
            export_file = st.button("Export to XLSX")
            if export_file:
                file_name = "output_with_html.xlsx"
                df.to_excel(file_name, index=False)
                st.success(f"File '{file_name}' exported successfully!")
        else:
            st.error("Column 'SELLER_URL' not found in the uploaded file.")

if __name__ == "__main__":
    main()
