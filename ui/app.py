import streamlit as st
import requests
import pandas as pd
import os

# Set the page title and layout
st.set_page_config(
    page_title="Document Search",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to enhance the UI
st.markdown(
    """
    <style>
    /* Center the main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Header style */
    .title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FFFFFF; /* Updated to white for better visibility */
    }
    /* Subheader style */
    .subheader {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333333;
    }
    /* Customize the expander */
    .streamlit-expanderHeader {
        font-size: 1.25rem;
        font-weight: bold;
        color: #333333;
    }
    /* Button style */
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.write(" ")
    st.title("Document Search Tool")
    st.markdown("""
        This tool uses **Retrieval-Augmented Generation (RAG)** to search and generate responses from a document repository.
        
        **How to use:**
        1. Enter your query in the text field.
        2. Choose a filter: Title, Context, or Chunk.
        3. Click **Search** to get results and an AI-generated answer!
    """)
    st.markdown("---")
    st.markdown("🚀 Powered by **FastAPI** and **Streamlit**.")

st.markdown("<h1 class='title'>📚 Document Search Tool</h1>", unsafe_allow_html=True)
st.markdown("""
    Use this tool to search through documents and get AI-generated answers in real-time.
    Just enter your query and select the appropriate filter to get started.
""")

# input fields for query and filter
query = st.text_input("🔍 Enter your query:", key="query", help="Type the question or search term.")
filter = st.selectbox(
    "Filter by:", 
    ["title", "context", "abstract"], 
    help="Choose the granularity of the search: Title, Context, or Chunk."
)

# Search button with interactive spinner
if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a query before searching.")
    else:
        with st.spinner("Searching for results..."):
            try:
                # backend get request
                response = requests.get("http://localhost:8000/search", params={"query": query, "filter": filter})
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    answer = data.get("answer", "No answer generated.")
                    embeddings = data.get("embeddings", [])

                    # answer generated
                    st.markdown("<h2 class='subheader'>📝 AI-Generated Answer</h2>", unsafe_allow_html=True)
                    st.success(answer)

                    # results retrieved
                    st.markdown("<h2 class='subheader'>📄 Search Results</h2>", unsafe_allow_html=True)
                    if results:
                        for idx, result in enumerate(results, 1):
                            with st.expander(f"Result {idx}: {result['title']}"):
                                st.write(f"**Relevance Score:** {result['relevance_score']:.2f}")
                                st.markdown(f"[📄 Open PDF]({result['link']})", unsafe_allow_html=True)
                    else:
                        st.warning("No matching results found.")

                    # embeddings visualization
                    st.markdown("<h2 class='subheader'>🌐 Embedding Visualization</h2>", unsafe_allow_html=True)
                    if embeddings:
                        import numpy as np
                        from sklearn.decomposition import PCA
                        import plotly.express as px

                        embeddings_np = np.array(embeddings)
                        titles = [result['title'] for result in results]

                        pca = PCA(n_components=3)
                        embeddings_3d = pca.fit_transform(embeddings_np)

                        df_vis = pd.DataFrame({
                            'x': embeddings_3d[:, 0],
                            'y': embeddings_3d[:, 1],
                            'z': embeddings_3d[:, 2],
                            'title': titles
                        })

                        fig = px.scatter_3d(
                            df_vis,
                            x='x',
                            y='y',
                            z='z',
                            text='title',
                            color='title',
                            title='Embeddings Visualization',
                            color_discrete_sequence=px.colors.qualitative.Set1,
                        )

                        fig.update_traces(marker=dict(size=6, symbol='circle', opacity=0.7))

                        fig.update_traces(
                            hovertemplate='<b>%{text}</b><br>x: %{x}<br>y: %{y}<br>z: %{z}',
                            textfont=dict(color='white')
                        )

                        fig.update_layout(
                            height=700,
                            margin=dict(l=0, r=0, b=0, t=50),
                            paper_bgcolor='black',
                            plot_bgcolor='black',
                            title_font=dict(color='white'),
                            scene=dict(
                                xaxis=dict(title='PCA 1', showgrid=True, color='white', title_font=dict(color='white')),
                                yaxis=dict(title='PCA 2', showgrid=True, color='white', title_font=dict(color='white')),
                                zaxis=dict(title='PCA 3', showgrid=True, color='white', title_font=dict(color='white')),
                            )
                        )

                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No embeddings available for visualization.")


                else:
                    st.error(f"Error: Backend returned status code {response.status_code}.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the backend: {e}")

st.markdown("---")
st.markdown("🔗 Built with [Streamlit](https://streamlit.io) | Backend by [FastAPI](https://fastapi.tiangolo.com) | Google/Flan-T5 ")
