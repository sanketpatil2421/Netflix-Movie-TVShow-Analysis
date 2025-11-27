import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def show():
    st.title("📊 Netflix Data Analytics Dashboard")

    # File upload
    uploaded_file = st.file_uploader("Upload Netflix CSV Dataset", type="csv")

    if uploaded_file is not None:
        # Load and process data
        encodings = ['utf-8', 'latin1', 'cp1252']
        df = None
        for enc in encodings:
            try:
                df = pd.read_csv(uploaded_file, encoding=enc)
                break
            except UnicodeDecodeError:
                continue
        if df is None:
            st.error("Unable to read the CSV file. Please ensure it is a valid CSV with supported encoding (UTF-8, Latin1, or CP1252).")
            return
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')

        # Store in session state
        st.session_state.df = df

        # Filters
        st.sidebar.header("Filters")
        type_filter = st.sidebar.multiselect("Type", options=df['type'].unique(), default=df['type'].unique())
        country_filter = st.sidebar.multiselect("Country", options=df['country'].dropna().unique(), default=[])
        genre_filter = st.sidebar.multiselect("Genre", options=df['listed_in'].str.split(', ').explode().unique(), default=[])
        year_filter = st.sidebar.slider("Release Year", int(df['release_year'].min()), int(df['release_year'].max()), (int(df['release_year'].min()), int(df['release_year'].max())))

        # Apply filters
        filtered_df = df[df['type'].isin(type_filter)]
        if country_filter:
            filtered_df = filtered_df[filtered_df['country'].isin(country_filter)]
        if genre_filter:
            filtered_df = filtered_df[filtered_df['listed_in'].str.contains('|'.join(genre_filter))]
        filtered_df = filtered_df[(filtered_df['release_year'] >= year_filter[0]) & (filtered_df['release_year'] <= year_filter[1])]

        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Movies", len(filtered_df[filtered_df['type'] == 'Movie']))
        with col2:
            st.metric("Total TV Shows", len(filtered_df[filtered_df['type'] == 'TV Show']))
        with col3:
            st.metric("Total Titles", len(filtered_df))
        with col4:
            avg_rating = filtered_df['rating'].mode().iloc[0] if not filtered_df['rating'].mode().empty else "N/A"
            st.metric("Most Common Rating", avg_rating)

        # Charts
        st.header("Interactive Charts")

        col1, col2 = st.columns(2)

        with col1:
            # Bar Chart: Content by Year
            yearly_content = filtered_df.groupby('release_year').size().reset_index(name='count')
            fig_bar = px.bar(yearly_content, x='release_year', y='count', title="Content Added by Year",
                           color_discrete_sequence=['#e50914'])
            st.plotly_chart(fig_bar, use_container_width=True)

            # Pie Chart: Type Distribution
            type_dist = filtered_df['type'].value_counts()
            fig_pie = px.pie(values=type_dist.values, names=type_dist.index, title="Content Type Distribution",
                           color_discrete_sequence=['#e50914', '#333333'])
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Line Chart: Content added over time
            monthly_content = filtered_df.groupby(filtered_df['date_added'].dt.to_period('M')).size().reset_index(name='count')
            monthly_content['date_added'] = monthly_content['date_added'].astype(str)
            fig_line = px.line(monthly_content, x='date_added', y='count', title="Content Added Over Time",
                             color_discrete_sequence=['#e50914'])
            st.plotly_chart(fig_line, use_container_width=True)

            # Top 10 Countries
            country_count = filtered_df['country'].value_counts().head(10)
            fig_country = px.bar(country_count, x=country_count.index, y=country_count.values,
                               title="Top 10 Countries by Content Count", color_discrete_sequence=['#e50914'])
            st.plotly_chart(fig_country, use_container_width=True)

        # Genre Analysis
        st.header("Genre Analysis")
        col1, col2 = st.columns(2)

        with col1:
            # Popular Genres
            genres = filtered_df['listed_in'].str.split(', ').explode().value_counts().head(10)
            fig_genre = px.bar(genres, x=genres.index, y=genres.values, title="Popular Genres",
                             color_discrete_sequence=['#e50914'])
            st.plotly_chart(fig_genre, use_container_width=True)

        with col2:
            # Word Cloud for descriptions
            text = ' '.join(filtered_df['description'].dropna().head(100))
            wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Reds').generate(text)
            fig_wc, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig_wc)

        # Director/Actor Analysis
        st.header("Director & Actor Analysis")
        col1, col2 = st.columns(2)

        with col1:
            # Top Directors
            directors = filtered_df['director'].dropna().str.split(', ').explode().value_counts().head(10)
            fig_dir = px.bar(directors, x=directors.index, y=directors.values, title="Top Directors",
                           color_discrete_sequence=['#e50914'])
            st.plotly_chart(fig_dir, use_container_width=True)

        with col2:
            # Top Actors
            actors = filtered_df['cast'].dropna().str.split(', ').explode().value_counts().head(10)
            fig_act = px.bar(actors, x=actors.index, y=actors.values, title="Top Actors",
                           color_discrete_sequence=['#e50914'])
            st.plotly_chart(fig_act, use_container_width=True)

        # All Directors Chart
        st.header("All Directors Overview")
        all_directors = filtered_df['director'].dropna().str.split(', ').explode().value_counts().reset_index()
        all_directors.columns = ['Director', 'Content Count']
        fig_all_dir = px.bar(all_directors, x='Director', y='Content Count', title="All Directors by Content Count",
                           color_discrete_sequence=['#e50914'])
        fig_all_dir.update_xaxes(tickangle=45)
        st.plotly_chart(fig_all_dir, use_container_width=True)

        # Month-Year Selector for Releases
        st.header("Content Uploaded by Month-Year")
        col1, col2 = st.columns(2)
        with col1:
            selected_year = st.selectbox("Select Year", options=sorted(filtered_df['date_added'].dt.year.dropna().astype(int).unique(), reverse=True), key="year_selector")
        with col2:
            selected_month = st.selectbox("Select Month", options=[1,2,3,4,5,6,7,8,9,10,11,12], format_func=lambda x: pd.to_datetime(x, format='%m').strftime('%B'), key="month_selector")

        # Filter by selected month-year
        month_year_filtered = filtered_df[
            (filtered_df['date_added'].dt.year == selected_year) &
            (filtered_df['date_added'].dt.month == selected_month)
        ]

        if not month_year_filtered.empty:
            st.subheader(f"Movies and TV Shows Released in {pd.to_datetime(f'{selected_year}-{selected_month:02d}').strftime('%B %Y')}")
            st.dataframe(month_year_filtered[['title', 'type', 'director', 'country', 'date_added']].reset_index(drop=True))
            st.metric("Total Titles Released", len(month_year_filtered))

            # New Feature: Summary Stats for Selected Month-Year
            st.subheader("Summary Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Movies", len(month_year_filtered[month_year_filtered['type'] == 'Movie']))
            with col2:
                st.metric("TV Shows", len(month_year_filtered[month_year_filtered['type'] == 'TV Show']))
            with col3:
                top_genre = month_year_filtered['listed_in'].str.split(', ').explode().value_counts().idxmax() if not month_year_filtered.empty else "N/A"
                st.metric("Top Genre", top_genre)
        else:
            st.info(f"No content was added in {pd.to_datetime(f'{selected_year}-{selected_month:02d}').strftime('%B %Y')}.")

        # Movie/TV Show Names
        st.header("Movie & TV Show Names")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Movies")
            movies = filtered_df[filtered_df['type'] == 'Movie']['title'].head(10)
            for i, title in enumerate(movies, 1):
                st.write(f"{i}. {title}")

        with col2:
            st.subheader("TV Shows")
            tv_shows = filtered_df[filtered_df['type'] == 'TV Show']['title'].head(10)
            for i, title in enumerate(tv_shows, 1):
                st.write(f"{i}. {title}")

        # Special Column: Release Only Year
        st.header("Release Only Year")
        selected_release_year = st.selectbox("Select Release Year", options=sorted(filtered_df['release_year'].dropna().astype(int).unique(), reverse=True), key="release_year_selector")

        # Filter by selected release year
        release_year_filtered = filtered_df[filtered_df['release_year'] == selected_release_year]

        if not release_year_filtered.empty:
            st.subheader(f"Movies and TV Shows Released in {selected_release_year}")
            st.dataframe(release_year_filtered.reset_index(drop=True))
            st.metric("Total Titles Released", len(release_year_filtered))
        else:
            st.info(f"No content was released in {selected_release_year}.")

        # Longest Descriptions
        st.header("Top 10 Longest Descriptions")
        filtered_df['desc_length'] = filtered_df['description'].str.len()
        longest_desc = filtered_df.nlargest(10, 'desc_length')['description']
        for i, desc in enumerate(longest_desc, 1):
            st.write(f"{i}. {desc[:100]}...")

    else:
        st.info("Please upload a Netflix CSV dataset to get started.")
