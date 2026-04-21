import json

with open("data/input_pdf_content_list_v2.json") as f:
    data = json.load(f)


###

def extract_text_from_block(block):
    btype = block["type"]
    content = block.get("content", {})

    # ---- TITLE ----
    if btype == "title":
        items = content.get("title_content", [])
        return " ".join([i["content"] for i in items if i["type"] == "text"])

    # ---- PARAGRAPH ----
    elif btype == "paragraph":
        items = content.get("paragraph_content", [])
        parts = []

        for i in items:
            if i["type"] == "text":
                parts.append(i["content"])
            elif i["type"] == "equation_inline":
                parts.append(f"[EQUATION: {i['content']}]")

        return " ".join(parts)

    # ---- INDEX / TABLE OF CONTENTS ----
    elif btype == "index":
        items = content.get("list_items", [])
        return "\n".join([
            " ".join([x["content"] for x in item["item_content"] if x["type"] == "text"])
            for item in items
        ])

    # ---- IMAGE ----
    elif btype == "image":
        path = content.get("image_source", {}).get("path", "")
        captions = content.get("image_caption", [])

        caption_text = " ".join([c["content"] for c in captions if c["type"] == "text"])

        return f"[IMAGE: {path}] {caption_text}"

    # ---- IGNORE NOISE ----
    elif btype in ["page_header", "page_footer", "page_number", "page_footnote"]:
        return None

    return None


###

def build_sections_with_path(blocks):
    sections = []
    stack = []

    for block in blocks:
        btype = block["type"]

        if btype == "title":
            level = block["content"].get("level", 1)
            title_text = extract_text_from_block(block)

            while stack and stack[-1]["level"] >= level:
                stack.pop()

            parent_path = stack[-1]["path"] if stack else []

            node = {
                "title": title_text,
                "level": level,
                "content": [],
                "path": parent_path + [title_text]
            }

            stack.append(node)

            if len(stack) == 1:
                sections.append(node)

        else:
            text = extract_text_from_block(block)
            if text and stack:
                stack[-1]["content"].append(text)

    return sections


def get_document_sections(extracted_json_path):
    with open(extracted_json_path) as f:
        data = json.load(f)

    all_blocks = []
    for page in data:
        all_blocks.extend(page)
    
    sections = build_sections_with_path(all_blocks)

    return sections

    

#########################################


def chunk_text(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


# ====================================================
#
# ====================================================

def create_rag_chunks(sections, source_name):
    final_chunks = []

    for sec in sections:
        full_text = "\n".join(sec["content"]).strip()

        if not full_text:
            continue

        sub_chunks = chunk_text(full_text)

        for i, chunk in enumerate(sub_chunks):
            final_chunks.append({
                "text": chunk,
                "section_path": " > ".join(sec["path"]),
                "section_level": sec["level"],
                "chunk_id": i,
                "source": source_name
            })

    return final_chunks


if __name__=="__main__":
    
    json_file_path = "data/input_pdf_content_list_v2.json"

    sections = get_document_sections(json_file_path)

    chunks = create_rag_chunks(sections, "input_pdf")

    print(f"Total chunks: {len(chunks)}")
    for item in chunks[:5]:
        print(f"{item}\n")