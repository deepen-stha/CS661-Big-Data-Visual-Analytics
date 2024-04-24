import streamlit as st
import os
import pandas as pd
import pydeck as pdk
import altair as alt 
import plotly.graph_objects as go
from time import sleep

from datasets import names

st.set_page_config(
    layout='wide',
)

@st.cache_data
def load_data():
    return pd.read_csv(names.MUSIC_DATA)


music_data = load_data()

# Function to calculate explicit percentage for each country
def calculate_explicit_percentage(country_file):
    # Read the file
    df = pd.read_csv(country_file)
    # Calculate total number of songs
    total_songs = len(df)
    # Calculate total number of explicit songs
    explicit_songs = df['explicit'].sum()
    # Calculate explicit content percentage
    explicit_percentage = (explicit_songs / total_songs) * 100
    return explicit_percentage


listt = [
    'ae',
    'ar',
    'at',
    'au',
    'be',
    'bg',
    'bo',
    'br',
    'ca',
    'ch',
    'cl',
    'co',
    'cr',
    'cz',
    'de',
    'dk',
    'do',
    'ec',
    'ee',
    'eg',
    'es',
    'fi',
    'fr',
    'gb',
    'gr',
    'gt',
    'hk',
    'hn',
    'hu',
    'id',
    'ie',
    'il',
    'in',
    'is',
    'it',
    'jp',
    'kr',
    'lt',
    'lu',
    'lv',
    'ma',
    'mx',
    'my',
    'ni',
    'nl',
    'no',
    'nz',
    'pa',
    'pe',
    'ph',
    'pl',
    'pt',
    'py',
    'ro',
    'ru',
    'sa',
    'se',
    'sg',
    'sk',
    'sv',
    'th',
    'tr',
    'tw',
    'ua',
    'us',
    'vn',
    'za',
]
distt = {
    'ae': 'United Arab Emirates',
    'ar': 'Argentina',
    'at': 'Austria',
    'au': 'Australia',
    'be': 'Belgium',
    'bg': 'Bulgaria',
    'bo': 'Bolivia, Plurinational State of',
    'br': 'Brazil',
    'ca': 'Canada',
    'ch': 'Switzerland',
    'cl': 'Chile',
    'co': 'Colombia',
    'cr': 'Costa Rica',
    'cz': 'Czechia',
    'de': 'Germany',
    'dk': 'Denmark',
    'do': 'Dominican Republic',
    'ec': 'Ecuador',
    'ee': 'Estonia',
    'eg': 'Egypt',
    'es': 'Spain',
    'fi': 'Finland',
    'fr': 'France',
    'gb': 'United Kingdom',
    'gr': 'Greece',
    'gt': 'Guatemala',
    'hk': 'Hong Kong',
    'hn': 'Honduras',
    'hu': 'Hungary',
    'id': 'Indonesia',
    'ie': 'Ireland',
    'il': 'Israel',
    'in': 'India',
    'is': 'Iceland',
    'it': 'Italy',
    'jp': 'Japan',
    'kr': 'Korea, Republic of',
    'lt': 'Lithuania',
    'lu': 'Luxembourg',
    'lv': 'Latvia',
    'ma': 'Morocco',
    'mx': 'Mexico',
    'my': 'Malaysia',
    'ni': 'Nicaragua',
    'nl': 'Netherlands',
    'no': 'Norway',
    'nz': 'New Zealand',
    'pa': 'Panama',
    'pe': 'Peru',
    'ph': 'Philippines',
    'pl': 'Poland',
    'pt': 'Portugal',
    'py': 'Paraguay',
    'ro': 'Romania',
    'ru': 'Russian Federation',
    'sa': 'Saudi Arabia',
    'se': 'Sweden',
    'sg': 'Singapore',
    'sk': 'Slovakia',
    'sv': 'El Salvador',
    'th': 'Thailand',
    'tr': 'Türkiye',
    'tw': 'Taiwan, Province of China',
    'ua': 'Ukraine',
    'us': 'United States',
    'vn': 'Viet Nam',
    'za': 'South Africa',
}
rev_dic = {
    'United Arab Emirates': 'ae',
    'Argentina': 'ar',
    'Austria': 'at',
    'Australia': 'au',
    'Belgium': 'be',
    'Bulgaria': 'bg',
    'Bolivia, Plurinational State of': 'bo',
    'Brazil': 'br',
    'Canada': 'ca',
    'Switzerland': 'ch',
    'Chile': 'cl',
    'Colombia': 'co',
    'Costa Rica': 'cr',
    'Czechia': 'cz',
    'Germany': 'de',
    'Denmark': 'dk',
    'Dominican Republic': 'do',
    'Ecuador': 'ec',
    'Estonia': 'ee',
    'Egypt': 'eg',
    'Spain': 'es',
    'Finland': 'fi',
    'France': 'fr',
    'United Kingdom': 'gb',
    'Greece': 'gr',
    'Guatemala': 'gt',
    'Hong Kong': 'hk',
    'Honduras': 'hn',
    'Hungary': 'hu',
    'Indonesia': 'id',
    'Ireland': 'ie',
    'Israel': 'il',
    'India': 'in',
    'Iceland': 'is',
    'Italy': 'it',
    'Japan': 'jp',
    'Korea, Republic of': 'kr',
    'Lithuania': 'lt',
    'Luxembourg': 'lu',
    'Latvia': 'lv',
    'Morocco': 'ma',
    'Mexico': 'mx',
    'Malaysia': 'my',
    'Nicaragua': 'ni',
    'Netherlands': 'nl',
    'Norway': 'no',
    'New Zealand': 'nz',
    'Panama': 'pa',
    'Peru': 'pe',
    'Philippines': 'ph',
    'Poland': 'pl',
    'Portugal': 'pt',
    'Paraguay': 'py',
    'Romania': 'ro',
    'Russian Federation': 'ru',
    'Saudi Arabia': 'sa',
    'Sweden': 'se',
    'Singapore': 'sg',
    'Slovakia': 'sk',
    'El Salvador': 'sv',
    'Thailand': 'th',
    'Türkiye': 'tr',
    'Taiwan, Province of China': 'tw',
    'Ukraine': 'ua',
    'United States': 'us',
    'Viet Nam': 'vn',
    'South Africa': 'za',
}
# Read latitude and longitude data
additional_data = {
    "latitude": [
        23.4241,
        -38.4161,
        47.5162,
        -25.2744,
        50.8503,
        42.7339,
        -16.2902,
        -14.235,
        56.1304,
        46.8182,
        -35.6751,
        4.5709,
        9.7489,
        49.8175,
        51.1657,
        56.2639,
        18.7357,
        -1.8312,
        58.5953,
        26.8206,
        40.4637,
        61.9241,
        46.6034,
        55.3781,
        39.0742,
        15.7835,
        22.3193,
        15.2,
        47.1625,
        -0.7893,
        53.1424,
        31.0461,
        20.5937,
        64.9631,
        41.8719,
        36.2048,
        35.9078,
        55.1694,
        49.8153,
        56.8796,
        31.7917,
        23.6345,
        4.2105,
        12.8654,
        52.1326,
        60.472,
        -40.9006,
        8.538,
        -9.1907,
        12.8797,
        51.9194,
        39.3999,
        -23.4425,
        45.9432,
        61.524,
        23.8859,
        60.1282,
        1.3521,
        48.669,
        13.7942,
        15.87,
        38.9637,
        23.6978,
        48.3794,
        37.0902,
        14.0583,
        -30.5595,
    ],
    "longitude": [
        53.8478,
        -63.6167,
        14.5501,
        133.7751,
        4.3517,
        25.4858,
        -63.5887,
        -51.9253,
        -106.3468,
        8.2275,
        -71.543,
        -74.2973,
        -83.7534,
        15.473,
        10.4515,
        9.5018,
        -70.1627,
        -78.1834,
        25.0136,
        30.8025,
        -3.7492,
        25.7482,
        1.8883,
        -3.436,
        21.8243,
        -90.2308,
        114.1694,
        -86.2419,
        19.5033,
        113.9213,
        -7.6921,
        34.8516,
        78.9629,
        -19.0208,
        12.5674,
        138.2529,
        127.7669,
        23.8813,
        6.1296,
        24.6032,
        -7.0926,
        -102.5528,
        101.9758,
        -85.2072,
        5.2913,
        8.4689,
        174.886,
        -80.7821,
        -75.0152,
        121.774,
        19.1451,
        -8.2245,
        -58.4438,
        24.9668,
        105.3188,
        45.0792,
        18.6435,
        103.8198,
        19.699,
        -88.8965,
        100.9925,
        35.2433,
        120.9605,
        31.1656,
        -95.7129,
        108.2772,
        22.9375,
    ],
}

# Create DataFrame for latitude and longitude
df_ll = pd.DataFrame(additional_data, index=listt)
df_ll.index.name = 'Country'

# Folder containing aggregated files
output_directory = f'{names.REGIONWISE_EXPLICITNESS_DATA}/'


def get_country_name(country_code):
    return distt.get(country_code, 'Unknown')


def gexpl(country_file, k):
    # Read the file
    df = pd.read_csv(country_file)
    # Calculate number of songs for top k percentage
    top_k_songs = int(len(df) * (k / 100))
    # Filter top k percentage of songs
    top_k_df = df.tail(top_k_songs)
    # Calculate total number of explicit songs in top k percentage
    explicit_songs_top_k = top_k_df['explicit'].sum()
    # Calculate explicit content percentage for top k percentage of songs
    explicit_percentage_top_k = round(
        (explicit_songs_top_k / top_k_songs) * 100, 2
    )

    return explicit_percentage_top_k


# Function to get top k percent of songs' explicit percentage
def get_top_k_explicit_percentage(k):
    explicit_percentages = {}
    for filename in os.listdir(output_directory):
        if filename.endswith('.csv'):
            country_file = os.path.join(output_directory, filename)
            country_name = filename.split('_')[0]
            explicit_percentage = gexpl(country_file, k)
            explicit_percentages[country_name] = explicit_percentage

    # Convert explicit percentages to DataFrame
    df_explicit_percentages = pd.DataFrame(
        explicit_percentages.items(), columns=['Country', 'Explicit Percentage']
    )

    # Merge with latitude and longitude data
    df_combined = pd.merge(df_explicit_percentages, df_ll, on='Country')

    # Sort by explicit percentage
    df_combined.sort_values(
        by='Explicit Percentage', ascending=False, inplace=True
    )

    # Get top k percent
    top_k_percent = int(len(df_combined) * (k / 100))

    return df_combined.head(top_k_percent)


# Streamlit app
st.markdown("# Country Wise percentage of explicitness in popular songs  ")

# Slider for selecting top k percent
k_percent = st.slider('Select top k percent of songs', 0, 100, 100)

# Get top k percent of songs' explicit percentage
df_top_k = get_top_k_explicit_percentage(k_percent)

df_top_k['Country_Name'] = df_top_k['Country'].apply(get_country_name)


def map_explicit_percentage_to_color(explicit_percentage):
    # Define the lightest and darkest green colors
    lightest_green = [244, 255, 255, 100]  # Light green
    darkest_green = [0, 100, 0, 255]      # Dark green
    
    # Interpolate between the lightest and darkest green based on explicit percentage
    alpha = explicit_percentage / 100
    color = [
        int(lightest_green[i] * (1 - alpha) + darkest_green[i] * alpha)
        for i in range(3)
    ]
    color.append(255)  # Set alpha channel to 255
    
    return color


# Apply the function to create a new column for marker color
df_top_k['fill_color'] = df_top_k['Explicit Percentage'].apply(
    map_explicit_percentage_to_color
)


# Create Pydeck map
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_top_k,
    get_position=['longitude', 'latitude'],
    get_radius=100000,
    get_fill_color='fill_color',  # Red color for markers
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=1.0,
    pitch=45,
)

tooltip = {
    'html': '<b>{Country_Name}</b><br />Explicit Percentage: {Explicit Percentage}',
    'style': {
        'backgroundColor': 'rgba(100, 100, 100, 0.9)',  # Lighter shade of gray with some transparency
        'color': 'white',
    },
}
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v9',
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
))
def generate_legend():
    # Define the colors
    min_green = (244, 255, 255)  # Light green
    max_green = (0, 100, 0)     # Dark green
    
    # Generate HTML for continuous legend
    legend_html = "<div style='display: flex; flex-direction: row; width: 100%;'>"
    for i in range(6):  # Generate 6 color shades
        alpha = i / 5  # Vary alpha from 0 to 1 in steps of 0.2
        r = int(min_green[0] * (1 - alpha) + max_green[0] * alpha)
        g = int(min_green[1] * (1 - alpha) + max_green[1] * alpha)
        b = int(min_green[2] * (1 - alpha) + max_green[2] * alpha)
        color_str = f"rgba({r}, {g}, {b}, 1)"
        legend_html += f"<div style='background-color: {color_str}; flex-grow: 1; height: 30px;'></div>"
    legend_html += "</div>"
    
    return legend_html

# Generate legend HTML
legend_html = generate_legend()

# Define the global average
global_avg = "42.11%"

# Create HTML string for the legend with the global average
legend_with_global = f"<div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 10vh;'>{legend_html}<div style='margin-top: 20px; margin-bottom: 50px; font-size: 30px; color: rgba(150, 150, 150, 1); padding: 10px;'><span style='background-color: rgba(194, 230, 153, 1); '></span><span style='background-color: rgba(194, 230, 153, 1); '></span></div></div>"

# Render the legend with the global average using markdown
st.markdown(legend_with_global, unsafe_allow_html=True)





# Function to load country data
def load_country_data(country_codes):
    data = []
    for country_code in country_codes:
        file_path = (
            f"{names.YEARWISE_EXPLICITNESS_DATA}/{country_code}_aggregated.csv"
        )
        if os.path.exists(file_path):
            country_data = pd.read_csv(file_path)
            # Add country code as a column for later use
            country_data['Country'] = country_code
            data.append(country_data)
    return pd.concat(data)



# Default selection
default_selection = ["India", "United States"]

# Convert default selection to country codes
default_selection_codes = [rev_dic[country] for country in default_selection]

# Select multiple countries with default value
selected_countries = st.multiselect(
    "Select countries", list(distt.values()), default=default_selection
)

# Convert selected country names to country codes
selected_country_codes = [rev_dic[country] for country in selected_countries]

# Load data for selected countries
country_data = load_country_data(selected_country_codes)
global_reference_data = pd.DataFrame({
    'Year': [2017, 2018, 2019, 2020, 2021, 2022],
    'Explicit Percentage': [.3792, 0.4686, 0.4428, 0.4401, 0.3820, 0.3544]
})

col1, col2 = st.columns(2)

with col2:
    if not country_data.empty:
        st.write("")
        st.write("")
        st.write("**Explicit Percentage Over the Years**")
        st.write("")
        st.write("")
        st.write("")
        # Ensure 'Year' column is numeric
        country_data['Year'] = pd.to_numeric(country_data['Year'])
        # Scale 'Explicit Percentage' data to range between 0 and 1
        country_data['Explicit Percentage'] /= 100
        
        # Create Altair chart for country data
        country_chart = alt.Chart(country_data).mark_line().encode(
            x='Year:O',  # O for ordinal scale for categorical data (years)
            y=alt.Y('Explicit Percentage:Q', axis=alt.Axis(format='0.0%')),  # Format y-axis labels as percentages
            color='Country:N'  # N for nominal scale for categorical data (country)
        )
        
        # Create Altair chart for global reference line
        global_ref_line = alt.Chart(global_reference_data).mark_line(color='red', strokeDash=[3,3]).encode(
            x='Year:O',  # O for ordinal scale for categorical data (years)
            y=alt.Y('Explicit Percentage:Q', axis=alt.Axis(format='0.0%',title=None)),  # Format y-axis labels as percentages
        )
        
        # Overlay country chart and global reference line
        chart = (country_chart + global_ref_line).properties(
            width=600,  # Adjust chart width as needed
            height=400  # Adjust chart height as needed
        ).configure_axis(
            labelAngle=0  # Rotate X-axis labels horizontally
        )

        # Show combined chart using Streamlit
        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("No data available for the selected countries.")

with col1:
    # Calculate average obscenity and instrumentalness for each year
    average_obscenity = music_data.groupby('release_date')['obscene'].mean().reset_index()
    average_instrumentalness = (
        music_data.groupby('release_date')['instrumentalness'].mean().reset_index()
    )

    # Determine y-axis range
    y_min = min(
        average_obscenity['obscene'].min(),
        average_instrumentalness['instrumentalness'].min(),
    )
    y_max = max(
        average_obscenity['obscene'].max(),
        average_instrumentalness['instrumentalness'].max(),
    )
    y_range = [max(0, y_min - 0.1), min(1, y_max)]

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
            opacity=0.7,
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
        xaxis=dict(
            dtick=10
        ),  # Adjust tick frequency on x-axis for better readability
        yaxis=dict(range=y_range),  # Set dynamic range for y-axis
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
            fig.data[0]['x'] = average_obscenity['release_date'][: i + 1]
            fig.data[0]['y'] = average_obscenity['obscene'][: i + 1]
            # fig.data[1]['x'] = average_instrumentalness['release_date'][:i+1]
            # fig.data[1]['y'] = average_instrumentalness['instrumentalness'][:i+1]
            plot.plotly_chart(fig, use_container_width=True)
