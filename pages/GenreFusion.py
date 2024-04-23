import streamlit as st
import pandas as pd
import chardet
import numpy as np
import plotly.express as px

from datasets import names

#load data from a specific country and year
def load_country_data(country_code, year):
    path_ = f'{names.GENRE_FUSION_DATA}/{country_code}/{country_code}-genre_network-{year}.csv'
    with open(path_, 'rb') as f:
        result = chardet.detect(f.read())
    return pd.read_csv(path_, encoding=result['encoding'])

country_codes = {
    'ae': 'United Arab Emirates',
    'ar': 'Argentina',
    'at': 'Austria',
    'au': 'Australia',
    'be': 'Belgium',
    'bg': 'Bulgaria',
    'bo': 'Bolivia',
    'br': 'Brazil',
    'ca': 'Canada',
    'ch': 'Switzerland',
    'cl': 'Chile',
    'co': 'Colombia',
    'cr': 'Costa Rica',
    'cz': 'Czech Republic',
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
    'global': 'Global', 
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
    'kr': 'South Korea',
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
    'ru': 'Russia',
    'sa': 'Saudi Arabia',
    'se': 'Sweden',
    'sg': 'Singapore',
    'sk': 'Slovakia',
    'sv': 'El Salvador',
    'th': 'Thailand',
    'tr': 'Turkey',
    'tw': 'Taiwan',
    'ua': 'Ukraine',
    'us': 'United States',
    'vn': 'Vietnam',
    'za': 'South Africa'
}

st.title('Fusion Genre Visualization')

selected_country_code = st.selectbox('Select a country', list(country_codes.keys()), format_func=lambda x: country_codes[x])

year = st.number_input('Enter the year', min_value=2019, max_value=2022, value=2020)

country_data = load_country_data(selected_country_code, year)
country_data.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

country_data['Weighted_Popularity'] = country_data['Weight'] * country_data['Avg_Popularity']

top_20_genres = country_data.nlargest(150, 'Weighted_Popularity')

# Normalize 'Weighted_Popularity' column to range [0, 1]
min_val = top_20_genres['Weighted_Popularity'].min()
max_val = top_20_genres['Weighted_Popularity'].max()
top_20_genres['Popularity'] = (top_20_genres['Weighted_Popularity'] - min_val) / (max_val - min_val)
top_20_genres['Popularity'].replace([np.inf, -np.inf, np.nan], 0, inplace=True)

# Plot bubble plot with Plotly
fig = px.scatter(top_20_genres, x='Source', y='Target', size='Popularity', color='Popularity',
                 hover_name='Source', hover_data={'Target': True, 'Popularity': True},
                 labels={'Source': 'Source Genre', 'Target': 'Target Genre'},
                 title=f'Bubble Plot of Top 20 Fusion Genres in {country_codes[selected_country_code]} for the year {year}',
                 size_max=50, width=800, height=600, color_continuous_scale='Blues')

fig.update_layout(xaxis_tickangle=-45, xaxis_title_standoff=40)
fig.update_yaxes(title_standoff=40)

st.plotly_chart(fig)
