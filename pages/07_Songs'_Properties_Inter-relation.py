
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit.components.v1 import html
from datasets import names

# Function to plot the data

# Import Allura font from Google Fonts
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Allura&display=swap" rel="stylesheet">
    
    <style>
    @keyframes color-dots {
        0% {
            transform: translate(0, 0);
        }
        50% {
            transform: translate(10px, -10px);
        }
        100% {
            transform: translate(0, 0);
        }
    }

    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;  # Adjust height as needed
    }
    .top_left {
        display: flex;
        justify-content: left;
        align-items: center;
        height: 100px;  # Adjust height as needed
    }

    .script-text {
        font-family: 'Allura', cursive;
        font-size: 64px;  # Adjust size as needed
        font-weight: normal;  # Use normal font weight
        text-align: center;
        color: white;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
        position: relative;
    }

    .text {
        font-family: 'Allura', cursive;
        font-size:100px;  # Adjust size as needed
        font-weight: normal;  # Use normal font weight
        text-align: center;
        color: orange;
        
        position: relative;
    }

    .basic_text {
        font-family: 'Comic Sans MS';
        font-size:100px;  # Adjust size as needed
        font-weight: normal;  # Use normal font weight
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        
        position: relative;
    }

    .script-text::before,
    .script-text::after {
        content: '';
        position: absolute;
        background: radial-gradient(circle, rgba(255, 0, 255, 0.7), rgba(255, 0, 255, 0));
        width: 10px;
        height: 10px;
        border-radius: 50%;
        animation: color-dots 2s infinite;
    }

    .script-text::before {
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
    }

    .script-text::after {
        bottom: 10px;
        right: 50%;
        transform: translateX(50%);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Use a div to center the text with a visually appealing effect
st.write(
    """
    
    <div class="centered">
        <div class="script-text">Mix & Master</div>
    </div>
    """,
    unsafe_allow_html=True,
)


def plot_data(views, show_median, median_color, box_color):
    fig1 = go.Figure()

    fig1.add_trace(go.Box(y=views,
                         boxmean=show_median,
                         marker_color=box_color,  # Change marker color here
                         line_color=median_color if show_median else None,
                         boxpoints=False))  # Set to 'outliers' to show outliers

    fig1.update_layout(
        yaxis=dict(type='log', title='Streams (log scale)', showgrid=False, color='white'),
        title='Number of Stream Analysis',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=False, color='white'),
        title_font=dict(color='white'),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig1)

# Define list of countries and years
countries_raw = ["United Arab Emirates", "Argentina", "Austria", "Australia", "Belgium", "Bulgaria",
             "Bolivia",'Brazil',"Canada","Switzerland", "Chile","Colombia","Costa Rica","Czech Republic",
             "Germany","Denmark","Dominican Republic","Ecuador", "Estonia","Egypt", "Spain", "Finland",
             "France","United Kingdom","Greece", "Guatemala", "Hong Kong", "Honduras", 'Hungary','Indonesia',
              "Ireland","Israel","India","Iceland", "Italy", "Japan",'South Korea', 'Lithuania','Luxembourg',
              'Latvia','Morocco','Mexico','Malaysia','Nicaragua','Netherlands', 'Norway','New Zealand','Panama',
              'Peru','Philippines','Poland','Portugal', 'Paraguay','Romania','Russia','Saudi Arabia', 'Sweden','Singapore','Slovakia',
              'El Salvador','Thailand','Turkey','Taiwan','Ukraine', 'United States', 'Vietnam','South Africa'
              ]  # Add your list of countries here
countries = sorted(countries_raw)


m = {'United Arab Emirates':'ae','Argentina':'ar', 'Austria': 'at', 'Australia': 'au', 'Belgium':'be','Bulgaria':'bg',
     'Bolivia':'bo','Brazil':'br', 'Canada':'ca', 'Switzerland':'ch','Chile':'cl','Colombia':'co',
      'Costa Rica':'cr','Czech Republic':'cz','Germany':'de','Denmark':'dk','Dominican Republic':'do','Ecuador':'ec',
      'Estonia':'ee', 'Egypt':'eg', 'Spain':'es', 'Finland':'fi','France':'fr', 'United Kingdom':'gb','Greece':'gr',
      'Guatemala':'gt','Hong Kong':'hk','Honduras':'hn', 'Hungary':'hu', 'Indonesia':'id','Ireland':'ie', 'Israel':'il',
      'India':'in', 'Iceland':'is', 'Italy':'it','Japan':'jp', 'South Korea':'kr','Lithuania':'lt','Luxembourg':'lu',
      'Latvia':'lv','Morocco':'ma','Mexico':'mx','Malaysia':'my','Nicaragua':'ni','Netherlands':'nl','Norway':'no', 'New Zealand':'nz',
      'Panama':'pa','Peru':'pe','Philippines':'ph','Poland':'pl','Portugal':'pt','Paraguay':'py', 'Romania':'ro','Russia':'ru',
      'Saudi Arabia':'sa', 'Sweden':'se','Singapore':'sg', 'Slovakia':'sk', "El Salvador":'sv','Thailand':'th', 'Turkey':'tr',
      'Taiwan':'tw','Ukraine':'ua','United States':'us', 'Vietnam':'vn',' South Africa':'za'

        }
years = ['2017', '2018', '2019', '2020', '2021','2022']  # Add your list of years here



countries = ["Select"] + countries
years = ["Select"] + years
# User selects country and year
selected_country = st.selectbox("Select Country", countries)
selected_year = st.selectbox("Select Year", years)
if selected_country =='Select' or selected_year == 'Select':
    st.stop()
# /Users/shauryaagarwal/Desktop/streamlit/MGDplus/songs/regional/kr/kr-hit_songs-2021

# Construct file path based on selected country and year
file_path = names.REGIONWISE_CORRELATION_DATA+ m[selected_country] + '/' + m[selected_country] +'-hit_songs-' + selected_year +'.csv'



# Read the selected CSV file
try:
    data = pd.read_csv(file_path, delimiter='\t')
    data.dropna(inplace=True)
    st.write("Data loaded successfully.") 
except FileNotFoundError:
    st.error("No data available for selected combination")
    st.stop()

# Select specific attributes for correlation
attributes = ["popularity", "acousticness", "num_available_markets", "duration_ms", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "valence", "tempo", "total_streams"]

st.sidebar.markdown("<h1 class= 'text' >Audio Aura</h1>", unsafe_allow_html=True)

st.sidebar.markdown("<h2 class= 'basic_text' >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Apply&nbsp;&nbsp;&nbsp; filters</h2>", unsafe_allow_html=True)

min_popularity = int(data["popularity"].min())
max_popularity = int(data["popularity"].max())
min_popularity1 = int(data["popularity"].min())
max_popularity2 = int(data["popularity"].max())

stream_range1 = st.sidebar.slider(
        "Select #Stream Range",
        min_value=int(data["total_streams"].min()),
        max_value=int(data["total_streams"].min()),
        value=(int(data["total_streams"].min()), int(data["total_streams"].max())),
        key="stream_range1"
    )


popularity_range1 = st.sidebar.slider(
        "Select Popularity Range",
        min_value=min_popularity1,
        max_value=max_popularity2,
        value=(min_popularity1, max_popularity2),
        key="popularity_range1"
    )

filtered_data1 = data[(data["popularity"] >= popularity_range1[0]) & (data["popularity"] <= popularity_range1[1]) & (data["total_streams"] >= stream_range1[0])
        & (data["total_streams"] <= stream_range1[1])]

selected_data1 = filtered_data1[attributes]
st.write(((len(selected_data1))/len(data['popularity']))*100," %")

# Create a correlation matrix
correlation_matrix = selected_data1.corr()

# Create a heatmap trace
heatmap_trace = go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    colorscale="YlOrBr",  # Use red-blue color scale
    zmin=-1,
    zmax=1,
    colorbar=dict(title="Correlation"),
    hoverinfo='text',  # Set hoverinfo to text
    hovertemplate="Attribute %{y}: %{x}<br>Correlation: %{z:.2f}",  # Define hovertemplate
    hoverongaps=False,
    reversescale=True,
)

# Create layout
layout = go.Layout(
    title="Song's properties Analysis via Correlation",
    xaxis=dict(title="Attributes"),
    yaxis=dict(title="Attributes"),
)

# Create figure
fig = go.Figure(data=[heatmap_trace], layout=layout)
# Set the size of the figure
fig.update_layout(width=800, height=600)

# Update hover mode to compare mode
fig.update_layout(hovermode="closest")

# Add hover effect to enlarge the hovered cell
fig.update_layout(hoverlabel=dict(
    bgcolor="black",
    font_size=16,
    bordercolor="white",
))

# Display the heatmap
st.plotly_chart(fig)

#wiscus plot
show_plot = st.sidebar.checkbox("#stream analysis via Wiscus Plot", value=False)
if show_plot:
    st.subheader("Wiscus Plot")
    
    st.sidebar.header("")
    popularity_range = st.sidebar.slider(
        "Select Popularity Range",
        min_value=int(data["popularity"].min()),
        max_value = int(data["popularity"].max()),
        value=(min_popularity, max_popularity),
        key="popularity_range"
    )

    stream_range = st.sidebar.slider(
        "Select #Stream Range",
        min_value=int(data["total_streams"].min()),
        max_value=int(data["total_streams"].min()),
        value=(int(data["total_streams"].min()), int(data["total_streams"].max())),
        key="stream_range"
    )

    max_data_points = len(data)
   
    show_median = True
    median_color = '#0BF1FA'
    box_color = 'blue'

# Generate and plot the data
# views = int(data["total_streams"])
    filtered_df = data[
        (data["total_streams"] >= stream_range[0])
        & (data["total_streams"] <= stream_range[1])
        & (data["popularity"] >= popularity_range[0])
        & (data["popularity"] <= popularity_range[1])
    ]
    st.write((len(filtered_df)/len(data['popularity']))*100, " %")
    views = filtered_df['total_streams'].tolist()
    plot_data(views, show_median, median_color, box_color)
else:
    st.write("Select checkbox from side menu for stream analysis")