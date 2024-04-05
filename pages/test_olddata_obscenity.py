import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from time import sleep















#adjust window size













# Load data
data = pd.read_csv('tcc_ceds_music.csv')

# Streamlit app
st.title('Visualization of Average Obscenity Over the Years')
# st.title('Visualization of Average Obscenity and Instrumentalness Over the Years')

# Calculate average obscenity and instrumentalness for each year
average_obscenity = data.groupby('release_date')['obscene'].mean().reset_index()
average_instrumentalness = data.groupby('release_date')['instrumentalness'].mean().reset_index()

# Determine y-axis range
y_min = min(average_obscenity['obscene'].min(), average_instrumentalness['instrumentalness'].min())
y_max = max(average_obscenity['obscene'].max(), average_instrumentalness['instrumentalness'].max())
y_range = [max(0, y_min - 0.1), min(1, y_max )]

# Create plot
fig = go.Figure()

# Add traces
fig.add_trace(
    go.Scatter(
        x=[],
        y=[],
        mode='lines',
        # line=dict(color='gold', width=1.5, shape='spline'),
        line=dict(color='royalblue', width=1.5, shape='spline'),
        name='Average Obscenity',
        opacity=0.7
    )
)

# fig.add_trace(
#     go.Scatter(
#         x=[],
#         y=[],
#         mode='lines',
#         line=dict(color='royalblue', width=1.5, shape='spline'),
#         name='Average Instrumentalness',
#         opacity=0.7
#     )
# )

# Update layout
fig.update_layout(
    xaxis=dict(title='Release Date', dtick=10),  # Adjust tick frequency on x-axis for better readability
    yaxis=dict(title='Value', range=y_range),  # Set dynamic range for y-axis
    # title='Visualization of Average Obscenity and Instrumentalness Over the Years',
    title='Visualization of Average Obscenity Over the Years',
    font=dict(family='Arial', size=14, color='black'),
    plot_bgcolor='rgba(255, 255, 255, 0)',  # Set transparent background
    paper_bgcolor='rgba(255, 255, 255, 0)',  # Set transparent background for the entire plot area
)

# Display the plot
plot = st.plotly_chart(fig)

# Animate drawing of the graph
for i in range(len(average_obscenity)):
    with plot:
        sleep(0.1)
        fig.data[0]['x'] = average_obscenity['release_date'][:i+1]
        fig.data[0]['y'] = average_obscenity['obscene'][:i+1]
        # fig.data[1]['x'] = average_instrumentalness['release_date'][:i+1]
        # fig.data[1]['y'] = average_instrumentalness['instrumentalness'][:i+1]
        plot.plotly_chart(fig, use_container_width=True)
