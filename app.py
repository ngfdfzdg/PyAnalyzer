import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure outputs folder exists
if not os.path.exists("outputs"):
    os.makedirs("outputs")

class PyAnalyzer:
    def __init__(self, file_path):
        """Initialize with the path to the CSV file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        self.df = pd.read_csv(file_path)
        self.file_name = os.path.splitext(os.path.basename(file_path))[0]

    def generate_summary(self):
        """Generate and return a summary of the dataset."""
        summary = []
        summary.append(f"Dataset Summary for {self.file_name}:\n")
        summary.append(f"Shape: {self.df.shape}")
        summary.append(f"\nColumns: {list(self.df.columns)}")
        summary.append(f"\nData Types:\n{self.df.dtypes}")
        summary.append(f"\nMissing Values:\n{self.df.isnull().sum()}")
        summary.append(f"\nBasic Statistics:\n{self.df.describe()}")
        return "\n".join(summary)

    def plot_bar_chart(self, column, top_n=10, save=False):
        """Create a bar chart for a specified column."""
        if column not in self.df.columns:
            raise ValueError(f"Column {column} not found in dataset.")
        
        plt.figure(figsize=(10, 6))
        value_counts = self.df[column].value_counts().head(top_n)
        sns.barplot(x=value_counts.values, y=value_counts.index, palette='viridis')
        plt.title(f"Bar Chart of {column} (Top {top_n})")
        plt.xlabel("Count")
        plt.ylabel(column)
        plt.tight_layout()
        
        if save:
            plt.savefig(f"outputs/{self.file_name}_{column}_bar_chart.png")
        return plt.gcf()

    def plot_pie_chart(self, column, top_n=5, save=False):
        """Create a pie chart for a specified column."""
        if column not in self.df.columns:
            raise ValueError(f"Column {column} not found in dataset.")
        
        plt.figure(figsize=(8, 8))
        value_counts = self.df[column].value_counts().head(top_n)
        plt.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
        plt.title(f"Pie Chart of {column} (Top {top_n})")
        
        if save:
            plt.savefig(f"outputs/{self.file_name}_{column}_pie_chart.png")
        return plt.gcf()

    def plot_histogram(self, column, bins=10, save=False):
        """Create a histogram for a numerical column."""
        if column not in self.df.columns:
            raise ValueError(f"Column {column} not found in dataset.")
        if not pd.api.types.is_numeric_dtype(self.df[column]):
            raise ValueError(f"Column {column} must be numeric for histogram.")
        
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df[column], bins=bins, kde=True, color='skyblue')
        plt.title(f"Histogram of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.tight_layout()
        
        if save:
            plt.savefig(f"outputs/{self.file_name}_{column}_histogram.png")
        return plt.gcf()

# Streamlit app configuration
st.set_page_config(page_title="PyAnalyzer Dashboard", layout="wide")

# Title
st.title("PyAnalyzer: Power BI-like Data Analysis Dashboard")

# Sidebar for file selection
st.sidebar.header("Data Source")
data_folder = "data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
selected_file = st.sidebar.selectbox("Select a CSV file", ["Select a file"] + csv_files)

if selected_file != "Select a file":
    file_path = os.path.join(data_folder, selected_file)
    try:
        # Initialize PyAnalyzer
        analyzer = PyAnalyzer(file_path)

        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["Data Summary", "Visualizations", "Data Table"])

        # Tab 1: Data Summary
        with tab1:
            st.header("Dataset Summary")
            with st.expander("View Summary"):
                summary = analyzer.generate_summary()
                st.text(summary)
                st.write(f"**Shape**: {analyzer.df.shape}")
                st.write(f"**Columns**: {list(analyzer.df.columns)}")
                st.write("**Data Types**:")
                st.write(analyzer.df.dtypes)
                st.write("**Missing Values**:")
                st.write(analyzer.df.isnull().sum())

        # Tab 2: Visualizations
        with tab2:
            st.header("Visualizations")
            column = st.selectbox("Select a column for visualizations", analyzer.df.columns)
            top_n = st.slider("Top N categories for bar/pie charts", 5, 20, 10)
            save_plots = st.checkbox("Save visualizations to outputs/")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"Bar Chart: {column}")
                fig = analyzer.plot_bar_chart(column, top_n=top_n, save=save_plots)
                st.pyplot(fig)
                plt.close(fig)

            with col2:
                st.subheader(f"Pie Chart: {column}")
                fig = analyzer.plot_pie_chart(column, top_n=top_n, save=save_plots)
                st.pyplot(fig)
                plt.close(fig)

            if pd.api.types.is_numeric_dtype(analyzer.df[column]):
                st.subheader(f"Histogram: {column}")
                bins = st.slider("Number of bins", 5, 50, 10)
                fig = analyzer.plot_histogram(column, bins=bins, save=save_plots)
                st.pyplot(fig)
                plt.close(fig)

        # Tab 3: Data Table
        with tab3:
            st.header("Data Table")
            st.write("Explore the raw data with sorting and filtering.")
            sort_column = st.selectbox("Sort by column", analyzer.df.columns)
            sort_order = st.radio("Sort order", ["Ascending", "Descending"])
            filter_column = st.selectbox("Filter by column", analyzer.df.columns)
            filter_value = st.text_input(f"Enter value to filter {filter_column}")

            # Apply sorting and filtering
            df_display = analyzer.df.copy()
            if filter_value:
                df_display = df_display[df_display[filter_column].astype(str).str.contains(filter_value, case=False, na=False)]
            if sort_order == "Ascending":
                df_display = df_display.sort_values(by=sort_column)
            else:
                df_display = df_display.sort_values(by=sort_column, ascending=False)

            st.dataframe(df_display)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please select a CSV file to begin.")