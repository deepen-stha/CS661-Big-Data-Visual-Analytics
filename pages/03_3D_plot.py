import streamlit as st
import pandas as pd
import plotly.express as px

from datasets import names

# Function to load data
@st.cache_data
def load_data():
    data = pd.read_csv(names.SPOTIFY_DATA)
    return data

# Load data
data = load_data()

# Streamlit webpage title
st.title('Music Tracks Data Visualization')

# Sidebar for user input features
st.sidebar.header('Filters')

# Filter by Genre
selected_genre = st.sidebar.selectbox('Genre', options=['All'] + list(data['track_genre'].unique()))
if selected_genre != 'All':
    data = data[data['track_genre'] == selected_genre]

# Filter by Artist
selected_artist = st.sidebar.selectbox('Artist', options=['All'] + list(data['artists'].unique()))
if selected_artist != 'All':
    data = data[data['artists'] == selected_artist]

# Filter by Popularity
popularity_range = st.sidebar.slider('Popularity Range', int(data['popularity'].min()), int(data['popularity'].max()), (50, 100))
data = data[(data['popularity'] >= popularity_range[0]) & (data['popularity'] <= popularity_range[1])]

# Filter by Explicit Content
explicit_content = st.sidebar.radio('Explicit Content', options=['All', 'Yes', 'No'])
if explicit_content == 'Yes':
    data = data[data['explicit'] == 1]
elif explicit_content == 'No':
    data = data[data['explicit'] == 0]

# Main page
st.header('Track Information')
st.write('Displaying tracks filtered by selected criteria.')

# Plotting the data in a 3D scatter plot
fig = px.scatter_3d(data, x='danceability', y='energy', z='popularity',
                    color='popularity', hover_data=['track_name', 'artists'])
st.plotly_chart(fig)
# Run this with `streamlit run your_script_name.py`
