import streamlit as st

def show():
    st.title("About Netflix Data Analytics")

    st.markdown("""
    <div class="card">
        <h3>Project Overview</h3>
        <p>This Netflix Data Analytics Dashboard is a comprehensive tool for exploring and visualizing Netflix content data. Built with Streamlit and powered by Python, it provides interactive charts, filters, and AI-generated insights to help users understand trends in Netflix's vast library.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <h4>Features</h4>
            <ul>
                <li>📊 Interactive dashboards with multiple chart types</li>
                <li>🔍 Advanced filtering capabilities</li>
                <li>🤖 AI-generated insights</li>
                <li>📱 Responsive design for all devices</li>
                <li>🎨 Netflix-inspired UI with smooth animations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h4>Technologies Used</h4>
            <ul>
                <li>🐍 Python & Streamlit</li>
                <li>📈 Plotly for visualizations</li>
                <li>🧹 Pandas for data processing</li>
                <li>☁️ WordCloud for text analysis</li>
                <li>🎨 Custom CSS for styling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.header("Developer")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://via.placeholder.com/150x150/e50914/ffffff?text=DEV", caption="Developer Avatar")
    with col2:
        st.markdown("""
        <div class="card">
            <h4>AI Assistant</h4>
            <p>Built by an advanced AI assistant specializing in data analytics and web development.</p>
            <p>Passionate about creating beautiful, functional data visualization tools.</p>
        </div>
        """, unsafe_allow_html=True)

    st.header("Connect")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<a href="#" style="text-decoration: none;"><button style="background-color: #e50914; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; transition: all 0.3s;">GitHub</button></a>', unsafe_allow_html=True)
    with col2:
        st.markdown('<a href="#" style="text-decoration: none;"><button style="background-color: #e50914; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; transition: all 0.3s;">LinkedIn</button></a>', unsafe_allow_html=True)
    with col3:
        st.markdown('<a href="#" style="text-decoration: none;"><button style="background-color: #e50914; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; transition: all 0.3s;">Twitter</button></a>', unsafe_allow_html=True)
