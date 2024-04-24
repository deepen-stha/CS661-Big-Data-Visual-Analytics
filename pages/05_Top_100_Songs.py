import streamlit as st
import pandas as pd
import plotly.express as px
from datasets import names
@st.cache_data
def load_data():
    data = pd.read_csv(names.TOP_100_SONGS_DATA)
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data = data.dropna(subset=['date'])
    data = data[(data['date'].dt.year >= 2013) & (data['date'].dt.year <= 2023)]
    return data

data = load_data()

st.title('Top 100 Songs Annually (2013-2023)')

# Sidebar for year selection
year_choice = st.sidebar.selectbox('Choose a Year:', range(2013, 2024))

# Filtering data based on selected year
yearly_data = data[data['date'].dt.year == year_choice]

# Group by track and artist, then get top 100 based on streams
top_songs = yearly_data.groupby(['name', 'artists']).agg({
    'streams': 'sum'
}).nlargest(100, 'streams').reset_index()

# st.write(f"Top 100 Songs in {year_choice}", top_songs)

# Visualization: Top songs by streams
fig = px.bar(top_songs, x='name', y='streams', hover_data=['artists'],
             title=f"Top 100 Songs by Streams in {year_choice}")
st.plotly_chart(fig)

# Visualization: Distribution of Streams per Artist
artist_streams = yearly_data.groupby('artists').agg({'streams': 'sum'}).reset_index()
fig2 = px.bar(artist_streams, x='artists', y='streams', title='Distribution of Streams per Artist')
st.plotly_chart(fig2)

# Visualization: Explicit vs Non-explicit Tracks
# explicit_count = yearly_data.groupby('explicit').agg({'streams': 'sum'}).reset_index()
# fig3 = px.pie(explicit_count, values='streams', names='explicit', title='Explicit vs Non-explicit Tracks')
# st.plotly_chart(fig3)

# Visualization: Average Song Duration per Year
avg_duration = data.groupby(data['date'].dt.year).agg({'duration': 'mean'}).reset_index()
fig4 = px.line(avg_duration, x='date', y='duration', title='Average Song Duration per Year')
st.plotly_chart(fig4)

# Optional: User selects a song to view its streaming trend
# song_list = yearly_data['name'].unique()
# selected_song = st.selectbox('Select a Song to View Streaming Trend:', song_list)
# song_data = yearly_data[yearly_data['name'] == selected_song]
# song_trend = song_data.groupby(song_data['date'].dt.month).agg({'streams': 'sum'}).reset_index()
# fig5 = px.line(song_trend, x='date', y='streams', title=f'Streaming Trend for {selected_song}')
# st.plotly_chart(fig5)

##############################################################

top_100_data = yearly_data[yearly_data['name'].isin(top_songs['name'])]
fig5 = px.scatter(top_100_data, x='duration', y='streams', hover_data=['name', 'artists'], title=f'Song Duration vs Streams for Top 100 Songs in {year_choice}')
st.plotly_chart(fig5)
