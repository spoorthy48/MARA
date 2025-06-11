import os
import requests
import fitz  # PyMuPDF
import arxiv

class DataLoader:
    def __init__(self, download_dir="downloads"):
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def fetch_arxiv_papers(self, query, max_results=5):
        print(f"Searching arXiv for query: {query}")
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        results = []
        for result in search.results():
            paper = {
                "title": result.title,
                "summary": result.summary,
                "pdf_url": result.pdf_url,
                "authors": [author.name for author in result.authors]
            }
            results.append(paper)
        return results

    def download_pdf(self, url, title):
        filename = title.replace(" ", "_") + ".pdf"
        filepath = os.path.join(self.download_dir, filename)

        if not os.path.exists(filepath):
            response = requests.get(url)
            with open(filepath, "wb") as f:
                f.write(response.content)
        return filepath

    def extract_diagrams(self, pdf_path):
        doc = fitz.open(pdf_path)
        diagram_dir = pdf_path.replace(".pdf", "_images")
        os.makedirs(diagram_dir, exist_ok=True)

        diagrams = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            images = page.get_images(full=True)

            print(f"Page {page_num + 1} has {len(images)} images")

            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                image_filename = f"page{page_num+1}_img{img_index+1}.png"
                image_path = os.path.join(diagram_dir, image_filename)

                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)

                diagrams.append({
                    "image_path": image_path,
                    "caption": f"Diagram from page {page_num+1}, image {img_index+1}",
                    "section": "Experimental Results"
                })

                print(f"Saved image: {image_path}")

        return diagrams
