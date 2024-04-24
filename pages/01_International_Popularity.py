import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from datasets import names

@st.cache_data
def load_data():
    return pd.read_csv(names.INTERNATIONAL_POPULARITY_DATA)

# Load data
data = load_data()


# Streamlit app
st.title('Popular Genres and Artists by Country')

# Select country
selected_country = st.selectbox('Select a country:', data['country'].unique())

# Select number of top genres to display
m = st.slider('Select the number of top genres:', min_value=1, max_value=10, value=7)

# Select number of top artists to display for each genre
k = st.slider('Select the number of top artists for each genre:', min_value=1, max_value=10, value=7)

# Filter data for the selected country
data_country = data[data['country'] == selected_country]

# Group data by genre and artist, then calculate total streams
data_grouped = data_country.groupby(['artist_genre', 'artist_individual']).agg({'streams': 'sum'}).reset_index()

# Exclude genre '0'
data_grouped = data_grouped[data_grouped['artist_genre'] != '0']

# Keep only the top m genres based on total streams
top_genres = data_grouped.groupby('artist_genre').agg({'streams': 'sum'}).nlargest(m, 'streams').index

# Filter data to keep only the top m genres
data_filtered = data_grouped[data_grouped['artist_genre'].isin(top_genres)]

# Keep only the top k artists for each genre
top_artists = data_filtered.groupby('artist_genre').apply(lambda x: x.nlargest(k, 'streams')).reset_index(drop=True)
top_artists['country'] = selected_country

# Plot sunburst using go
id1=[selected_country]
labels1 = [selected_country]
parents1 = ['']
values1 = [top_artists['streams'].sum()]
for i in range(len(list(set(top_artists['artist_genre'])))):
    id1.append(list(set(top_artists['artist_genre']))[i])
    labels1.append(list(set(top_artists['artist_genre']))[i])
    parents1.append(selected_country)
    values1.append(top_artists[top_artists['artist_genre'] == list(set(top_artists['artist_genre']))[i]]['streams'].sum())
for i in range(len(top_artists)):
    parent_value = top_artists[top_artists['artist_genre'] == top_artists['artist_genre'][i]]['streams'].sum()
    child_value = top_artists['streams'][i]
    scale_factor = parent_value / child_value if child_value != 0 else 0
    id1.append(top_artists['artist_genre'][i]+top_artists['artist_individual'][i])
    labels1.append(top_artists['artist_individual'][i])
    parents1.append(top_artists['artist_genre'][i])
    values1.append(child_value)
# average_score = top_artists['streams'].sum() / k
fig = go.Figure()
fig.add_trace(go.Sunburst(
    ids=id1,
    labels=labels1,
    parents=parents1,
    values=values1,
    maxdepth=2,
    branchvalues='total',
    insidetextorientation='auto',
    marker = dict(colorscale = 'twilight')#Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd
    # marker=dict(
    #     # colors=top_artists['streams'],
    #     colorscale='RdBu',
    #     # cmin=1000000
    #     )
))

# Update layout
# help(go.Sunburst().marker)

fig.update_layout(
    title=f'Top {m} Genres',
    title_x = 0.42,
    width=600, height=600
)

# Display the plot
# st.plotly_chart(fig)

# Keep only the bottom m genres based on total streams
bottom_genres = data_grouped.groupby('artist_genre').agg({'streams': 'sum'}).nsmallest(m, 'streams').index

# Filter data to keep only the bottom m genres
bottom_filtered = data_grouped[data_grouped['artist_genre'].isin(bottom_genres)]

# Keep only the bottom k artists for each genre
bottom_artists = bottom_filtered.groupby('artist_genre').apply(lambda x: x.nsmallest(k, 'streams')).reset_index(drop=True)
bottom_artists['country'] = selected_country

# Plot sunburst for least popular genres and artists
id2 = [selected_country]
labels2 = [selected_country]
parents2 = ['']
values2 = [bottom_artists['streams'].sum()]
for i in range(len(list(set(bottom_artists['artist_genre'])))):
    id2.append(list(set(bottom_artists['artist_genre']))[i])
    labels2.append(list(set(bottom_artists['artist_genre']))[i])
    parents2.append(selected_country)
    values2.append(bottom_artists[bottom_artists['artist_genre'] == list(set(bottom_artists['artist_genre']))[i]]['streams'].sum())
for i in range(len(bottom_artists)):
    parent_value = bottom_artists[bottom_artists['artist_genre'] == bottom_artists['artist_genre'][i]]['streams'].sum()
    child_value = bottom_artists['streams'][i]
    scale_factor = parent_value / child_value if child_value != 0 else 0
    id2.append(bottom_artists['artist_genre'][i] + bottom_artists['artist_individual'][i])
    labels2.append(bottom_artists['artist_individual'][i])
    parents2.append(bottom_artists['artist_genre'][i])
    values2.append(child_value)

# Create a second sunburst plot
fig2 = go.Figure()
fig2.add_trace(go.Sunburst(
    ids=id2,
    labels=labels2,
    parents=parents2,
    values=values2,
    maxdepth=2,
    branchvalues='total',
    insidetextorientation='auto',
    marker = dict(colorscale = 'reds')
    # marker=dict(
    #     # colors=top_artists['streams'],
    #     colorscale='Earth', #Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd
    #     # cmax=1000000
    #     )
))

# Update layout for the second plot
fig2.update_layout(
    title=f'Bot {m} Genres',
    title_x = 0.42,
    width=600, height=600
)

# Display the second plot
# st.plotly_chart(fig2)

# Display the plots side by side
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig)
with col2:
    st.plotly_chart(fig2)