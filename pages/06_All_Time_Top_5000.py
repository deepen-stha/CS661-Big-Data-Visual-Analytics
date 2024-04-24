import streamlit as st
import pandas as pd
import plotly.express as px
from datasets import names

# Load the preprocessed data
@st.cache_data
def load_data():
    # Load the dataset
    data = pd.read_csv(names.SPOTIFY_DATA)
    
    # Removing duplicates: assuming a combination of 'track_name' and 'artists' makes a song unique
    data = data.drop_duplicates(subset=['track_name', 'artists'])
    
    # Return the top 5000 unique songs in each genre based on popularity
    return data.groupby('track_genre').apply(
        lambda x: x.nlargest(5000, 'popularity')).reset_index(drop=True)

data = load_data()

# Streamlit page configuration
st.title('All time Top-5000  Songs by Genre')
st.sidebar.title("Settings")

# Sidebar for genre selection
genre_list = data['track_genre'].unique()
genre_choice = st.sidebar.selectbox('Choose a Genre:', genre_list)

# Filtering data based on selected genre
filtered_data = data[data['track_genre'] == genre_choice]

# Display the filtered data
# st.write(f"All time Top-5000  Songs in Genre: {genre_choice}")
# st.dataframe(filtered_data[['track_name', 'artists', 'popularity']])

# Visualization of popularity vs danceability
fig = px.scatter(filtered_data, x='popularity', y='danceability', color='energy',
                 hover_name='track_name', title=f"Popularity vs Danceability for {genre_choice} Genre")
st.plotly_chart(fig)

# Scatter plot for tempo vs valence
fig2 = px.scatter(filtered_data, x='tempo', y='valence', size='popularity', color='liveness',
                 hover_name='track_name', title=f"Tempo vs Valence for {genre_choice} Genre")
st.plotly_chart(fig2)

# Bar chart for energy vs loudness
fig3 = px.bar(filtered_data, x='energy', y='loudness', color='danceability',
              title=f"Energy vs Loudness for {genre_choice} Genre")
st.plotly_chart(fig3)

# Scatter plot for acousticness vs speechiness
fig4 = px.scatter(filtered_data, x='acousticness', y='speechiness', color='valence',
                  hover_name='track_name', title=f"Acousticness vs Speechiness for {genre_choice} Genre")
st.plotly_chart(fig4)

# Select Features to Compare - simplified to bar plots if applicable
features = st.sidebar.multiselect('Select Features to Compare:', ['energy', 'danceability', 'loudness', 'valence', 'tempo'], default=['energy', 'danceability'])
if len(features) == 2:
    # Bar chart comparison for two selected features
    fig_features = px.bar(filtered_data, x=features[0], y=features[1], color='popularity',
                          title="Feature Comparison")
    st.plotly_chart(fig_features)
