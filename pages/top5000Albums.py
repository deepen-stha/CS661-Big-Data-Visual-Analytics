import streamlit as st
import pandas as pd
import plotly.express as px
from dateutil.parser import parse
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

from datasets import names


cloud_image_path = './assets/img/cloud.png'


# Load your dataset
data_path = names.UPDATED_TOP_5000_DATA
data = pd.read_csv(data_path)

# Split genres and create a list of unique genres
all_genres = set()
data['Genre'].str.split(',').apply(lambda x: all_genres.update(x))
all_genres = list(all_genres)

# Create sidebar for genre selection
selected_genres = st.sidebar.multiselect('Select Genres', all_genres)

# Convert release date to datetime
data['rel_date'] = data['rel_date'].apply(lambda x: parse(x))

# Create date range filter
min_date = data['rel_date'].min()
max_date = data['rel_date'].max()
start_date = st.sidebar.date_input('Start Date', min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input('End Date', max_date, min_value=min_date, max_value=max_date)

# Convert start_date and end_date to datetime objects
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter the dataset based on selected genres and date range
if start_date <= end_date:
    filtered_data = data[data['rel_date'].between(start_date, end_date)]
elif start_date > end_date:
    st.warning('Start date should be before or equal to end date. Please adjust the date range.')
    filtered_data = data
else:
    filtered_data = data

# Function to get sentiment
def get_sentiment(text):
    analysis = TextBlob(str(text))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'



# Filter the dataset based on selected genres
if selected_genres:
    filtered_data = filtered_data[filtered_data['Genre'].apply(lambda x: any(genre in selected_genres for genre in x.split(',')))]
    

# Calculate the range of average ratings for selected genres
min_rating = filtered_data['avg_rat'].min() if not filtered_data.empty else 0
max_rating = filtered_data['avg_rat'].max() if not filtered_data.empty else 5
st.subheader('Genre Comparison: Average Ratings')
# Show visualizations for selected genres
# Show visualizations for selected genres or top 5 genres if none selected
if selected_genres:
    
    filtered_data = filtered_data[filtered_data['Genre'].apply(lambda x: any(genre in selected_genres for genre in x.split(',')))]
    if not filtered_data.empty:
        # Create a boxplot for average ratings using Plotly
        fig = px.box(filtered_data, y='avg_rat', color='Genre', title='Genre Comparison: Average Ratings'
                     ,hover_data={'Genre': False, 'avg_rat': True, 'album': True})
        #Update the layout to set the background color to a dark gradient
        fig.update_layout(
            plot_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            paper_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            font_color='white'  # White font color
        )
        st.plotly_chart(fig)
        # Calculate summary statistics for the box plot
        summary_stats = filtered_data.groupby('Genre')['avg_rat'].describe()
        # Show the summary statistics in a table
        st.subheader('Summary Statistics')
        st.write(summary_stats)


        # Genre Preference plot
        st.subheader('Genre Preference: Number of Ratings vs. Average Ratings')
        fig_preference = px.scatter(filtered_data, x='num_rat', y='avg_rat', color='Genre', title='Genre Preference: Number of Ratings vs. Average Ratings',
                                    hover_data={'Genre': True, 'num_rat': True, 'avg_rat': True, 'album': True, 'rel_date':True})
        fig_preference.update_layout(
            plot_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            paper_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            font_color='white'  # White font color
        )
        st.plotly_chart(fig_preference)

        


        # #Trend Analysis for number of ratings
        # st.subheader('Trend Analysis: Number of Ratings Over Time for Selected Genre')
        # # Sort the data by release date
        # filtered_data_sorted = filtered_data.sort_values('rel_date')
        # fig_trend_selected = px.line(filtered_data_sorted, x='rel_date', y='num_rat', color='Genre', title='Trend Analysis: Number of Ratings Over Time for Selected Genre')
        # fig_trend_selected.update_layout(
        #     plot_bgcolor='rgb(31, 31, 31)',  # Dark gray background
        #     paper_bgcolor='rgb(31, 31, 31)',  # Dark gray background
        #     font_color='white'  # White font color
        # )
        # st.plotly_chart(fig_trend_selected)
        
        

        # Plot for reviews
        # Plot for reviews
        colors = px.colors.qualitative.Pastel
        # Group by genre and calculate the total number of reviews for each genre
        genre_reviews = filtered_data.groupby('Genre')['num_revs'].sum().reset_index()
        # Sort genres by number of reviews in descending order
        genre_reviews = genre_reviews.sort_values(by='num_revs', ascending=False)
        # Plot the number of reviews for selected genres as a pie chart
        fig_genre_reviews = px.pie(genre_reviews, names='Genre', values='num_revs', 
                                    title='Number of Reviews by Genre',
                                    color='Genre', color_discrete_sequence=colors,
                                    labels={'Genre': 'Genre', 'num_revs': 'Number of Reviews'},
                                    hole=0.3,  # Set the center hole size
                                    )
        fig_genre_reviews.update_traces(textposition='inside', textinfo='percent+label')
        fig_genre_reviews.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            font_color='white',  # White font color
            margin=dict(t=50),  # Add margin to the top
            legend=dict(orientation='h', yanchor='bottom', y=-0.2),  # Position legend below the chart
        )
        st.plotly_chart(fig_genre_reviews)





        # Sentiment Analysis
        # Apply sentiment analysis to descriptions and create a new column for sentiment
        filtered_data['sentiment'] = filtered_data['descs'].apply(get_sentiment)
        # Group by genre and sentiment to get the count
        genre_sentiment_counts = filtered_data.groupby(['Genre', 'sentiment']).size().reset_index(name='counts')

        # Define custom pastel colors with transparency for sentiment categories
        colors = {'positive': 'rgba(76,154,42, 0.5)',  # Light blue-green with 70% opacity
                'negative': 'rgba(255,0,0, 0.3)',  # Light orange with 70% opacity
                'neutral': 'rgba(0,0,255, 0.3)'}    # Light yellow with 70% opacity

        # Define border colors for each sentiment category
        border_colors = {'positive': '#00FF00',  # Dark green
                        'negative': '#FF0000',    # Dark red
                        'neutral': '#0000FF'}     # Dark blue

        # Plot the distribution of sentiment for each genre using a bar chart
        fig_genre_sentiment = px.bar(genre_sentiment_counts, x='Genre', y='counts', color='sentiment',
                                    title='Genre and Sentiment in Descriptions',
                                    labels={'Genre': 'Genre', 'counts': 'Count', 'sentiment': 'Sentiment'},
                                    color_discrete_map=colors)

        # Add border to the bars
        for sentiment, color in border_colors.items():
            fig_genre_sentiment.for_each_trace(lambda t: t.update(marker_line_color=color, marker_line_width=1.5)
                                                if t.name == sentiment else (),)

        fig_genre_sentiment.update_layout(
            plot_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            paper_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            font_color='white'  # White font color
        )
        st.plotly_chart(fig_genre_sentiment)





        # Word Cloud
        # Combine the descriptions for selected genres
        text = ' '.join(str(desc) for desc in filtered_data['descs'] if not pd.isnull(desc))
        # Check if text is not empty
        if text:
            mask_image = np.array(Image.open(cloud_image_path))
            # Create the word cloud with the mask
            wordcloud = WordCloud(width=800, height=400, background_color='rgba(255, 255, 255, 0)', mode='RGBA', mask=mask_image).generate(text)
            # Display the word cloud using Streamlit
            st.image(wordcloud.to_array(), use_column_width=True)


    else:
        st.write('No data available for the selected genres.')
else:
    # Create a selectbox for choosing the number of genres to display
    num_genres = st.selectbox('Select Top Number of Genres', [3, 5, 10, 15])

    # Show top N genres visualization
    top_genres = data['Genre'].str.split(',').explode().value_counts().head(num_genres).index.tolist()
    top_data = data[data['Genre'].apply(lambda x: any(genre in top_genres for genre in x.split(',')))]

    if not top_data.empty:
        st.subheader(f'Top {num_genres} Genres: Average Ratings')
        # Create a boxplot for average ratings using Plotly
        fig = px.box(top_data, y='avg_rat', color='Genre', title=f'Top {num_genres} Genres: Average Ratings',
                 hover_data={'Genre': False, 'avg_rat': True, 'album': True})
        # Update the layout to set the background color to a dark gradient
        fig.update_layout(
            plot_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            paper_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            font_color='white'  # White font color
        )
        st.plotly_chart(fig)
        # Calculate summary statistics for the box plot
        summary_stats = top_data.groupby('Genre')['avg_rat'].describe()
        # Show the summary statistics in a table
        st.subheader('Summary Statistics')
        st.write(summary_stats)



        # Genre Preference plot top n
        st.subheader('Genre Preference: Number of Ratings vs. Average Ratings')
        fig_preference = px.scatter(top_data, x='num_rat', y='avg_rat', color='Genre', title='Genre Preference: Number of Ratings vs. Average Ratings',
                                    hover_data={'Genre': True, 'num_rat': True, 'avg_rat': True, 'album': True,'rel_date':True})
        fig_preference.update_layout(
            plot_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            paper_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            font_color='white'  # White font color
        )
        st.plotly_chart(fig_preference)



        #Analysis for top 5 genres reviews
        # Calculate the total number of reviews for each genre
        genre_reviews = filtered_data.groupby('Genre')['num_revs'].sum().reset_index()
        # Sort genres by the number of reviews in descending order
        top_genres_reviews = genre_reviews.sort_values('num_revs', ascending=False).head(num_genres)
        # Define a color palette for the genres
        colors = px.colors.qualitative.Set3
        # Plot the top 5 genres by number of reviews as a donut chart with actual numbers
        # Plot the top 5 genres by number of reviews as a donut chart with actual numbers
        fig_top_genres_reviews_donut = px.pie(top_genres_reviews, values='num_revs', names='Genre',
                                            title='Top 5 Genres by Number of Reviews',
                                            hole=0.3,  # Set the size of the hole in the center
                                            labels={'num_revs': 'Number of Reviews'},
                                            hover_data=['num_revs'],  # Display actual numbers in hover
                                            )
        # Update hover text to show both percentage and actual number
        hover_text = [f"{label}<br>{value}"
                    for label, value, percent in zip(top_genres_reviews['Genre'],
                                                        top_genres_reviews['num_revs'],
                                                        top_genres_reviews['num_revs'] / top_genres_reviews['num_revs'].sum() * 100)]
        fig_top_genres_reviews_donut.update_traces(hoverinfo='text+percent', text=hover_text)
        fig_top_genres_reviews_donut.update_layout(
            plot_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            paper_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            font_color='white'  # White font color
        )
        st.plotly_chart(fig_top_genres_reviews_donut)


        # Apply sentiment analysis to descriptions and create a new column for sentiment
        top_data['sentiment'] = top_data['descs'].apply(get_sentiment)
        # Group by genre and sentiment to get the count
        genre_sentiment_counts_top = top_data.groupby(['Genre', 'sentiment']).size().reset_index(name='counts')

        # Define custom pastel colors with transparency for sentiment categories
        colors = {'positive': 'rgba(76,154,42, 0.5)',  # Light blue-green with 70% opacity
                'negative': 'rgba(255,0,0, 0.3)',  # Light orange with 70% opacity
                'neutral': 'rgba(0,0,255, 0.3)'}    # Light yellow with 70% opacity

        # Define border colors for each sentiment category
        border_colors = {'positive': '#00FF00',  # Dark green
                        'negative': '#FF0000',    # Dark red
                        'neutral': '#0000FF'}     # Dark blue

        # Plot the distribution of sentiment for each genre using a bar chart
        fig_genre_sentiment = px.bar(genre_sentiment_counts_top, x='Genre', y='counts', color='sentiment',
                                    title='Genre and Sentiment in Descriptions',
                                    labels={'Genre': 'Genre', 'counts': 'Count', 'sentiment': 'Sentiment'},
                                    color_discrete_map=colors)

        # Update the border colors based on the sentiment
        for sentiment, color in border_colors.items():
            fig_genre_sentiment.for_each_trace(lambda t: t.update(marker_line_color=color, marker_line_width=1)
                                                if t.name == sentiment else (),)

        fig_genre_sentiment.update_layout(
            plot_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            paper_bgcolor='rgb(31, 31, 31)',  # Dark gray background
            font_color='white'  # White font color
        )

        st.plotly_chart(fig_genre_sentiment)



        # Word Cloud
        text = ' '.join(filtered_data['descs'].astype(str))
        mask = np.array(Image.open(cloud_image_path))
        wordcloud = WordCloud(width=800, height=400, background_color='rgba(255, 255, 255, 0)', mode='RGBA',mask=mask).generate(text)

        # Display the word cloud directly
        st.image(wordcloud.to_array(), use_column_width=True)


        
    else:
        st.write('No data available for the top 5 genres.')
