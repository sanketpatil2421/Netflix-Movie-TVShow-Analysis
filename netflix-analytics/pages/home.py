import streamlit as st

def show():
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Netflix Data Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Dive deep into Netflix content insights with interactive visualizations and AI-powered analytics.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Explore Dashboard", key="explore_dashboard"):
            st.session_state.selected_page = "Dashboard"
            st.rerun()
    with col2:
        if st.button("Upload Dataset", key="upload_dataset"):
            st.session_state.selected_page = "Dashboard"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Check if data is available for trends
    if 'df' in st.session_state:
        df = st.session_state.df

        # Most Watched Trends (based on recent releases and popularity)
        st.header("🎬 Trending Movies & TV Shows")

        # Most Recent Movies
        st.subheader("Latest Movies")
        recent_movies = df[(df['type'] == 'Movie') & (df['release_year'] >= 2020)].sort_values('release_year', ascending=False).head(5)
        for _, movie in recent_movies.iterrows():
            st.write(f"🎥 **{movie['title']}** ({movie['release_year']}) - {movie['rating']}")

        # Most Recent TV Shows
        st.subheader("Latest TV Shows")
        recent_tv = df[(df['type'] == 'TV Show') & (df['release_year'] >= 2020)].sort_values('release_year', ascending=False).head(5)
        for _, show in recent_tv.iterrows():
            st.write(f"📺 **{show['title']}** ({show['release_year']}) - {show['rating']}")

        # Popular Genres
        st.subheader("Popular Genres")
        genres = df['listed_in'].str.split(', ').explode().value_counts().head(5)
        for genre, count in genres.items():
            st.write(f"🎭 **{genre}**: {count} titles")

    else:
        # Animated poster carousel (simulated with images)
        st.subheader("Featured Content")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://via.placeholder.com/300x400/ff0000/ffffff?text=Stranger+Things", caption="Stranger Things")
        with col2:
            st.image("https://via.placeholder.com/300x400/ff0000/ffffff?text=The+Crown", caption="The Crown")
        with col3:
            st.image("https://via.placeholder.com/300x400/ff0000/ffffff?text=Money+Heist", caption="Money Heist")

    st.markdown("""
    <style>
    .poster-carousel {
        display: flex;
        overflow-x: auto;
        gap: 20px;
        padding: 20px 0;
    }
    .poster {
        flex-shrink: 0;
        width: 200px;
        height: 300px;
        background-color: #e50914;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        transition: transform 0.3s ease;
    }
    .poster:hover {
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)
