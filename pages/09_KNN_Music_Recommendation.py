import streamlit as st
import pandas as pd
import pandasql as psql
from sklearn.neighbors import NearestNeighbors
import seaborn as sns
from datasets import names

# Custom color palette for plots
sns.set_palette("pastel")

# Title of the app
st.title('🎵 Music Insights and Recommendation Simulator')

# Customize the background and text
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .stApp {
        background-image: url("https://images.pexels.com/photos/1389429/pexels-photo-1389429.jpeg");
        background-attachment: fixed;
        background-size: cover;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = pd.read_csv(names.SPOTIFY_DATA)
    features = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    data[features] = (data[features] - data[features].min()) / (data[features].max() - data[features].min())
    return data

data = load_data()

# Sidebar for options
st.sidebar.header('Set Your Preferences')

# User preferences input for recommendation
st.sidebar.subheader('Music Preferences for Recommendation')
user_preferences = {}
for feature in ['danceability', 'energy', 'valence', 'tempo']:
    user_preferences[feature] = st.sidebar.slider(f'{feature.capitalize()}', 0.0, 1.0, 0.5, 0.01)

# Input for number of recommendations min value will be 2 max value will be 6 and default value is 5
number_of_recommendations = st.sidebar.number_input('Number of Tracks to Recommend', min_value=2, max_value=6, value=5)

# Recommendation function using nearest neighbors
def recommend_tracks(preferences, data, n_recommendations=5):
    user_df = pd.DataFrame([preferences])
    neighbors = NearestNeighbors(n_neighbors=n_recommendations, algorithm='ball_tree')
    neighbors.fit(data[list(preferences.keys())])
    distances, indices = neighbors.kneighbors(user_df)
    return data.iloc[indices[0]]

# SQL Query Input
st.sidebar.subheader('SQL Query for Data Filtering')
user_query = st.sidebar.text_area("Write your SQL query here (use 'data' as table name):", 'SELECT * FROM data LIMIT 10')

# Execute SQL Query
query_results = None
if st.sidebar.button('Execute SQL Query'):
    try:
        query_results = psql.sqldf(user_query, locals())
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}")

# Display SQL query results
if query_results is not None:
    st.write(query_results)

# Display recommendations based on user preferences
st.subheader('🎧 Track Recommendations Based on Your Preferences')
if st.button('Recommend Tracks'):
    recommended_tracks = recommend_tracks(user_preferences, data, n_recommendations=number_of_recommendations)
    st.write(recommended_tracks[['artists', 'track_name', 'album_name'] + list(user_preferences.keys())])

    # Display audio features of recommended tracks using seaborn pairplot
    st.subheader('Audio Features of Recommended Tracks')
    pairplot_data = recommended_tracks[['danceability', 'energy', 'valence', 'tempo']]
    pairplot_fig = sns.pairplot(pairplot_data)
    st.pyplot(pairplot_fig)
