# Import Libraries
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
def load_data(file_path):
    try:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            data = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        else:
            st.error('File type not supported')
            return None
        return data
    except Exception as e:
        st.error(f'Error: {e}')
        return None

# Displaying data info
def display_data_info(data):
    st.subheader('Data Info')
    st.write(data.info())

# Displaying dynamic table for data preview
def display_dynamic_table(data):
    st.subheader('Data Preview')
    row_to_show = st.slider('Select number of rows to show', min_value=1, max_value=len(data), value=10)
    st.dataframe(data.head(row_to_show))

# Data visualization
def visualize_data(data):
    st.subheader('Data Visualization')
    chart_type = st.selectbox("Select chart type", ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"])

    if chart_type == "Bar Chart":
        variable = st.selectbox("Select variable for x-axis", data.columns)
        st.bar_chart(data[variable])
    elif chart_type == "Line Chart":
        variable = st.selectbox("Select variable for x-axis", data.columns)
        st.line_chart(data[variable])
    elif chart_type == "Scatter Plot":
        x_variable = st.selectbox("Select variable for x-axis", data.columns)
        y_variable = st.selectbox("Select variable for y-axis", data.columns)
        fig, ax = plt.subplots()
        sns.scatterplot(x=x_variable, y=y_variable, data=data)
        st.pyplot(fig)
    elif chart_type == "Histogram":
        variable = st.selectbox("Select variable for histogram", data.columns)
        fig, ax = plt.subplots()
        sns.histplot(data[variable], ax=ax)
        st.pyplot(fig)

# Main function
def main():
    st.title("Data Visualization App")
    file_path = st.file_uploader("Upload CSV or Excel file", type=["csv", "xls", "xlsx"], accept_multiple_files=False)

    if file_path is not None:
        data = load_data(file_path)
        if data is not None:
            display_dynamic_table(data)
            visualize_data(data)


if __name__ == "__main__":
    main()