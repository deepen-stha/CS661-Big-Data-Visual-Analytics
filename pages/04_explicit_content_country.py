import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import pydeck as pdk

from datasets import names

st.set_page_config(
    page_title="Music Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
st.title("Music Data Dashboard")

# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

df = pd.read_csv(names.COUNTRY_DATA)

explicit_counts = df[df['explicit'] == True].groupby('country').size().reset_index(name='explicit_count')

col = st.columns((1.5, 4.5, 2), gap ='medium')
with col[1]:
    st.markdown('Number of Tracks with Explicit Content by Countrys')
    fig = px.choropleth(explicit_counts, 
                        locations='country', 
                        locationmode='country names',
                        color='explicit_count', 
                        hover_name='country',
                        # title='Number of Tracks with Explicit Content by Country',
                        color_continuous_scale='blues')
    fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=300
        )
# Use Streamlit to display the Plotly figure
    st.plotly_chart(fig,use_container_width=True)


# ---------------------------------------------------
# this needs more working, till now not completed, so for now I am providing the basic chloreopath 
# I will try to make improve the pydeck chart later.
# ----------------------------------------------------
# # Create a figure using Plotly Express
# with col[0]:
#     layer = pdk.Layer(
#         'HeatmapLayer',
#         data=explicit_counts,
#         get_position=['lng', 'lat'],
#         opacity=0.8,
#         get_weight='explicit_count'
#     )

#     # Set the initial view state for the map
#     view_state = pdk.ViewState(latitude=0, longitude=0, zoom=1)

#     # Create the Pydeck map
#     map_ = pdk.Deck(
#         map_style='mapbox://styles/mapbox/light-v9',
#         layers=[layer],
#         initial_view_state=view_state
#     )

# # Use Streamlit to display the Pydeck map
# st.pydeck_chart(map_)