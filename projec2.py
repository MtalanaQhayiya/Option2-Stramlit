import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Set Streamlit page config
st.set_page_config(page_title="Ages by Country and Gender", layout="wide")

# Title
st.title("📊 Individual Ages by Country and Gender")

# Load the dataset
try:
    df = pd.read_csv("country_data.csv")
except FileNotFoundError:
    st.error("❌ File 'country_data.csv' not found in the working directory.")
    st.stop()

# Clean whitespace
df.columns = df.columns.str.strip()
df['Country'] = df['Country'].str.strip()
df['Gender'] = df['Gender'].str.strip()

# Set colors for genders
color_map = {'M': 'blue', 'F': 'red'}
df['Color'] = df['Gender'].map(color_map)

# Sidebar filters
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Select countries to display",
    options=sorted(df['Country'].unique()),
    default=sorted(df['Country'].unique())
)
selected_genders = st.sidebar.multiselect(
    "Select gender(s)",
    options=['M', 'F'],
    default=['M', 'F']
)

# Filter data
filtered_df = df[df['Country'].isin(selected_countries) & df['Gender'].isin(selected_genders)]

# Sort for consistent layout
filtered_df = filtered_df.sort_values(by=["Country", "Gender"])

# Plotting
fig, ax = plt.subplots(figsize=(14, 6))

bar_width = 0.4
spacing = 1.0
x_positions = []
x_labels = []

x = 0
for country in filtered_df['Country'].unique():
    group = filtered_df[filtered_df['Country'] == country]
    for i, row in group.iterrows():
        ax.bar(x, row['Age'], color=row['Color'], width=bar_width)
        x_labels.append(f"{country}\n{row['Gender']}")
        x_positions.append(x)
        x += spacing

# Set labels and legend
ax.set_title("Individual Ages by Country and Gender")
ax.set_ylabel("Age")
ax.set_xticks(x_positions)
ax.set_xticklabels(x_labels, rotation=45, ha="right")
ax.legend(
    handles=[
        plt.Rectangle((0, 0), 1, 1, color='blue', label='Male'),
        plt.Rectangle((0, 0), 1, 1, color='red', label='Female')
    ],
    title="Gender"
)

st.pyplot(fig)

# Optional data view
with st.expander("🔎 View Filtered Data Table"):
    st.dataframe(filtered_df.reset_index(drop=True))






