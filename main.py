from data_loader import DataLoader
from report_generator import ReportGenerator

def main():
    query = "multi-agent systems"
    loader = DataLoader()
    generator = ReportGenerator()

    papers = loader.fetch_arxiv_papers(query)
    ieee_text = ""

    for i, paper in enumerate(papers):
        title = paper["title"]
        summary = paper["summary"]
        link = paper["link"]
        arxiv_id = link.split('/')[-1]

        ieee_text += f"Title:\n{title}\n\n"
        ieee_text += f"Abstract:\n{summary}\n\n"
        ieee_text += f"Keywords:\nMulti-agent, AI, research\n\n"
        ieee_text += f"Introduction:\nThis paper explores {title.lower()}.\n\n"
        ieee_text += f"Related Work:\nPrior works on {query.lower()} are discussed.\n\n"
        ieee_text += f"Literature Survey:\nVarious strategies and architectures are reviewed.\n\n"
        ieee_text += f"Methodology:\n• The authors propose a unique method.\n• Simulation-based evaluation conducted.\n• Multi-agent interactions modeled.\n\n"
        ieee_text += f"Experimental Results:\nObservations are documented and evaluated.\n\n"
        ieee_text += f"Discussion:\nBenefits and challenges are discussed.\n\n"
        ieee_text += f"Conclusion and Future Work:\nThe paper concludes with suggestions for future exploration.\n\n"

    output_path = "ieee_research_paper.pdf"
    generator.generate_ieee_format_doc(ieee_text, output_path)

if __name__ == "__main__":
    main()
