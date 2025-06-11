import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from agents import ResearchAgents
from data_loader import DataLoader
from report_generator import ReportGenerator
import logging
from io import BytesIO
import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

# --- Must be first ---
st.set_page_config(page_title="AI Research Assistant", layout="wide")

# --- Inject custom CSS for fancy UI ---
def inject_custom_css():
    st.markdown("""
        <style>
            body {
                background-image: url('istockphoto-1333222351-612x612.jpg');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-position: center;
            }
            .block-container {
                backdrop-filter: blur(8px);
                background-color: rgba(0, 0, 0, 0.6);
                border-radius: 10px;
                padding: 2rem;
                color: white;
            }
            h1, h2, h3 {
                color: #00e1ff !important;
                font-weight: bold;
                text-shadow: 1px 1px 2px black;
            }
            .stTextInput>div>div>input {
                color: white;
            }
            .stButton>button {
                background: linear-gradient(to right, #00c6ff, #0072ff);
                color: white;
                border-radius: 10px;
                font-weight: bold;
                padding: 0.6rem 1.4rem;
                transition: all 0.3s ease-in-out;
                animation: glow 1.8s infinite alternate;
            }
            .stButton>button:hover {
                transform: scale(1.05);
                background: linear-gradient(to right, #0094ff, #005bb5);
            }
            @keyframes glow {
                from { box-shadow: 0 0 5px #00c6ff; }
                to { box-shadow: 0 0 20px #0072ff; }
            }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- Setup logging and env ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# --- API key check ---
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("❌ GROQ_API_KEY is missing. Please set it in your .env file.")
    st.stop()

# --- Core components ---
agents = ResearchAgents(groq_api_key)
data_loader = DataLoader()
report_gen = ReportGenerator()

# --- Session state setup ---
if "processed" not in st.session_state:
    st.session_state.processed = []
    st.session_state.all_summaries = []
if "query" not in st.session_state:
    st.session_state.query = ""

# --- Tabs for Navigation ---
tabs = st.tabs(["🏠 Home", "📑 Results", "📄 Summarized Paper", "📊 Literature Survey"])

# --- HOME Tab ---
with tabs[0]:
    st.title(" 🤖 MARA - Multi Agent Research Assistant ")
    st.markdown("<h3 style='text-align: center;'>Your AI-Powered Research Companion</h3>", unsafe_allow_html=True)


    with st.sidebar:
        st.markdown("## 💡 Suggestions")
        if st.session_state.query:
            st.markdown(f"- Explore **{st.session_state.query} + Applications**")
            st.markdown(f"- Compare **{st.session_state.query}** with Deep Learning")
            st.markdown("- Investigate recent breakthroughs and future challenges.")
        else:
            st.info("Search a topic to see personalized suggestions.")

    with st.form("search_form"):
        query = st.text_input("🔍 Enter a research topic:")
        submitted = st.form_submit_button("Search")

    if submitted and query:
        st.session_state.query = query
        with st.spinner("⏳ Fetching and analyzing papers..."):
            arxiv_papers = data_loader.fetch_arxiv_papers(query)

            if not arxiv_papers:
                st.error("❌ No papers found.")
            else:
                st.session_state.processed = []
                st.session_state.all_summaries = []

                for paper in arxiv_papers:
                    try:
                        st.success(f"📄 {paper['title']}")
                        summary = agents.summarize_paper(paper['summary'])
                        quality = agents.review_quality(summary)
                        recs = agents.recommend_topics(summary)

                        st.session_state.processed.append({
                            "title": paper["title"],
                            "link": paper["pdf_url"],
                            "summary": summary,
                            "quality_review": quality,
                            "recommendations": recs,
                            
                        })
                        st.session_state.all_summaries.append(summary)
                    except Exception as e:
                        logger.error(f"Error: {e}")
                        st.error(f"Processing error: {e}")

# --- RESULTS Tab ---
with tabs[1]:
    if st.session_state.processed:
        st.subheader("📘 Top Results")
        feedback_data = []
        for i, paper in enumerate(st.session_state.processed, 1):
            with st.expander(f"📄 {paper['title']}"):
                st.markdown(f"🔗 [Read Paper]({paper['link']})")
                st.markdown(f"**🧾 Summary:** {paper['summary']}")
                st.markdown(f"**✅ Quality Review:** {paper['quality_review']}")
                st.markdown(f"**🧠 Recommendations:** {paper['recommendations']}")
                feedback = st.text_input("💬 Leave feedback:", key=f"fb_{i}")
                if feedback:
                    feedback_data.append({"title": paper["title"], "feedback": feedback})

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if feedback_data and st.button("💾 Save Feedback"):
                try:
                    pd.DataFrame(feedback_data).to_csv("user_feedback.csv", index=False)
                    st.success("✅ Feedback saved.")
                except Exception as e:
                    logger.error(e)
                    st.error("Failed to save feedback.")
    else:
        st.info("Search a topic first to see results.")

# --- IEEE PAPER Tab ---
with tabs[2]:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚙️ Generate Pdf "):
            combined = "\n\n".join(st.session_state.all_summaries)
            if not combined.strip():
                st.error("❌ No summaries available.")
            else:
                ieee = agents.generate_new_paper(combined)
                if "failed" in ieee.lower() or not ieee.strip():
                    ieee = "⚠️ Fallback: Failed to generate real content."

                st.subheader("📄 Pdf Output")
                st.code(ieee)
                ieee_path = report_gen.generate_ieee_format_doc(ieee)
                if ieee_path and os.path.exists(ieee_path):
                    st.session_state.ieee_path = ieee_path
                    st.success("✅ Paper generated!")

        if "ieee_path" in st.session_state:
            try:
                with open(st.session_state.ieee_path, "rb") as f:
                    st.download_button("📥 Download Paper", data=f, file_name="summarized_paper.pdf")
            except Exception as e:
                logger.error(e)
                st.error("Download failed.")

# --- LITERATURE SURVEY TAB ---
with tabs[3]:
    st.subheader("📊 Comparative Literature Survey Table")
    if st.session_state.processed:
        rows = []
        for p in st.session_state.processed:
            rows.append({
                "Paper Title": p['title'],
                "Abstract": p['summary'],
                "Introduction": p['summary'],
                "Related Research": p['recommendations'],
                "Methodology": p['summary'],
                "Experiment": p['summary'],
                "Result": p['quality_review'],
                "Future Work": p['recommendations'],
                "Conclusion": p['summary']
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", data=csv, file_name="literature_survey.csv")

        with col2:
            buffer = report_gen.generate_lit_survey_pdf(df)
            if buffer:
                st.download_button("📥 Download PDF", data=buffer, file_name="literature_survey.pdf")
    else:
        st.info("Please search a topic first.")