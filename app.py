import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearchAgents
from data_loader import DataLoader

load_dotenv()

st.title("📚 Virtual Research Assistant")


# Retrieve API key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("GROQ_API_KEY is missing. Please set it in your .env file.")
    st.stop()

# Initialize
agents = ResearchAgents(groq_api_key)
data_loader = DataLoader()

# UI
query = st.text_input("Enter a research topic:")

if st.button("Search") and query:
    with st.spinner("Fetching and analyzing papers..."):
        arxiv_papers = data_loader.fetch_arxiv_papers(query)

        if not arxiv_papers:
            st.error("No papers found. Try another topic.")
        else:
            processed = []

            for paper in arxiv_papers:
                try:
                    st.write(f"🔍 Processing paper: {paper['title']}")
                    summary = agents.summarize_paper(paper['summary'])
                    adv_dis = agents.analyze_advantages_disadvantages(summary)

                    processed.append({
                        "title": paper["title"],
                        "link": paper["link"],
                        "summary": summary,
                        "advantages_disadvantages": adv_dis
                    })
                except Exception as e:
                    st.error(f"Error processing paper: {e}")

            st.subheader("Top Research Papers:")
            for i, paper in enumerate(processed, 1):
                st.markdown(f"### {i}. {paper['title']}")
                st.markdown(f"🔗 [Read Paper]({paper['link']})")
                st.write(f"**Summary:** {paper['summary']}")
                st.write(f"**Advantages/Disadvantages:**\n{paper['advantages_disadvantages']}")
                st.markdown("---")
