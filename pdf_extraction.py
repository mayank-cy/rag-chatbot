# import os
# from mineru.pdf2md import convert_pdf_to_markdown

# def pdf_to_markdown(input_pdf_path: str, output_dir: str):
#     """
#     Convert PDF to structured markdown using MinerU.
#     """

#     # Ensure output directory exists
#     os.makedirs(output_dir, exist_ok=True)

#     # Output markdown file path
#     output_md_path = os.path.join(
#         output_dir,
#         os.path.splitext(os.path.basename(input_pdf_path))[0] + ".md"
#     )

#     # Convert PDF → Markdown
#     markdown_content = convert_pdf_to_markdown(input_pdf_path)

#     # Save markdown
#     with open(output_md_path, "w", encoding="utf-8") as f:
#         f.write(markdown_content)

#     print(f"✅ Markdown saved at: {output_md_path}")


# if __name__ == "__main__":
#     input_pdf = "data/input_pdf.pdf"        # your PDF path
#     output_folder = "outputs"     # target folder

#     pdf_to_markdown(input_pdf, output_folder)

from mineru import MinerU

miner = MinerU()
markdown = miner.convert("data/input_pdf.pdf", output_format="markdown")

with open("output.md", "w") as f:
    f.write(markdown)