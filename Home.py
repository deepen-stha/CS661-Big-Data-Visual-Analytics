import streamlit as st

headline = 'Audio Aura'

st.set_page_config(
    page_title=headline,
    page_icon='🎵',
    layout='wide',
    initial_sidebar_state='expanded',
)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images5.alphacoders.com/438/438504.jpg');
        background-attachment: fixed;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(headline)

# TODO: Homepage components
