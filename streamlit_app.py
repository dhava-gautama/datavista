# Import Libraries
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
def load_data(file_path):
    try:
        if file_path.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file_path.type == 'application/vnd.ms-excel':
            data = pd.read_excel(file_path)
        elif file_path.type == 'text/csv':
            data = pd.read_csv(file_path)
        else:
            st.error('File type not supported. Please upload a CSV or Excel file.'+ file_path.type)
            return None
        # Autoparse time variables
        time_variable = ['date', 'time', 'datetime', 'timestamp', 'waktu']
        for col in data.columns:
            if any(name in col.lower() for name in time_variable):
                data[col] = pd.to_datetime(data[col], dayfirst=True, errors='coerce')
                # set time variable as index
                data.set_index(col, inplace=True)
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
    # let user choose to display the data head or tail.
    head_or_tail = st.selectbox('Display head or tail of the data', ['Head', 'Tail'])
    if head_or_tail == 'Head':
        st.dataframe(data.head(row_to_show))
    else:
        st.dataframe(data.tail(row_to_show))

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
    st.set_page_config(layout="wide")
    st.title("Data Visualization App")
    # Sidebar
    with st.sidebar:
        st.subheader("Upload Data")
        st.write("Please upload a CSV or Excel file.")
        file_path = st.file_uploader("Upload CSV or Excel file", type=["csv", "xls", "xlsx"],
                                     accept_multiple_files=False)
    # Main
    if file_path is not None:
        data = load_data(file_path)
        if data is not None:
            display_dynamic_table(data)
            visualize_data(data)


if __name__ == "__main__":
    main()
