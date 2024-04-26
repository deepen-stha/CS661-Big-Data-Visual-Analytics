# Audio Aura

In the dynamic realm of music, knowing what resonates with audiences is crucial. Our data-driven exploration helps us uncover trends and insights driving musical achievements. With innovative analytics and visualization, we navigate through genre preferences, artist popularity, musical scales, and emerging trends.

<br>

![t0](https://github.com/deepen-stha/CS661-Big-Data-Visual-Analytics/assets/105813454/fc05fb63-82a4-46a1-a53d-455d38d7db45)

## Contributors

1. **Akash Shivaji Varude**<br>
   Album Analysis
1. **Darshan Jain**<br>
   Region-based Insights
1. **Deepen Shrestha**<br>
   KNN Music Recommendation
1. **Indraneel Rajeevan**<br>
   Music Scale Analysis
1. **Nitish Kumar**<br>
   Top-k Songs
1. **Pankaj Siddharth Nandeshwar**<br>
   International Popularity
1. **Pranjal Maroti Nandeshwar**<br>
   Genre Fusion
1. **Shaurya Agarwal**<br>
   Songs' Properties Inter-relation

<br>

---

# International Popularity

For a given region, the plots show:

- The top ‘m’ genres in that region
- The top ‘k’ artists for the given genre
- Total streams for the given genre/artists (Hover based)

<br>

![t1](https://github.com/deepen-stha/CS661-Big-Data-Visual-Analytics/assets/105813454/4a0565b6-e002-4f37-99fd-4e99490c25c2)

<br>

---

# Region-based Insights

First map shows the trend for “explicitness”

- For the last few years trend has been increasing for explicitness in songs, but not in every region
- This map depicts the percentage of songs that have explicit content over the countries (67 countries)
- With a variable of taking the top - k% songs with most streams.

The second map shows the trend for “explicitness” for time being:

- The reference of global trend is given with red dotted line
- The other lines are for a country over the years
- This also shows the growth over the years Global value is around 42%

<br>

![t2](https://github.com/deepen-stha/CS661-Big-Data-Visual-Analytics/assets/105813454/b106a4c4-bc4e-4b3c-b71f-80aa89ba7d41)

<br>

---

# Genre Fusion

The bubble plot captures the following insights:

- Genre fusion popularity by country and year
- Assists label companies in tracking current trends
- Reflects global interest in genre fusion

<br>

![t3](https://github.com/deepen-stha/CS661-Big-Data-Visual-Analytics/assets/105813454/9ad935e7-11af-480b-9515-150272987b71)

<br>

---

# Album Analysis

- Average ratings
- Number of ratings
- Sentiment analysis
- Word cloud
- Custom functionalities

<br>

![t4](https://github.com/deepen-stha/CS661-Big-Data-Visual-Analytics/assets/105813454/887ef550-5c30-4fb8-ae29-824c7c3aa372)

<br>

---

# Top 100 Songs Annually (2013-2023)

- Provides insight into the most popular songs annually.
- Reflects trends and preferences in music consumption over the years.
- Indicates which artists have a larger share of the streaming market.
- Offers insights into listener preferences for explicit content.
- Highlights trends in song length and potential shifts in audience preferences.

<br>

![t5 1](https://github.com/deepen-stha/CS661-Big-Data-Visual-Analytics/assets/105813454/c77cfacf-e6e4-43b6-a794-da79e9825324)

<br>

---

# All time Top-5000 Songs by Genre

- Provides insight of the Top-5000 songs of all time by Genre.
- Acousticness Vs Speechiness
- Feature Comparison
- Tempo Vs Valence
- Highlights trends in song length and potential shifts in audience preferences.

<br>

![t5 2](https://github.com/deepen-stha/CS661-Big-Data-Visual-Analytics/assets/105813454/bfd6aef0-52ed-4143-beb9-10d7bedde1a5)

<br>

---

# Songs' Properties Inter-relation (Mix & Master)

- Select a specific country and year
- Apply filters (Stream and Popularity)
- Additional insights via Wiscus Plot

<br>

![t6](https://github.com/deepen-stha/CS661-Big-Data-Visual-Analytics/assets/105813454/ec92b59e-483c-4dff-adce-62ca5a4acc1b)

<br>

---

# Music Scale Analysis

- Visualize the relationships between a chosen Song Property and all the Music Scales
- Visualize the relationship between a chosen Song Property and a chosen Music Scale
- Visualize the relationships between a chosen Music Scale and any subset of the Music Properties
- Customize the Music Notation

<br>

![t7](https://github.com/deepen-stha/CS661-Big-Data-Visual-Analytics/assets/105813454/7b063798-6f3e-4f64-b8c7-618aa22a3615)

<br>

---

# KNN Music Recommendation

- Recommending songs from our data to customers on the basis of Danceability, Energy, Valence, Tempo.
- Minimum recommendation user can select is 2 and maximum it can go to 6. Default value will be 5.
- The final predicted value is then plotted using matrix of scatter plot and histogram (pairplot or scatterplot matrix).
- Support for dynamic SQL querying

<br>

![t8](https://github.com/deepen-stha/CS661-Big-Data-Visual-Analytics/assets/105813454/d7f434a8-f689-4591-8f9f-f39bb9b92253)

<br>

---

# Usage

**Development Environment:**<br>
Execute the given `setup.bat` or run the command `pip install -r requirements.txt`

**Run via Localhost:**<br>
Execute the given `run.bat` or run the command `streamlit run Home.py`

**Deployed Application:**<br>
https://cs661-big-data-visual-analytics-group1.streamlit.app/

<br>
