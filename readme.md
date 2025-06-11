## 📚 MARA - Multi-Agent Research Assistant

**MARA** is an AI-powered virtual research assistant designed to automate and enhance the scientific literature review process. Built using a multi-agent architecture, MARA fetches research papers, summarizes them intelligently, analyzes quality, and generates a well-structured IEEE-style report — complete with formatted text, citations, and optional literature survey tables.

### 🚀 Key Features

* 🔍 **Topic-Based Paper Retrieval**
  Fetches recent and relevant papers from arXiv based on user queries.

* 🧠 **Multi-Agent Architecture**
  Includes dedicated agents for summarization, quality review, and topic recommendation using LLMs.

* 🧾 **IEEE-Style Report Generation**
  Automatically formats a clean research report with bold section headings and academic tone.

* 📑 **Literature Survey Table**
  Compiles multiple papers into a structured, downloadable table (CSV or PDF).

* 🎨 **Styled Streamlit UI**
  A visually engaging frontend with suggestion tips, expandable result panels, and interactive downloads.

### 🧱 Architecture Overview

* **Frontend:** Streamlit-based web interface with custom CSS styling.
* **Backend:** Python services using LLMs for summarization, critique, and formatting.
* **Agents:**

  * `Scholar Agent`: Summarizes research papers
  * `Critique Agent`: Reviews quality of summaries
  * `Synthesis Agent`: Recommends future research directions
  * `Report Generator`: Produces IEEE-style documents

### 📂 Folder Structure

```
MARA/
├── app.py                    # Streamlit frontend
├── agents.py                # LLM multi-agent logic
├── data_loader.py           # ArXiv API and paper fetching
├── report_generator.py      # PDF and literature table generation
├── .env                     # API keys
├── requirements.txt         # Required Python libraries
└── README.md                # GitHub description
```

### 🔧 Technologies Used

* **Python 3.9+**
* **Streamlit**
* **FPDF**
* **LangChain / AutoGen**
* **arXiv API**
* **OpenAI / Groq LLMs**

### 📄 Output Example

MARA generates an IEEE-style report with the following structure:

* Title
* Abstract
* Keywords
* Introduction
* Related Work
* Methodology
* Experimental Results
* Discussion
* Conclusion and Future Work

### 📦 Installation

```bash
git clone https://github.com/yourusername/MARA.git
cd MARA
pip install -r requirements.txt
streamlit run app.py
```

> Make sure to add your GROQ or OpenAI API key to a `.env` file as `GROQ_API_KEY=your-key-here`
