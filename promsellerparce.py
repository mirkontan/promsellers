import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Function to extract HTML code from URL
def extract_html(url, counter):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_code = response.text
            counter += 1
            return html_code, counter
        else:
            return "Error: Unable to retrieve HTML", counter
    except Exception as e:
        return f"Error: {str(e)}", counter

# Function to extract shop name from HTML code
def extract_shop_name(html_code):
    try:
        soup = BeautifulSoup(html_code, 'html.parser')
        shop_name_element = soup.find('h1', class_='_3Trjq')
        if shop_name_element:
            return shop_name_element.text.strip()
        else:
            # Attempt to extract company name from alternative section
            company_name_element = soup.find('a', class_='_0cNvO')
            if company_name_element:
                return company_name_element.text.strip()
            else:
                return "Shop name not found"
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
            # Count the number of rows before removing duplicates
            st.write(f"Number of rows before removing duplicates: {len(df)}")

            # Remove duplicates from SELLER_URL column
            df.drop_duplicates(subset=['SELLER_URL'], inplace=True)

            # Count the number of rows after removing duplicates
            st.write(f"Number of rows after removing duplicates: {len(df)}")

            # Add new column 'HTML' to store HTML code
            df['HTML'] = ''
            counter_text = st.empty()
            counter = 0

            for index, row in df.iterrows():
                url = row['SELLER_URL']
                html_code, counter = extract_html(url, counter)
                df.at[index, 'HTML'] = html_code
                counter_text.text(f"URLs processed: {counter}/{len(df)}")

            # Add new column 'Shop Name' to store shop names
            df['Shop Name'] = df['HTML'].apply(extract_shop_name)

            # Display dataframe with Shop Name column
            st.write("Extracted Shop Names from URLs:")
            st.write(df[['SELLER_URL', 'Shop Name']])

            # Export dataframe to XLSX
            export_file = st.button("Export to XLSX")
            if export_file:
                file_name = "output_with_shop_names.xlsx"
                df.to_excel(file_name, index=False)
                st.success(f"File '{file_name}' exported successfully!")
        else:
            st.error("Column 'SELLER_URL' not found in the uploaded file.")

if __name__ == "__main__":
    main()
