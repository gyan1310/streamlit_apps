import streamlit as st
import pandas as pd

st.title("Excel Data Filters App")

# File upload widget
uploaded_file = st.sidebar.file_uploader("Upload an Excel file")

# Check if a file has been uploaded
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # Get a list of column names from the DataFrame
    columns_list = df.columns.tolist()
    
    # Create a selectbox widget for selecting the column
    column_to_filter = st.selectbox("Select a column to filter:", columns_list)

    value_to_replace = st.text_input("Enter the value to replace:")

    def remove_none_values(df, column):
        df = df.dropna(subset=[column])
        return df

    def replace_values(df, column, old_value, new_value):
        df[column] = df[column].replace(old_value, new_value)
        return df

    def find_min_max_values(df, column):
        min_value = df[column].min()
        max_value = df[column].max()
        return min_value, max_value
    
    if st.button("Remove None Values"):
        if column_to_filter:
            df = remove_none_values(df, column_to_filter)
        else:
            st.warning("Please select a valid column.")

    if st.button("Replace Values"):
        if column_to_filter and value_to_replace:
            new_value = st.text_input("Enter the new value:")
            df = replace_values(df, column_to_filter, value_to_replace, new_value)
        else:
            st.warning("Please select a valid column and enter a value to replace.")

    if st.button("Find Min and Max"):
        if column_to_filter:
            min_val, max_val = find_min_max_values(df, column_to_filter)
            st.write(f"Minimum Value: {min_val}")
            st.write(f"Maximum Value: {max_val}")
        else:
            st.warning("Please select a valid column.")
            
    if df is not None:
        st.write("Filtered Data:")
        st.dataframe(df)
