from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

headers_to_split_on = [
    ("#", "Heading 1"),
    ("##", "Heading 2"),
    ("###", "Heading 3")
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

def split_page(page_path, root_path):
    with open(page_path, "r", encoding="utf-8") as f:
        content = f.read()
    docs = markdown_splitter.split_text(content)
    text_splits = text_splitter.split_documents(docs)
    docs = []
    for split in text_splits:
        docs.append({
            "filename": page_path,
            "path": page_path.replace(root_path, ""),
            "content": split.page_content
        })
    return docs