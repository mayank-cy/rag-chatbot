# RAG Chatbot (Document + FAISS)

Lightweight Retrieval-Augmented-Generation (RAG) demo that:
- extracts structured blocks from PDFs (via mineru),
- builds hierarchical sections and fixed-size text chunks,
- computes embeddings (HF BGE via inference API),
- indexes with FAISS, and
- serves a Streamlit chat UI that retrieves context and queries an LLM.

Quick links
- Extraction & chunking: [chunk_extraction.py](chunk_extraction.py) — see [`chunk_extraction.get_document_sections`](chunk_extraction.py), [`chunk_extraction.build_sections_with_path`](chunk_extraction.py), [`chunk_extraction.chunk_text`](chunk_extraction.py), [`chunk_extraction.create_rag_chunks`](chunk_extraction.py)
- Embeddings & indexing: [embeddings.py](embeddings.py) — see [`embeddings.get_embedding_for_chunks`](embeddings.py), [`embeddings.store_embeddings`](embeddings.py), [`embeddings.load_embeddings_and_index`](embeddings.py), [`embeddings.retrieve_context_from_query`](embeddings.py), [`embeddings.filter_results`](embeddings.py), [`embeddings.build_context`](embeddings.py)
- Orchestration: [generate_chunks_and_embeddings.py](generate_chunks_and_embeddings.py)
- UI: [streamlit_ui.py](streamlit_ui.py) — see [`streamlit_ui.load_data`](streamlit_ui.py)
- Sample input JSON: [data/input_pdf_content_list_v2.json](data/input_pdf_content_list_v2.json)
- Shell helper: [run_extraction.sh](run_extraction.sh)
- Environment: [.env](.env) (HF_TOKEN)
- Dependencies: [requirements.txt](requirements.txt)

Prerequisites
- Python 3.8+
- HF API token (set HF_TOKEN in [.env](.env))
- Optional: mineru for PDF -> JSON extraction (not enabled in requirements)

Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# If you need mineru for extraction:
# pip install "mineru[all]"
```

Pipeline (recommended)
1. Extract PDF -> JSON (mineru). Example helper:
   ./run_extraction.sh <input_pdf_dir> <output_dir>
2. Create chunks + embeddings + FAISS index:
   python generate_chunks_and_embeddings.py
   - creates `faiss_index.bin` and `chunks.pkl` via [`embeddings.store_embeddings`](embeddings.py)
3. Run the Streamlit UI:
   streamlit run streamlit_ui.py
   - UI loads index+chunks via [`streamlit_ui.load_data`](streamlit_ui.py) → [`embeddings.load_embeddings_and_index`](embeddings.py)

Notes & tips
- The sample JSON used for development is at [data/input_pdf_content_list_v2.json](data/input_pdf_content_list_v2.json).
- HF embedding endpoint is configured in [embeddings.py](embeddings.py). Make sure your token in [.env](.env) is valid and has inference access.
- Chunking parameters live in [`chunk_extraction.chunk_text`](chunk_extraction.py) (chunk_size, overlap) — tune for your use case.
- FAISS index uses inner product with normalized vectors for cosine-similarity.

Troubleshooting
- If HF inference returns 503, [`embeddings.get_embedding`](embeddings.py) contains a retry/backoff pattern.
- If Streamlit fails to load index/files, ensure `faiss_index.bin` and `chunks.pkl` are present in the project root after running the generator script.

License & security
- Do not commit [.env](.env) or keys to VCS. (.gitignore already excludes `.env` and outputs.)
- This repo is a demo; adjust rate limits, caching, and prompts before production use.

Contributing
- Use the existing modules and functions linked above when adding features or tests.
- Keep code modular: extraction → chunking → embedding → indexing → serving.

```// filepath: /Users/mayankchoudhary/Desktop/rag_project/README.md
# RAG Chatbot (Document + FAISS)

Lightweight Retrieval-Augmented-Generation (RAG) demo that:
- extracts structured blocks from PDFs (via mineru),
- builds hierarchical sections and fixed-size text chunks,
- computes embeddings (HF BGE via inference API),
- indexes with FAISS, and
- serves a Streamlit chat UI that retrieves context and queries an LLM.

Quick links
- Extraction & chunking: [chunk_extraction.py](chunk_extraction.py) — see [`chunk_extraction.get_document_sections`](chunk_extraction.py), [`chunk_extraction.build_sections_with_path`](chunk_extraction.py), [`chunk_extraction.chunk_text`](chunk_extraction.py), [`chunk_extraction.create_rag_chunks`](chunk_extraction.py)
- Embeddings & indexing: [embeddings.py](embeddings.py) — see [`embeddings.get_embedding_for_chunks`](embeddings.py), [`embeddings.store_embeddings`](embeddings.py), [`embeddings.load_embeddings_and_index`](embeddings.py), [`embeddings.retrieve_context_from_query`](embeddings.py), [`embeddings.filter_results`](embeddings.py), [`embeddings.build_context`](embeddings.py)
- Orchestration: [generate_chunks_and_embeddings.py](generate_chunks_and_embeddings.py)
- UI: [streamlit_ui.py](streamlit_ui.py) — see [`streamlit_ui.load_data`](streamlit_ui.py)
- Sample input JSON: [data/input_pdf_content_list_v2.json](data/input_pdf_content_list_v2.json)
- Shell helper: [run_extraction.sh](run_extraction.sh)
- Environment: [.env](.env) (HF_TOKEN)
- Dependencies: [requirements.txt](requirements.txt)

Prerequisites
- Python 3.8+
- HF API token (set HF_TOKEN in [.env](.env))
- Optional: mineru for PDF -> JSON extraction (not enabled in requirements)

Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# If you need mineru for extraction:
# pip install "mineru[all]"
```

Pipeline (recommended)
1. Extract PDF -> JSON (mineru). Example helper:
   ./run_extraction.sh <input_pdf_dir> <output_dir>
2. Create chunks + embeddings + FAISS index:
   python generate_chunks_and_embeddings.py
   - creates `faiss_index.bin` and `chunks.pkl` via [`embeddings.store_embeddings`](embeddings.py)
3. Run the Streamlit UI:
   streamlit run streamlit_ui.py
   - UI loads index+chunks via [`streamlit_ui.load_data`](streamlit_ui.py) → [`embeddings.load_embeddings_and_index`](embeddings.py)

Notes & tips
- The sample JSON used for development is at [data/input_pdf_content_list_v2.json](data/input_pdf_content_list_v2.json).
- HF embedding endpoint is configured in [embeddings.py](embeddings.py). Make sure your token in [.env](.env) is valid and has inference access.
- Chunking parameters live in [`chunk_extraction.chunk_text`](chunk_extraction.py) (chunk_size, overlap) — tune for your use case.
- FAISS index uses inner product with normalized vectors for cosine-similarity.

Troubleshooting
- If HF inference returns 503, [`embeddings.get_embedding`](embeddings.py) contains a retry/backoff pattern.
- If Streamlit fails to load index/files, ensure `faiss_index.bin` and `chunks.pkl` are present in the project root after running the generator script.

License & security
- Do not commit [.env](.env) or keys to VCS. (.gitignore already excludes `.env` and outputs.)
- This repo is a demo; adjust rate limits, caching, and prompts before production use.

Contributing
- Use the existing modules and functions linked above when adding features or tests.
- Keep code modular: extraction → chunking → embedding → indexing → serving.
