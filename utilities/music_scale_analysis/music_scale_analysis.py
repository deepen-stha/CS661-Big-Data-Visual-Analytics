"""
Copyright 2024 Indraneel Rajeevan
SPDX-License-Identifier: BSD-3-Clause

Project:
IIT Kanpur CS661 End-semester Activity,
Music Data Visualization,
Music Scale Analysis (Valence-Mode)
"""

import streamlit as st

from scales.attributes import *
from scales.raw import *

from scales.plots.boxplot import show_boxplot
from scales.plots.heatmap import show_heatmap
from scales.plots.piechart import show_piechart


@st.cache_resource
def load_dataset():
    return initialize()


def init_layout():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left: 2rem;
                padding-right: 2rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state():
    if 'reset' not in st.session_state:
        st.session_state.reset = False
    if 'notation' not in st.session_state:
        st.session_state.notation = '#'
    if 'key' not in st.session_state:
        st.session_state.key = 'C'
    if 'mode' not in st.session_state:
        st.session_state.mode = 'Major'
    if 'property' not in st.session_state:
        st.session_state.property = 'Valence'
    if 'features' not in st.session_state:
        st.session_state.features = properties


def reset_button_callback():
    st.session_state.reset = True
    st.session_state.notation = '#'
    st.session_state.key = 'C'
    st.session_state.mode = 'Major'
    st.session_state.property = 'Valence'
    st.session_state.features = properties


def run():

    df = load_dataset()

    music_scales_url = 'https://en.wikipedia.org/wiki/Scale_(music)'
    music_scales_md = f'[{music_scales_url}]({music_scales_url})'

    spotify_api_url = 'https://developer.spotify.com/documentation'
    spotify_api_md = f'[{spotify_api_url}]({spotify_api_url})'

    virtual_piano_url = 'https://www.musicca.com/scale-finder'
    virtual_piano_url_md = f'[{virtual_piano_url}]({virtual_piano_url})'

    col_title, _, col_scales = st.columns([0.5, 0.13, 0.37])

    with col_title:

        st.title('Music Scale Analysis 🎵')
        st.markdown('#####')

        col0, col1, col2, col3, col4 = st.columns(
            [1, 2, 2, 2, 3],
        )

        with col0:
            st.markdown('#####')
            st.button(
                '↻',
                type='secondary',
                help='Reset all plots',
                on_click=reset_button_callback,
                use_container_width=False,
            )

        with col1:
            scale_notation = st.selectbox(
                'Notation',
                [
                    '#',
                    'b',
                ],
                key='notation',
            )
            use_sharp_notation = True if scale_notation == '#' else False

        with col2:
            scale_key = st.selectbox(
                'Scale Key',
                list(
                    pitch_class_map_sharp.values()
                    if use_sharp_notation
                    else pitch_class_map_flat.values()
                ),
                key='key',
            )

        with col3:
            scale_mode = st.selectbox(
                'Scale Mode',
                [
                    'Major',
                    'Minor',
                ],
                key='mode',
            )

        with col4:
            property = st.selectbox(
                'Music Property',
                [p.capitalize() for p in properties],
                key='property',
            ).lower()

    scale = f'{scale_key}-{scale_mode}'

    with col_scales:
        with st.container(border=True):
            st.markdown(f'**Music Scales:** {music_scales_md}')
            st.markdown(f'**Spotify API:** {spotify_api_md}')
            st.markdown(f'**Play Scales:** {virtual_piano_url_md}')

    features = st.multiselect(
        'Features',
        help='Choose interested features',
        placeholder='Choose interested features',
        options=properties,
        key='features',
    )
    if len(features) == 0:
        features = [st.session_state.property.lower()]

    col1, col2, col3 = st.columns([0.45, 0.25, 0.3])

    with col1:
        with st.container(border=True):
            st.plotly_chart(
                show_piechart(df, scale, features),
                use_container_width=True,
            )

    with col2:
        with st.container(border=True):
            st.plotly_chart(
                show_boxplot(df, property, scale),
                use_container_width=True,
            )

    with col3:
        with st.container(border=True):
            st.plotly_chart(
                show_heatmap(df, property, use_sharp_notation),
                use_container_width=True,
            )


if __name__ == '__main__':

    st.set_page_config(
        page_title='Music Scale Analysis 🎵',
        layout='wide',
    )

    init_layout()
    init_state()

    with st.container(border=True):
        run()
