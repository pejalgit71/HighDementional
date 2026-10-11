import streamlit as st
import pandas as pd
import altair as alt

# Sample Data for visualization
data = {
    'Age': [25, 32, 40, 50, 28, 45, 36, 23, 31, 27, 33, 41],
    'Income': [35000, 42000, 60000, 80000, 37000, 75000, 54000, 30000, 48000, 36000, 51000, 61000],
    'Education': ['High School', 'Bachelors', 'Masters', 'PhD', 'High School', 'Masters', 'Bachelors', 
                  'High School', 'Bachelors', 'High School', 'Bachelors', 'Masters'],
    'Occupation': ['Engineer', 'Doctor', 'Artist', 'Scientist', 'Teacher', 'Engineer', 'Artist', 
                   'Scientist', 'Doctor', 'Teacher', 'Engineer', 'Scientist']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Exploratory Graphics (Scatter Plot for Age vs Income)
st.title("Exploratory Graphics vs Presentation Graphics")

st.header("Exploratory Graphics: Interactive Scatter Plot")
scatter_chart = alt.Chart(df).mark_circle(size=60).encode(
    x='Age',
    y='Income',
    color='Education',
    tooltip=['Age', 'Income', 'Education', 'Occupation']
).interactive()

st.altair_chart(scatter_chart, use_container_width=True)

st.write("This scatter plot is an example of exploratory graphics, where you can hover over data points to explore details interactively.")

# Presentation Graphics (Static Bar Chart for Total Income by Education Level)
st.header("Presentation Graphics: Static Bar Chart")
bar_chart = alt.Chart(df).mark_bar().encode(
    x='Education',
    y='sum(Income)',
    color='Education'
)

st.altair_chart(bar_chart, use_container_width=True)

st.write("This static bar chart is an example of presentation graphics, conveying a simple message without interactivity.")

# Interactive Linked Highlighting for High-Dimensional Data
st.header("Interactive Linked Highlighting for High-Dimensional Data")

# Linked charts: Scatter plot and bar chart
highlight = alt.selection(type='single', on='mouseover', fields=['Education'], nearest=True)

scatter_chart_linked = alt.Chart(df).mark_circle(size=60).encode(
    x='Age',
    y='Income',
    color=alt.condition(highlight, 'Education', alt.value('lightgray')),
    tooltip=['Age', 'Income', 'Education', 'Occupation']
).add_selection(
    highlight
)

bar_chart_linked = alt.Chart(df).mark_bar().encode(
    x='Education',
    y='sum(Income)',
    color=alt.condition(highlight, 'Education', alt.value('lightgray'))
)

# Combine the scatter and bar charts
linked_charts = scatter_chart_linked | bar_chart_linked

st.altair_chart(linked_charts, use_container_width=True)

st.write("Here, hovering over any education level in either chart will highlight relevant data points in the other chart, showing relationships between variables interactively.")

# Appropriate Graphics for Certain Variables with Linked Context
st.header("Finding Appropriate Graphics and Linking Multivariate Context")

occupation_bar = alt.Chart(df).mark_bar().encode(
    x='Occupation',
    y='count()',
    color='Education',
    tooltip=['Occupation', 'Education', 'count()']
).interactive()

st.altair_chart(occupation_bar, use_container_width=True)

st.write("This bar chart shows how to find the most appropriate graphic (a count bar chart for occupation) while preserving the context of education level as a linked variable.")
