import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.title("💡 AI-Generated Insights")

    # Check if data is available
    if 'df' not in st.session_state:
        st.warning("Please upload a dataset in the Dashboard first.")
        return

    df = st.session_state.df

    # Generate insights
    insights = []

    # Genre popularity trend
    genre_trend = df['listed_in'].str.split(', ').explode().value_counts().head(5)
    insights.append(f"📈 **Genre Popularity**: The top genres are {', '.join(genre_trend.index)}. {genre_trend.index[0]} leads with {genre_trend.iloc[0]} titles.")

    # Countries producing most content
    country_content = df['country'].value_counts().head(5)
    insights.append(f"🌍 **Top Content Producers**: {', '.join(country_content.index)} produce the most content, with {country_content.index[0]} leading at {country_content.iloc[0]} titles.")

    # Most common genre combination
    genre_combos = df['listed_in'].value_counts().head(5)
    insights.append(f"🔗 **Common Genre Combinations**: The most frequent genre combo is '{genre_combos.index[0]}' appearing in {genre_combos.iloc[0]} titles.")

    # Year-wise content growth
    yearly_growth = df.groupby('release_year').size().pct_change().mean() * 100
    insights.append(f"📊 **Content Growth**: Average yearly growth in content addition is {yearly_growth:.1f}%.")

    # Additional insights
    movie_ratio = (df['type'] == 'Movie').mean() * 100
    insights.append(f"🎬 **Content Type Ratio**: {movie_ratio:.1f}% of content are Movies, {100-movie_ratio:.1f}% are TV Shows.")

    avg_duration = df[df['type'] == 'Movie']['duration'].str.extract(r'(\d+)').astype(float).mean().iloc[0]
    insights.append(f"⏱️ **Average Movie Duration**: Movies average {avg_duration:.0f} minutes in length.")

    # Display insights with animations
    for i, insight in enumerate(insights):
        st.markdown(f"""
        <div class="insight-card" style="animation-delay: {i*0.2}s;">
            <p>{insight}</p>
        </div>
        """, unsafe_allow_html=True)

    # Animated chart: Genre distribution over time
    st.header("Genre Distribution Over Time")
    df['year_added'] = df['date_added'].dt.year
    genre_year = df.groupby(['year_added', 'listed_in']).size().reset_index(name='count')
    genre_year = genre_year.sort_values('count', ascending=False).groupby('year_added').head(5)

    fig = px.bar(genre_year, x='year_added', y='count', color='listed_in', title="Top Genres by Year Added",
                 color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig, use_container_width=True)

    # Month-Year Selector for Releases
    st.header("Content Released by Month-Year")
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Year", options=sorted(df['date_added'].dt.year.dropna().astype(int).unique(), reverse=True), key="insights_year_selector")
    with col2:
        selected_month = st.selectbox("Select Month", options=[1,2,3,4,5,6,7,8,9,10,11,12], format_func=lambda x: pd.to_datetime(x, format='%m').strftime('%B'), key="insights_month_selector")

    # Filter by selected month-year
    month_year_filtered = df[df['date_added'].notna() & (df['date_added'].dt.year == selected_year) & (df['date_added'].dt.month == selected_month)]

    if not month_year_filtered.empty:
        st.subheader(f"Movies and TV Shows Released in {pd.to_datetime(f'{selected_year}-{selected_month:02d}').strftime('%B %Y')}")
        st.dataframe(month_year_filtered[['title', 'type', 'director', 'country', 'date_added']].reset_index(drop=True))
        st.metric("Total Titles Released", len(month_year_filtered))

        # New Feature: Content Rating Distribution
        st.subheader("Content Rating Distribution")
        rating_dist = month_year_filtered['rating'].value_counts().reset_index()
        rating_dist.columns = ['Rating', 'Count']
        fig_rating = px.bar(rating_dist, x='Rating', y='Count', title="Content Ratings",
                           color_discrete_sequence=['#e50914'])
        st.plotly_chart(fig_rating, use_container_width=True)

        # Additional Charts for Filtered Data
        st.header("Filtered Data Charts")

        col1, col2 = st.columns(2)

        with col1:
            # TV Shows/Movies Chart
            type_dist_filtered = month_year_filtered['type'].value_counts()
            fig_type = px.pie(values=type_dist_filtered.values, names=type_dist_filtered.index, title="Movies vs TV Shows Distribution",
                             color_discrete_sequence=['#e50914', '#333333'])
            st.plotly_chart(fig_type, use_container_width=True)

            # Country Chart
            country_count_filtered = month_year_filtered['country'].value_counts().head(10)
            fig_country = px.bar(country_count_filtered, x=country_count_filtered.index, y=country_count_filtered.values,
                               title="Top 10 Countries by Content Count", color_discrete_sequence=['#e50914'])
            st.plotly_chart(fig_country, use_container_width=True)

        with col2:
            # Director Chart
            directors_filtered = month_year_filtered['director'].dropna().str.split(', ').explode().value_counts().head(10)
            fig_dir = px.bar(directors_filtered, x=directors_filtered.index, y=directors_filtered.values, title="Top Directors",
                           color_discrete_sequence=['#e50914'])
            st.plotly_chart(fig_dir, use_container_width=True)

    else:
        st.info(f"No content was added in {pd.to_datetime(f'{selected_year}-{selected_month:02d}').strftime('%B %Y')}.")
