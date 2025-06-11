from fpdf import FPDF 
import re
import pandas as pd
from io import BytesIO
import os
from PIL import Image

class CustomPDF(FPDF):
    def __init__(self, title=None):
        super().__init__('P', 'mm', 'A4')
        self.paper_title = title if title else "Summarized Research Paper"
        self.header_rendered = False

    def header(self):
        if self.page_no() == 1 and not self.header_rendered:
            self.set_font("Arial", 'B', 12)
            self.set_x(10)
            max_width = 190
            words = self.paper_title.split()
            line = ''
            for word in words:
                if self.get_string_width(line + ' ' + word) > max_width:
                    self.cell(0, 10, line.strip(), ln=True, align='C')
                    line = word
                else:
                    line += ' ' + word
            if line:
                self.cell(0, 10, line.strip(), ln=True, align='C')
            self.ln(2)
            self.header_rendered = True

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f"Page {self.page_no()}", align='C')


class ReportGenerator:
    def __init__(self):
        self.figure_count = 1
        self.table_count = 1

    def _clean_text(self, text):
        if not text:
            return ""
        replacements = {
            '—': '-', '–': '-', '‘': "'", '’': "'", '“': '"', '”': '"', '…': '...', '•': '-'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text.strip()

    def _format_bullet_points(self, text, count=5):
        if not text:
            return ""
        text = text.replace("•", "-")
        sentences = re.split(r'(?<=[.!?]) +', text.strip())
        sentences = [s.strip() for s in sentences if s.strip()]
        bullets = sentences[:count] + [""] * (count - len(sentences))
        return "\n".join([f"- {self._clean_text(s)}" for s in bullets if s])

    def _extract_title(self, lines):
        for line in lines:
            if line.strip().lower().startswith("title:"):
                return line.strip()[6:].strip()
        return "Summarized Research Paper"

    def _add_diagram(self, pdf, diagram):
        try:
            img_path = diagram.get("image_path")
            caption = diagram.get("caption", "")
            if img_path and os.path.exists(img_path):
                pdf.ln(2)
                pdf.image(img_path, x=25, w=160)
                pdf.set_font("Arial", 'I', 10)
                pdf.ln(2)
                pdf.multi_cell(0, 10, f"Figure {self.figure_count}: {caption}", align='C')
                pdf.ln(2)
                self.figure_count += 1
        except Exception as e:
            print(f"[ERROR] Failed to embed image {img_path}: {e}")

    def _add_table(self, pdf, table_df: pd.DataFrame):
        try:
            pdf.ln(4)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 10, f"Table {self.table_count}", ln=True, align='C')
            col_widths = [180 // len(table_df.columns)] * len(table_df.columns)
            row_height = 8

            # Header
            for i, col in enumerate(table_df.columns):
                pdf.cell(col_widths[i], row_height, str(col), border=1, ln=0, align='C')
            pdf.ln()

            # Rows
            pdf.set_font("Arial", size=10)
            for _, row in table_df.iterrows():
                for i, item in enumerate(row):
                    text = str(item)[:40]  # limit cell content length
                    pdf.cell(col_widths[i], row_height, text, border=1, ln=0, align='C')
                pdf.ln()
            self.table_count += 1
        except Exception as e:
            print(f"[ERROR] Failed to embed table: {e}")

    def generate_ieee_format_doc(self, ieee_text, diagrams=None, output_path="summarized_research_paper.pdf", tables=None):
        if not ieee_text.strip():
            print("[ERROR] Empty paper content.")
            return None

        try:
            cleaned_text = self._clean_text(ieee_text)
            lines = cleaned_text.split('\n')
            title = self._extract_title(lines)

            pdf = CustomPDF(title=title)
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=11)
            pdf.ln(5)

            headings = [
                "Title", "Abstract", "Keywords", "Introduction", "Related Work", "Literature Survey",
                "Methodology", "Experimental Results", "Discussion", "Conclusion and Future Work"
            ]

            current_section = ""
            content_buffer = []
            inserted_diagrams = set()
            tables = tables.copy() if tables else {}

            for line in lines:
                line_clean = line.strip()
                if not line_clean:
                    continue

                matched_heading = next((h for h in headings if line_clean.lower().startswith(h.lower())), None)

                if matched_heading:
                    # Write previous section's content
                    if content_buffer:
                        pdf.set_font("Arial", size=11)
                        pdf.multi_cell(0, 10, '\n'.join(content_buffer), align='J')
                        pdf.ln(4)

                        # Insert diagrams
                        if diagrams:
                            for diagram in diagrams:
                                if diagram.get("section", "").lower() == current_section.lower():
                                    img_path = diagram.get("image_path")
                                    if img_path and img_path not in inserted_diagrams:
                                        self._add_diagram(pdf, diagram)
                                        inserted_diagrams.add(img_path)

                        # Insert tables
                        if current_section in tables:
                            self._add_table(pdf, tables[current_section])
                            del tables[current_section]

                        content_buffer = []

                    # New section heading
                    pdf.set_font("Arial", 'B', 12)
                    pdf.cell(0, 10, matched_heading, ln=True)
                    pdf.ln(2)

                    current_section = matched_heading
                    remaining = line_clean[len(matched_heading):].strip(" :-")
                    if remaining:
                        content_buffer.append(remaining)
                else:
                    content_buffer.append(line_clean)

            # Final section buffer
            if content_buffer:
                pdf.set_font("Arial", size=11)
                pdf.multi_cell(0, 10, '\n'.join(content_buffer), align='J')

                if diagrams:
                    for diagram in diagrams:
                        if diagram.get("section", "").lower() == current_section.lower():
                            img_path = diagram.get("image_path")
                            if img_path and img_path not in inserted_diagrams:
                                self._add_diagram(pdf, diagram)
                                inserted_diagrams.add(img_path)

                if current_section in tables:
                    self._add_table(pdf, tables[current_section])

            pdf.output(output_path, 'F')
            return output_path

        except Exception as e:
            print(f"[ERROR] PDF generation failed: {e}")
            return None

    def generate_lit_survey_pdf(self, df):
        try:
            pdf = CustomPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Literature Survey Table", ln=True, align='C')
            pdf.ln(10)

            for index, row in df.iterrows():
                pdf.set_font("Arial", 'B', 12)
                pdf.multi_cell(0, 10, self._clean_text(f"{index+1}. {row['Paper Title']}"))
                pdf.set_font("Arial", size=11)
                for col in df.columns[1:]:
                    content = self._format_bullet_points(str(row[col])) if isinstance(row[col], str) else str(row[col])
                    pdf.set_font("Arial", 'B', 11)
                    pdf.multi_cell(0, 10, f"{col}:")
                    pdf.set_font("Arial", size=11)
                    pdf.multi_cell(0, 10, content)
                pdf.ln(5)

            buffer = BytesIO()
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            buffer.write(pdf_bytes)
            buffer.seek(0)
            return buffer

        except Exception as e:
            print(f"[ERROR] Literature Survey PDF generation failed: {e}")
            return None

def generate_pdf_from_text(text, output_path="summarized_research_paper.pdf", diagrams=None, tables=None):
    generator = ReportGenerator()
    return generator.generate_ieee_format_doc(text, diagrams=diagrams, tables=tables, output_path=output_path)
