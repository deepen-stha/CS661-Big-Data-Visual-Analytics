# %%
import streamlit as st
import pandas as pd
import plotly.express as px

# %%
# Load data
data = pd.read_csv('dataset1.csv') # WARNING: large dataset (integration put on hold)

# %%
# # Sort the data according to weeks
# data = data.sort_values('week')

# %%
# # Convert 'streams' column to numeric type
# data['streams'] = pd.to_numeric(data['streams'], errors='coerce')

# %%
data[:1000]['track_name']

# %%
# Sample 1/50 of the data
data = data[:int(data.shape[0]/10)]

# %%
data['week']

# %%
# Streamlit app
st.title('Bubble Chart of Top 10 Music Genres by Total Streams (Per Week)')

# %%
# Function to keep only top 10 genres for each week
# def keep_top_10_genres(group):
#     return group.nlargest(10, 'streams')
def keep_top_10_genres(group):
    return group.nlargest(10, 'sum_streams')  # Use 'sum_streams' instead of 'streams'

# %%
data['week'] = pd.to_datetime(data['week'], format='%d-%m-%Y')

# %%
def aggregate_data(group):
    sum_streams = group['streams'].sum()
    avg_instrumentalness = group['instrumentalness'].mean()
    return pd.Series({'sum_streams': sum_streams, 'avg_instrumentalness': avg_instrumentalness})

# Apply the custom aggregation function
data_aggregated = data.groupby(['week', 'artist_genre']).apply(aggregate_data).reset_index()

# Apply the function to keep only top 10 genres for each week
data_aggregated_top_10 = data_aggregated.groupby('week').apply(keep_top_10_genres).reset_index(drop=True)

# %%
# data_top_10 = data.groupby(['week', 'artist_genre']).agg({'streams': 'sum'}).reset_index()

# %%
# num_streams_genre_0 = [data_top_10[data_top_10['artist_genre'] == '0']['streams']]

# %%
# num_streams_genre_0

# %%
# Apply the function to keep only top 10 genres for each week
# data_top_10 = data_top_10.groupby('week').apply(keep_top_10_genres).reset_index(drop=True)

# %%
# data_top_10 = data.groupby(['week', 'artist_genre']).agg({'streams': 'sum'}).reset_index()

# %%
data_top_10 = data_aggregated_top_10

# %%
data_top_10['lang']=''

# %%
data_top_10_temp = data.groupby(['week', 'artist_genre', 'instrumentalness']).agg({'streams': 'sum'}).reset_index()

# %%
most_used_instrumentalness_temp =data_top_10_temp.groupby(['week', 'artist_genre']).apply(lambda x: x.loc[x['streams'].idxmax()])[['artist_genre', 'instrumentalness']].reset_index(drop=True)


# %%
most_used_instrumentalness_temp

# %%
data_top_10

# %%
data_top_10['lang'] = data_top_10_temp['instrumentalness']

import numpy as np
# data_top_10['streams'] = data_top_10['streams']/np.max(data_top_10['streams'])
# scaled_streams = np.array(data_top_10['streams']) / np.max(data_top_10['streams'])  # Example normalization
# %%
data_top_10

# %%
# Bubble chart using Plotly Express
# fig = px.scatter(data_top_10, x='week', y='artist_genre', size='streams', color='artist_genre',
#                  title='Bubble Chart of Top 10 Music Genres by Total Streams (Per Week)',
#                  labels={'week': 'Week', 'streams': 'Total Streams'}, width=1000, height=600)
# fig.update_layout(plot_bgcolor='rgba(255, 255, 255, 0)',  # Set transparent background
#                   paper_bgcolor='rgba(255, 255, 255, 0)',  # Set transparent background for the entire plot area
#                   font=dict(family='Arial', size=14, color='black'))
# fig.update_xaxes(title_font=dict(size=16, color='black'))
# fig.update_yaxes(title_font=dict(size=16, color='black'))

# # Display the plot
# st.plotly_chart(fig)


fig = px.scatter_3d(data_top_10, x='week', y='artist_genre', z='avg_instrumentalness', size='sum_streams', color='artist_genre',
                    title='3D Bubble Chart of Top 10 Music Genres by Total Streams (Per Week)',
                    labels={'week': 'Week', 'artist_genre': 'Genre', 'avg_instrumentalness': 'Language', 'sum_streams': 'Total Streams'},
                    width=1000, height=1000)

# fig.update_traces(marker=dict(symbol='circle', line=dict(width=2, color='DarkSlateGrey'), size_max=100),
#                   selector=dict(mode='markers'), 
#                   marker_size=data_top_10['streams'].apply(lambda x: x / 500))  # Adjust the scale factor as desired

fig.update_layout(plot_bgcolor='rgba(255, 255, 255, 0)',  # Set transparent background
                  paper_bgcolor='rgba(255, 255, 255, 0)',  # Set transparent background for the entire plot area
                  font=dict(family='Arial', size=10, color='white'),
                  xaxis_showgrid = False,
                   yaxis_showgrid = False,
                    # zaxis_showgrid = False,
                      )
fig.update_xaxes(title_font=dict(size=10, color='black'))
fig.update_yaxes(title_font=dict(size=10, color='black'))
fig.update_scenes(zaxis_title_text='Instrumentalness')  # Update the title of the z-axis

# Display the plot
st.plotly_chart(fig)





