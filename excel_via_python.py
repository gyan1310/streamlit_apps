import streamlit as st
import pandas as pd

st.title("Excel Data Filters App")

# Input fields for user-defined values
column_to_filter = st.text_input("Enter the column to filter:")
value_to_replace = st.text_input("Enter the value to replace:")

# File upload widget
uploaded_file = st.sidebar.file_uploader("Upload an Excel file")

# Check if a file has been uploaded
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
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
            st.warning("Please enter a valid column name.")

    if st.button("Replace Values"):
        if column_to_filter and value_to_replace:
            new_value = st.text_input("Enter the new value:")
            df = replace_values(df, column_to_filter, value_to_replace, new_value)
        else:
            st.warning("Please enter valid column and value.")

    if st.button("Find Min and Max"):
        if column_to_filter:
            min_val, max_val = find_min_max_values(df, column_to_filter)
            st.write(f"Minimum Value: {min_val}")
            st.write(f"Maximum Value: {max_val}")
        else:
            st.warning("Please enter a valid column name.")
            
    if df is not None:
        st.write("Filtered Data:")
        st.dataframe(df)
