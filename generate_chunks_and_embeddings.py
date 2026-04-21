from chunk_extraction import get_document_sections, create_rag_chunks
from embeddings import store_embeddings, get_embedding_for_chunks
from dotenv import load_dotenv
load_dotenv()


json_file_path = "data/input_pdf_content_list_v2.json"

sections = get_document_sections(json_file_path)

chunks = create_rag_chunks(sections, "input_pdf")

print(f"Total chunks: {len(chunks)}")
# for item in chunks[:7]:
#     print(f"{item}\n")


embeddings = get_embedding_for_chunks(chunks)

store_embeddings(embeddings, chunks)

print("embeddings and chunks saved.")


