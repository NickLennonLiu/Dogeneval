import json

def load_cat_doc_mapping(file='/home/junetheriver/codes/qa_generation/huawei/ability_analysis/cat_doc_mapping.json'):
    with open(file, 'r') as f:
        cat_doc_mapping = json.load(f)
    return cat_doc_mapping

def load_cat_doc_by_mapping(mappings, files):
    cat_docs = {cat: [] for cat in mappings.keys()}
    for cat, paths in mappings.items():
        for file in files:
            for path in paths:
                if path in file['path']:
                    cat_docs[cat].append(file)
                    break
    return cat_docs

def load_cat_doc(files):
    cat_doc_mapping=load_cat_doc_mapping()
    return load_cat_doc_by_mapping(cat_doc_mapping, files)

if __name__ == "__main__":
    result = load_cat_doc_mapping()
    print(result)