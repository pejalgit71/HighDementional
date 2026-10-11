import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from pandas.plotting import parallel_coordinates

# Load dataset manually from a CSV file instead of using sns.load_dataset
df = pd.read_csv('tips.csv')  # Replace with the local path to your CSV file

st.title("Examples of Advanced Data Visualizations")

# Example 1: Mosaic Plot (Marimekko)
with st.expander("Mosaic Plot (Marimekko)"):
    st.write("A **Mosaic Plot** (also known as a Marimekko or Mekko chart) is used to visualize categorical data in a two-dimensional space.")
    
    # Using plotly to simulate a Mekko-like plot
    fig_mekko = px.histogram(df, x="day", y="total_bill", color="sex", barmode="stack", histfunc="sum", height=400)
    fig_mekko.update_layout(yaxis_title="Total Bill")
    st.plotly_chart(fig_mekko)

# Example 2: Trellis Displays
with st.expander("Trellis Displays"):
    st.write("**Trellis Displays** are used to compare multiple subsets of data by using the same graphical representation across several small charts (also called 'small multiples').")

    # Creating trellis display using Altair
    trellis_chart = alt.Chart(df).mark_point().encode(
        x='total_bill',
        y='tip',
        color='sex',
        facet=alt.Facet('day:N', columns=2)
    )
    st.altair_chart(trellis_chart, use_container_width=True)

# Example 3: Heatmap
with st.expander("Heatmap"):
    st.write("A **Heatmap** is used to represent the intensity of values in a matrix-like format using different color intensities.")

    # Creating a heatmap using seaborn
    pivot_table = pd.pivot_table(df, values='total_bill', index='day', columns='time', aggfunc='mean')
    fig, ax = plt.subplots()
    sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", ax=ax)
    st.pyplot(fig)

# Example 4: Multivariate Scatter Plot
with st.expander("Multivariate Scatter Plot"):
    st.write("A **Multivariate Scatter Plot** visualizes relationships between more than two variables by using color, shape, and size dimensions.")

    scatter_plot = alt.Chart(df).mark_circle(size=60).encode(
        x='total_bill',
        y='tip',
        color='sex',
        size='size',
        tooltip=['total_bill', 'tip', 'sex', 'size']
    ).interactive()
    
    st.altair_chart(scatter_plot, use_container_width=True)

# Example 5: Parallel Coordinate Plot
with st.expander("Parallel Coordinate Plot"):
    st.write("A **Parallel Coordinate Plot** visualizes multidimensional data by drawing individual data points across several parallel axes.")

    df_parallel = df[['total_bill', 'tip', 'size', 'day']]
    df_parallel['day'] = pd.Categorical(df_parallel['day']).codes

    fig, ax = plt.subplots(figsize=(8, 6))
    parallel_coordinates(df_parallel, 'day', color=('#556270', '#4ECDC4', '#C7F464'))
    st.pyplot(fig)

# Example 6: Grand Tour (animated multidimensional scatter)
with st.expander("Grand Tour"):
    st.write("A **Grand Tour** is a technique that provides an animated visualization of high-dimensional data by smoothly rotating through different 2D projections of the data.")

    # Grand Tour using plotly express for high-dimensional data (3D as an example)
    fig = px.scatter_3d(df, x='total_bill', y='tip', z='size', color='sex')
    st.plotly_chart(fig)
