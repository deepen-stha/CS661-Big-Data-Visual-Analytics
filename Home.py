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
st.markdown("""
""", unsafe_allow_html=False)

# Adding a brief introduction about the project in bold
st.markdown("""
**In the dynamic realm of music, knowing what resonates with audiences is crucial. Our data-driven exploration helps us uncover trends and insights driving musical achievements. With innovative analytics and visualization, we navigate through genre preferences, artist popularity, and emerging trends.**
""", unsafe_allow_html=False)

# TODO: Homepage components
st.markdown("""
**Join us as we decode the secrets of musical success, shaping the future of music creation and engagement.**
""", unsafe_allow_html=False)